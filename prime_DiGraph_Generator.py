import networkx as nx
import _pickle as pickle
from copy import deepcopy
from itertools import product
from pathlib import Path

import networkx.exception

import extended_DiGraph as edg
import collection_DiGraph as cdg


Nodes2_Prime1 = edg.DiGraph()
Nodes2_Prime1.add_edges_from([[1, 2], [2, 1]])
Nodes2_Prime1 = Nodes2_Prime1.normalize()

def find_primes(DG, already_checked_cdg = None):
    if already_checked_cdg is None:
        already_checked_cdg = cdg.CollectionDiGraphs()
    if not DG.is_strongly_connected:
        return ([], already_checked_cdg)
    if already_checked_cdg.isomorphic_graph_exists(DG):
        return ([], already_checked_cdg)
    else:
        already_checked_cdg.add_DGs([DG])
    if DG.is_prime:
        return ([DG], already_checked_cdg)
    edge_list = list(DG.edges)
    all_primes = []
    for edge in edge_list:
        DG_temp = edg.DiGraph(DG)
        DG_temp.remove_edge(*edge)
        primes_for_this_edge_removal, already_checked_cdg = find_primes(DG_temp, already_checked_cdg)
        all_primes = all_primes + primes_for_this_edge_removal
    return (all_primes, already_checked_cdg)


def add_a_node_all_possibilities(DG, already_checked_cdg = None, check_isomorphism = True, check_primality = True, reduce_to_primes = True):
    '''
    :param DG: Directed graph to which a node is to be added
    :param all_DGs: A CDG against which isomorphism is to be checked and results are added to this CDG.
    :param check_isomorphism: If the generated DGs need to be checked for isomorphism.
    :param check_primality: Check if the newly generated DG is prime.
    :param reduce_to_primes: Reduce the DGs to their primes after formation if they are not prime.
    :return:
    '''
    all_DGs = cdg.CollectionDiGraphs()
    num_nodes = DG.number_of_nodes()
    if already_checked_cdg is None:
        already_checked_cdg = deepcopy(all_DGs)
    for in_edge_node in DG.nodes():
        for out_edge_node in DG.nodes():
            DG_temp = edg.DiGraph(DG)
            DG_temp.add_edges_from([[in_edge_node, num_nodes], [num_nodes, out_edge_node]])
            if reduce_to_primes:
                DG_reduced_to_primes, already_checked_cdg = find_primes(DG_temp, already_checked_cdg)
                all_DGs.add_DGs(DG_reduced_to_primes)
                continue
            if check_isomorphism:
                if all_DGs.isomorphic_graph_exists(DG_temp):
                    continue
            if check_primality:
                if not DG_temp.is_prime:
                    continue
            all_DGs.add_DGs([DG_temp])
    return all_DGs, already_checked_cdg


def optimized_prime_extension(DG, already_checked_cdg = None, check_isomorphism = True):
    '''
    :param DG: Directed graph to which a node is to be added
    :param all_DGs: A CDG against which isomorphism is to be checked and results are added to this CDG.
    :param check_isomorphism: If the generated DGs need to be checked for isomorphism.
    :return:
    '''
    all_DGs = cdg.CollectionDiGraphs()
    num_nodes = DG.number_of_nodes()
    if already_checked_cdg is None:
        already_checked_cdg = cdg.CollectionDiGraphs()
    for in_edge_node in DG.nodes():
        for out_edge_node in DG.nodes():
            DG_temp = edg.DiGraph(DG)
            DG_temp.add_edges_from([[in_edge_node, num_nodes], [num_nodes, out_edge_node]])
            DG_temp2 = edg.DiGraph(DG_temp)
            if DG_temp2.has_edge(in_edge_node, out_edge_node):      # Either the added node is connected to a
                # single preexisting node of a prime graph or an edge is bifurcated to add a new node.
                DG_temp2.remove_edge(in_edge_node, out_edge_node)
                _DG = DG_temp2
                if check_isomorphism:
                    if already_checked_cdg.isomorphic_graph_exists(_DG):
                        continue
                already_checked_cdg.add_DGs([_DG])
                # No need to check for primality as it will definitely be a prime.
                all_DGs.add_DGs([_DG])
            else:
                _DG = DG_temp
                if check_isomorphism:
                    if already_checked_cdg.isomorphic_graph_exists(_DG):
                        continue
                already_checked_cdg.add_DGs([_DG])
                if not _DG.is_prime:
                    continue
                all_DGs.add_DGs([_DG])
    return all_DGs, already_checked_cdg


def connect_nexus_all_possibilities(lower_DG, higher_DG, already_checked_cdg = None, check_isomorphism = True, check_primality = True, reduce_to_primes = True):
    '''
    :param lower_DG: A Directed graph
    :param higher_DG: Another Directed graph
    :param all_DGs: A CDG against which isomorphism is to be checked and results are added to this CDG.
    :param check_isomorphism: If the generated DGs need to be checked for isomorphism.
    :param check_primality: Check if the newly generated DG is prime.
    :param reduce_to_primes: Reduce the DGs to their primes after formation if they are not prime.
    :return:
    '''
    all_DGs = cdg.CollectionDiGraphs()
    if already_checked_cdg is None:
        already_checked_cdg = deepcopy(all_DGs)
    higher_DG = higher_DG.normalize()
    higher_DG_copy = edg.DiGraph(higher_DG)
    higher_DG_copy = nx.relabel_nodes(higher_DG_copy, {i:j for i,j in enumerate(list(range(lower_DG.number_of_nodes(),
                                        lower_DG.number_of_nodes()+higher_DG_copy.number_of_nodes())))})
    l_h_nexus_nodes_for_connection_all_possibilities = product(
        product(lower_DG.nodes, lower_DG.nodes),
        product(higher_DG_copy.nodes, higher_DG_copy.nodes)
    )
    for l_nodes, h_nodes in l_h_nexus_nodes_for_connection_all_possibilities:
        DG_new = edg.DiGraph(nx.disjoint_union(lower_DG, higher_DG))
        DG_new.add_edges_from([[l_nodes[0], h_nodes[0]], [h_nodes[1], l_nodes[1]]])
        if reduce_to_primes:
            DG_reduced_to_primes, already_checked_cdg = find_primes(DG_new, already_checked_cdg)
            all_DGs.add_DGs(DG_reduced_to_primes)
            continue
        if check_isomorphism:
            if all_DGs.isomorphic_graph_exists(DG_new):
                continue
        if check_primality:
            if not DG_new.is_prime:
                continue
        all_DGs.add_DGs([DG_new])
    return all_DGs, already_checked_cdg


class primeDiGraphGenerator():
    def __init__(self, name, path_prefix = ''):
        self.path_prefix = path_prefix
        self.name = name
        try:
            with open(Path(path_prefix) / Path(self.name + '._pickle'), 'rb') as inp:
                self.saved_data_filename = pickle.load(inp)
                self.highest_prime_computed = pickle.load(inp)
        except FileNotFoundError:
            self.saved_data_filename = None
            self.cdg = cdg.CollectionDiGraphs()
            self.cdg.add_DGs([Nodes2_Prime1])
            self.highest_prime_computed = 2
        if self.saved_data_filename is not None:
            try:
                with open(Path(path_prefix) / Path(self.saved_data_filename + 'CDG._pickle'), 'rb') as inp:
                    self.cdg = pickle.load(inp)
            except:
                raise('Error in loading data!')


    def save_data(self, cdg_filename, path_prefix = ''):
        self.cdg.save_object(cdg_filename + 'CDG', path_prefix=path_prefix)
        with open(Path(path_prefix)/Path(self.name+'._pickle'), 'wb') as outp:
            pickle.dump(cdg_filename, outp, 0)
            pickle.dump(self.highest_prime_computed, outp, 0)


    def compute_next_primes(self):
        prime_to_compute = self.highest_prime_computed + 1
        highest_current_primes = self.cdg.list_of_computed_DGs(self.highest_prime_computed)
        next_primes = cdg.CollectionDiGraphs()
        all_computed_isomorphs = cdg.CollectionDiGraphs()
        tot_highest_curr_primes = len(highest_current_primes)
        for i, a_highest_prime in enumerate(highest_current_primes):
            print(str(i+1) + '/' + str(tot_highest_curr_primes), end=':\t')
            computed_primes, all_computed_isomorphs = optimized_prime_extension(a_highest_prime, all_computed_isomorphs)
            print("New Primes: ", str(len(computed_primes.DGs)), ",\t Total isomorphs checked so far: ", str(len(all_computed_isomorphs.DGs)))
            next_primes.add_DGs(computed_primes.DGs)
        self.highest_prime_computed = prime_to_compute
        self.cdg.add_DGs(next_primes.DGs)
        return next_primes

    def optimized_combo_for_next_prime_computation(self):
        '''
        Find the combination that will reduce the computation for next prime computation.
        :return:
        '''
        current_highest_computed = self.highest_prime_computed
        prime_to_compute = current_highest_computed
        computations_req = {(1,current_highest_computed): self.cdg.count_of_computed_DGs(current_highest_computed)*(current_highest_computed**2)}
        for smaller_nexus in range(2, prime_to_compute//2+1):
            larger_nexus = prime_to_compute-smaller_nexus
            computations_req[(smaller_nexus,larger_nexus)] = smaller_nexus*smaller_nexus*larger_nexus*larger_nexus* \
                    self.cdg.count_of_computed_DGs(smaller_nexus)*self.cdg.count_of_computed_DGs(larger_nexus)
        print(computations_req)
        min_combo = min(computations_req, key=computations_req.get)
        print("Minimum computation required for: ", min_combo)
        return min_combo

    def compute_next_primes_optimized(self, lower_nexus_n, higher_nexus_n):
        if lower_nexus_n == 1:
            return self.compute_next_primes()
        prime_to_compute = self.highest_prime_computed + 1
        lower_nexus = self.cdg.list_of_computed_DGs(lower_nexus_n)
        higher_nexus = self.cdg.list_of_computed_DGs(higher_nexus_n)
        next_primes = cdg.CollectionDiGraphs()
        all_computed_isomorphs = cdg.CollectionDiGraphs()
        l_h_nexus = product(lower_nexus, higher_nexus)
        # total_nexus_combos = len(list(l_h_nexus))
        for a_l_h_prime in l_h_nexus:
            # print(str(i+1) + '/' + str(total_nexus_combos), end=':\t')
            computed_primes, all_computed_isomorphs = connect_nexus_all_possibilities(*a_l_h_prime, all_computed_isomorphs)
            print("New Primes: ", str(len(computed_primes.DGs)), ",\t Total isomorphs checked so far: ", str(len(all_computed_isomorphs.DGs)))
            next_primes.add_DGs(computed_primes.DGs)
        self.highest_prime_computed = prime_to_compute
        self.cdg.add_DGs(next_primes.DGs)
        return next_primes