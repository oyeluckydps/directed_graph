import networkx as nx


import extended_DiGraph as edg
import collection_DiGraph as cdg
import prime_DiGraph_Generator as pdgg
import utils


def edg_handling():
    EDG1 = edg.DiGraph()
    EDG1.add_edges_from([[1,2], [2,3], [2,4], [3,1], [4,1]])
    print(EDG1.nodes())
    print(EDG1.adj)
    print(EDG1)
    EDG2 = EDG1.normalize()
    print(EDG2)
    print("Strongly Connected: ", nx.is_strongly_connected(EDG2))
    print("Faster Isomorphic: ", nx.faster_could_be_isomorphic(EDG1, EDG2))
    print("Is Isomorphic: ", nx.is_isomorphic(EDG1, EDG2))
    print("Strongly Connected IMPLEMENTATION: ", EDG2.is_strongly_connected)
    print("Is Isomorphic IMPLEMENTATION: ", EDG2.is_isomorphic(EDG1))
    print("Is Prime IMPLEMENTATION: ", EDG2.is_prime)

    EDG3 = edg.DiGraph(EDG2)
    EDG3.remove_edge(0, 2)
    EDG4 = edg.DiGraph(EDG3)
    EDG4.add_edge(1, 2)
    EDG4 = EDG4.normalize()
    print(EDG4)
    print("EDG3: Strongly Connected IMPLEMENTATION: ", EDG3.is_strongly_connected)
    print("EDG4: Strongly Connected IMPLEMENTATION: ", EDG4.is_strongly_connected)
    print("EDG1, EDG4: Is Isomorphic IMPLEMENTATION: ", EDG4.is_isomorphic(EDG1))
    print("EDG3: Is Prime IMPLEMENTATION: ", EDG3.is_prime)
    print("EDG4: Is Prime IMPLEMENTATION: ", EDG4.is_prime)

    EDG5 = edg.DiGraph(EDG4)
    EDG5.add_edges_from([[2,3], [3,0]])
    print("EDG5: Is Prime IMPLEMENTATION: ", EDG5.is_prime)


def cdg_handling():
    CDG2_prime = cdg.CollectionDiGraphs('nodes2_prime')
    Nodes2_Prime1 = edg.DiGraph()
    Nodes2_Prime1.add_edges_from([[1, 2], [2, 1]])
    print(Nodes2_Prime1.is_strongly_connected)
    CDG2_prime.add_DGs([Nodes2_Prime1], normalize=True)
    print(CDG2_prime.DGs)

    Nodes3_Prime1 = edg.DiGraph()
    Nodes3_Prime2 = edg.DiGraph()
    Nodes3_Prime1.add_edges_from([[1, 2], [2, 3], [3, 1]])
    Nodes3_Prime2.add_edges_from([[1, 2], [2, 1], [3, 2], [2, 3]])
    CDG3_prime_all = CDG2_prime
    CDG3_prime_all.name = 'all_primes_till_3nodes'
    CDG3_prime_all.add_DGs([Nodes3_Prime1, Nodes3_Prime2], normalize=True)
    print(CDG3_prime_all.DGs)
    CDG3_prime_all_filename = 'CDG3_prime_all'
    CDG3_prime_all.save_object(CDG3_prime_all_filename)

    del CDG3_prime_all
    CDG3_prime_all_reloaded = cdg.load_object(filename=CDG3_prime_all_filename)
    print(CDG3_prime_all_reloaded.DGs)

def pdgg_handling():
    filename = 'consolidated'
    for i in range(3,16):
        _6nodes = pdgg.primeDiGraphGenerator(filename)
        print('Computing for ' + str(i) + ' nodes.')
        _6nodes.compute_next_primes()
        # all_encountered_digraphs, all_primes = _6nodes.compute_next_primes()
        # all_encountered_digraphs.save_object(filename=filename+f'_ALL_{i}_nodes')
        # utils.save_data(utils.time_block.timings, filename=filename+f'_TIMING_LOG_{i}_nodes.txt')
        utils.time_block.timings = {}
        _6nodes.save_data(filename)
        del _6nodes

def optimized_pdgg_handling():
    for i in range(3, 25):
        _12nodes = pdgg.primeDiGraphGenerator('least_computation')
        print('Computing for ' + str(i) + ' nodes.')
        best_combo = _12nodes.optimized_combo_for_next_prime_computation()
        _12nodes.compute_next_primes_optimized(*best_combo)
        _12nodes.save_data('least_computation')
        del _12nodes

def find_prime_testing():
    EDG1 = edg.DiGraph()
    a = []
    for i in range(5):
        for j in range(5):
            if i == j:
                continue
            else:
                a.append((i, j))
    EDG1.add_edges_from(a)
    (all_primes, checked_DGs) = pdgg.find_primes(EDG1)
    print('Printing the Graph in question.')
    print(EDG1)
    print('Printing all the primes of the given graph')
    for prime in all_primes:
        print(prime)
    print('Printing all the graphs that were checked!')
    for DG in list(checked_DGs.DGs):
        print(DG)


def find_prime_testing_ppt():
    EDG1 = edg.DiGraph()
    EDG1.add_edges_from([(0,1), (0,3), (1,2), (1,3), (2,0), (3,1), (3,2)])
    (all_primes, checked_DGs) = pdgg.find_primes(EDG1)
    print('Printing the Graph in question.')
    print(EDG1)
    print('Printing all the primes of the given graph')
    for prime in all_primes:
        print(prime)
    print('Printing all the graphs that were checked!')
    for DG in list(checked_DGs.DGs):
        print(DG)

def add_a_node_testing():
    EDG1 = edg.DiGraph()
    EDG1.add_edges_from([[1, 2], [2, 3], [2, 4], [3, 1], [4, 1]])

def weisfeiler_lehman_debug():
    adj_list = {0: [2, 4], 1: [0], 2: [0], 3: [1, 5], 4: [3], 5: [3]}
    EDG1 = edg.DiGraph()
    for k, l in adj_list.items():
        for e in l:
            EDG1.add_edge(k, e)
    adj_list2 = {0: [2, 3], 1: [4, 5], 2: [1], 3: [1], 4: [0], 5: [0]}
    EDG2 = edg.DiGraph()
    for k, l in adj_list2.items():
        for e in l:
            EDG2.add_edge(k, e)
    print(EDG1.isophorm_hash)
    print(EDG2.isophorm_hash)

if __name__ == '__main__':
    # edg_handling()
    # cdg_handling()
    pdgg_handling()
    # find_prime_testing()
    # weisfeiler_lehman_debug()
    # optimized_pdgg_handling()
    # find_prime_testing_ppt()