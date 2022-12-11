import networkx as nx
from itertools import product

import extended_DiGraph as edg
import collection_DiGraph as cdg

def fully_connected_DG(nodes_count):
    EDG1 = edg.DiGraph()
    a = [(elem[0],elem[1]) for elem in list(product(list(range(nodes_count)), repeat = 2)) if elem[0] != elem[1]]
    EDG1.add_edges_from(a)
    return EDG1

def find_all_DGs(DG, already_checked_cdg = None):
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
    all_DGs = [DG]
    for edge in edge_list:
        DG_temp = edg.DiGraph(DG)
        DG_temp.remove_edge(*edge)
        reduced_DGs_for_this_edge_removal, already_checked_cdg = find_all_DGs(DG_temp, already_checked_cdg)
        all_DGs = all_DGs + reduced_DGs_for_this_edge_removal
    return (all_DGs, already_checked_cdg)