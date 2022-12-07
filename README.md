# directed_graph
A tool to generate and experiment with directed graphs. It is built over networkx by enhancing its features.

## Two of the prime objectives of this tool are:
- Generate all possible prime directed graphs for a given number of nodes. A prime DG refers to a DG to which is strongly connected and if any edge from the given graph is removed it no longer remains strongly connected.
Such graphs are helpful in generation of all possible DGs for a given number of nodes. This is useful in rigorous testing of any geraph algorithm or system. 
Note that isomorphic graphs are pruned at each step.
- Generate a random directed strongly connected graph of given nodes. This is helpful in generation of strongly connected DGs for higher number of nodes e.g. 20-50. It helps in testing graph algorithms and systems with higher number of nodes where it is difficult to find all possible prime isomorphs.

# File Description
### extended_DiGraph (edg)
An enhancement over the DiGraph class of networkx that lets us do following in simplified manner:

<b>@property</b>
1. adj_: Returns adjancency list in form of dict.
2. isophorm_hash: Returns the weisfeiler_lehman_graph_hash of the graph. Note that two graphs can have same hash and yet not be isomorph but viceversa is not true.

<b>Mehods</b>
1. normalize: Normalize the graph such that the nodes are named successively from int(0) onwards. Also the nodes are arranged in decreasing order of edge metric = num_of_outgoing_nodes*nodes_in_geaph^2+number of incoming nodes.
2. is_strongly_connected: Return true if graph is strongly connected else False.
3. is_prime: Returns True is the graph is Prime (description above) else False.
4. is_isomorphic: Checks if the graph is isomorphic to other graph provided in argument.

### collection_DiGraph (cdg)
A class that is helpful in preserving a collection of edg. It helps in saving the collection of graph in csv and PICKLE and loading from a CSV/PICKLE.

<b>@property</b>
1. df: Shows the collection of DGs in form of Pandas dataframe. The columns are 'isomorphic_hash', 'number_of_nodes', 'number_of_edges', 'is_strongly_connected', 'is_prime', 'adj_'.

<b>Mehods</b>
1. add_DG: Add a directed graph to the collection.
2. list_of_computed_DGS: List all the DGs in collection for a given number of nodes.
3. size_of_computed_DGs: Tells the count of DGs in collection for a given number of ndoes.
4. isomorphic_graph_exists: Returns True if the DG passed in argument is isomorphic to any of the DGs in collection.
5. save_object: Save the collection in .PICKLE format.

<b>Non-class methods</b>
1. indices: A faster implementation over Python lists to get list of all matching indices for a given list and element.
2. load_object: Load an object of cdg class from saved .PICKLE file.

### prime_DiGraph_Generator
A class to help in generation of all prime DiGraphs. Given the current implementation it is only possible to generate all primes till 10 modes. With faster and better hashing as well as parallelization, it may be possible to generate primes till higher nodes.

<b>Non-class methods</b>
1. find_primes: Given any strongly connected Digraph, it would find all the primes (of equal number of nodes) that can be evolved (by adding edges) into this DG. It also has additional functionality to skip already checked graphs thus reducing calculations.
2. add_a_node_all_possibilities: Given a DG of nodes n, it would add a node to the graph and form n^2 new DGs by connecting the new node to existing nodes in all possible ways. Then these n^2 graphs are reduced to primes and all such primes are collected and returned in cdg.
3. connect_nexus_all_possibilities: This function takes two strongly connected DGs (called lower nexus and higher nexus). It forms one edge from lower nexus to higher nexus and another other way round in all possible ways. It then reduces these newly formed graphs into primes and returns them in cdg.

<b>Mehods</b>
1. __init__: Loads self.cdg and self.highest_prime_computed from already saved file. If there is not saved data then it starts with self.highest_prime_computed=2 and single prime of 2 nodes in cdg.
2. save_data: Saves the object itself in .PICKLE format.
3. compute_next_primes: Given the all primes in self.cdg, it adds a node to all the primes and in attempt to find primes with next number of nodes.
4. optimized_combo_for_next_prime_computation: Not to be used.
5. compute_next_primes_optimized: Not to be used.

### random_DiGraph_generator
A collection of functions to generate a random strongly connected DiGraph.

1. find_primes_probabilistically: Given any strongly connected DG, the DG is reduced to one prime by randomly removing edges using DFS.
2. add_edges_probabilistically: Add edges to a given DG probabilistically with the mentioned probability.
3. random_DiGraph: Combine the above two functions to generate a random prime of n nodes and then adds edges probabilistically.
