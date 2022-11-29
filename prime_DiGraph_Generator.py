import networkx as nx

import extended_DiGraph as edg
import collection_DiGraph as cdg

import _pickle as pickle
from copy import deepcopy

Nodes2_Prime1 = edg.DiGraph()
Nodes2_Prime1.add_edges_from([[1, 2], [2, 1]])
Nodes2_Prime1 = Nodes2_Prime1.normalize()

def find_primes(DG, already_checked_cdg = None):
    if already_checked_cdg is None:
        already_checked_cdg = cdg.CollectionDiGraphs()
    if not DG.is_strongly_connected:
        return ([], already_checked_cdg)
    # if already_checked_cdg.isomorphic_graph_exists(DG):
    #     return ([], already_checked_cdg)
    # else:
    #     already_checked_cdg.add_DGs([DG])
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
    DG.add_node(num_nodes)
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


class primeDiGraphGenerator():
    def __init__(self, name):
        self.name = name
        try:
            with open(self.name + '._pickle', 'rb') as inp:
                self.saved_data_filename = pickle.load(inp)
                self.highest_prime_computed = pickle.load(inp)
        except FileNotFoundError:
            self.saved_data_filename = None
            self.cdg = cdg.CollectionDiGraphs()
            self.cdg.add_DGs([Nodes2_Prime1])
            self.highest_prime_computed = 2
        if self.saved_data_filename is not None:
            try:
                with open(self.saved_data_filename + 'CDG._pickle', 'rb') as inp:
                    self.cdg = pickle.load(inp)
            except:
                raise('Error in loading data!')


    def save_data(self, cdg_filename):
        with open(self.name+'._pickle', 'wb') as outp:
            self.cdg.save_object(cdg_filename+'CDG')
            pickle.dump(cdg_filename, outp, 0)
            pickle.dump(self.highest_prime_computed, outp, 0)


    def compute_next_primes(self):
        prime_to_compute = self.highest_prime_computed + 1
        highest_current_primes = self.cdg.list_of_highest_computed_primes(self.highest_prime_computed)
        next_primes = cdg.CollectionDiGraphs()
        all_computed_isomorphs = cdg.CollectionDiGraphs()
        tot_highest_curr_primes = len(highest_current_primes)
        for i, a_highest_prime in enumerate(highest_current_primes):
            print(str(i+1) + '/' + str(tot_highest_curr_primes), end=':\t')
            computed_primes, all_computed_isomorphs = add_a_node_all_possibilities(a_highest_prime, all_computed_isomorphs)
            print("New Primes: ", str(len(computed_primes.DGs)), ",\t Total isomorphs checked so far: ", str(len(all_computed_isomorphs.DGs)))
            next_primes.add_DGs(computed_primes.DGs, check_against_isomorphism=True)
        self.highest_prime_computed = prime_to_compute
        self.cdg.add_DGs(next_primes.DGs)
        return next_primes
