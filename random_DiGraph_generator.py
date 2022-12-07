import random
import networkx as nx
from itertools import product
import sys

import extended_DiGraph as edg
import collection_DiGraph as cdg

sys.setrecursionlimit(10**8)

def find_primes_probabilistically(DG, already_checked_cdg = None):
    print("Edges in current DG = "+str(DG.number_of_edges()))
    if already_checked_cdg is None:
        already_checked_cdg = cdg.CollectionDiGraphs()
    if not DG.is_strongly_connected:
        return (None, already_checked_cdg)
    if DG.is_prime:
        return (DG, already_checked_cdg)
    edge_list = set(DG.edges)
    already_removed_edge = set()
    while True:
        try:
            not_tested_edges = edge_list-already_removed_edge
            an_edge_to_remove = random.choice(list(not_tested_edges))
        except IndexError:
            break
        else:
            DG_temp = edg.DiGraph(DG)
            DG_temp.remove_edge(*an_edge_to_remove)
            prime_DG, already_checked_cdg = find_primes_probabilistically(DG_temp, already_checked_cdg)
            if prime_DG is not None:
                return prime_DG, already_checked_cdg
            else:
                already_removed_edge.add(an_edge_to_remove)
    return (None, already_checked_cdg)

def add_edges_probabilistically(prime_DG, edge_probability=None):
    DG = prime_DG.normalize()
    if edge_probability is None:
        edge_probability = 0.5
    assert edge_probability<=1
    assert edge_probability>=0
    all_edge_list = set([(i, j) for i, j in product(range(DG.number_of_nodes()), range(DG.number_of_nodes())) if i != j])
    edges_to_add = all_edge_list-set(DG.edges)
    for edge in edges_to_add:
        if random.random()<edge_probability:
            DG.add_edge(*edge)
    return DG

def random_DiGraph(num_nodes, edge_probability = None):
    """
    :param num_nodes: Number of nodes in the random graph.
    :param edge_probability: Probability with which an edge has to be added over a prime graph.
    :return: A randomly generated graph.
    """
    DG = edg.DiGraph()
    edge_list = [(i, j) for i, j in product(range(num_nodes), range(num_nodes)) if i != j]
    DG.add_edges_from(edge_list)
    prime_DG, _ = find_primes_probabilistically(DG)
    rand_DG = add_edges_probabilistically(prime_DG, edge_probability)
    return rand_DG

if __name__ == '__main__':
    rand_prime_DG = random_DiGraph(10,0.5)
    print(rand_prime_DG)