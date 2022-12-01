import networkx as nx
from copy import deepcopy

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
        return (sorted(d for n,d in self.out_degree), sorted(d for n,d in self.in_degree))

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