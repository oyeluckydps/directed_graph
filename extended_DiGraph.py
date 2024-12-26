import networkx as nx
from copy import deepcopy
from collections import Counter
from hashlib import blake2b

class DiGraph(nx.DiGraph):
    """
    Extend the functionalities of DiGraph from networkx.
    """
    def __init__(self, incoming_graph_data = None, **attr):
        self.I_am_prime = None
        self.I_am_strongly_connected = None
        super().__init__(incoming_graph_data = incoming_graph_data, **attr)

    @property
    def adj_(self):
        return {k: [edge[1] for edge in self.out_edges(k)] for k in super(DiGraph, self).nodes()}

    @property
    def is_prime(self):
        # if self.I_am_prime is None:
        #     self.I_am_prime = self._is_prime()
        # return self.I_am_prime
        return self._is_prime()

    @property
    def is_strongly_connected(self):
        # if self.I_am_strongly_connected is None:
        #     self.I_am_strongly_connected = nx.is_strongly_connected(self)
        # return self.I_am_strongly_connected
        return nx.is_strongly_connected(self)

    def normalize(self):
        DG_rebased = DiGraph(nx.convert_node_labels_to_integers(self))
        N = DG_rebased.number_of_nodes()
        DG_edge_metric = [(DG_rebased.out_degree(node)*(N**2) + DG_rebased.in_degree(node), node) for node in DG_rebased.nodes]
        DG_edge_metric.sort()
        DG_edge_metric.reverse()
        mapping = dict(zip([n for d, n in DG_edge_metric], range(N)))
        DG_normalized = nx.relabel_nodes(DG_rebased, mapping=mapping)
        DG_normalized_sorted = DiGraph()
        DG_normalized_sorted.add_nodes_from(sorted(DG_normalized.nodes(data=True)))
        DG_normalized_sorted.add_edges_from(DG_normalized.edges(data=True))
        return DG_normalized_sorted

    @property
    def isophorm_hash(self):
        out_in_attr = {node: self.out_degree(node) * self.number_of_nodes() + self.in_degree(node) for node in self.nodes}
        nx.set_node_attributes(self, out_in_attr, 'in-out')
        dg_hash = self.weisfeiler_lehman_graph_hash(node_attr='in-out')
        return dg_hash


    def weisfeiler_lehman_graph_hash(
            G, edge_attr=None, node_attr=None, iterations=3, digest_size=16
            ):

        def weisfeiler_lehman_step(G, labels, edge_attr=None):
            """
            Apply neighborhood aggregation to each node
            in the graph.
            Computes a dictionary with labels for each node.
            """
            new_labels = {}
            for node in G.nodes():
                label = _neighborhood_aggregate(G, node, labels, edge_attr=edge_attr)
                new_labels[node] = _hash_label(label, digest_size)
            return new_labels

        # set initial node labels
        node_labels = _init_node_labels(G, edge_attr, node_attr)

        subgraph_hash_counts = []
        for _ in range(iterations):
            node_labels = weisfeiler_lehman_step(G, node_labels, edge_attr=edge_attr)
            counter = Counter(node_labels.values())
            # sort the counter, extend total counts
            subgraph_hash_counts.extend(sorted(counter.items(), key=lambda x: x[0]))

        # hash the final counter
        return _hash_label(str(tuple(subgraph_hash_counts)), digest_size)

    def is_isomorphic(self, DG2):
        return nx.is_isomorphic(self, DG2)

    def _is_prime(self):
        edge_list = deepcopy(self.edges)
        if not self.is_strongly_connected:
            return False
        for edge in edge_list:
            self.remove_edge(*edge)
            if self.is_strongly_connected:
                self.add_edge(*edge)
                return False
            else:
                self.add_edge(*edge)
        return True

    def __repr__(self, label = ''):
        msg = 'Printing the out edges chart for '+label+'\r\n'
        for k, v in self.adj_.items():
            msg = msg + str(k) + ': ' + str(v) + '\r\n'
        return msg

    def __str__(self):
        return self.__repr__()

def _hash_label(label, digest_size):
    return blake2b(label.encode("ascii"), digest_size=digest_size).hexdigest()

def _init_node_labels(G, edge_attr, node_attr):
    if node_attr:
        return {u: str(dd[node_attr]) for u, dd in G.nodes(data=True)}
    elif edge_attr:
        return {u: "" for u in G}
    else:
        return {u: str(deg) for u, deg in G.degree()}

def _neighborhood_aggregate(G, node, node_labels, edge_attr=None):
    """
    Compute new labels for given node by aggregating
    the labels of each node's neighbors.
    """
    new_label = node_labels[node] + '='
    in_label_list = []
    for nbr in G.predecessors(node):
        prefix = "" if edge_attr is None else str(G[node][nbr][edge_attr])
        in_label_list.append(prefix + node_labels[nbr] + ",")
    new_label += "".join(sorted(in_label_list))
    new_label += '-'
    out_label_list = []
    for nbr in G.successors(node):
        prefix = "" if edge_attr is None else str(G[node][nbr][edge_attr])
        out_label_list.append(prefix + node_labels[nbr] + ",")
    new_label += "".join(sorted(out_label_list))
    return new_label