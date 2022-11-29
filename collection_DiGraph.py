import networkx as nx
import extended_DiGraph as edg

import _pickle as pickle
import warnings

import pandas as pd

def load_object(filename, number_of_objects = 1):
    if number_of_objects == 1:
        with open(filename+'._pickle', 'rb') as inp:
            return pickle.load(inp)
    else:
        object_list = []
        with open(filename, 'rb') as inp:
            for i in range(number_of_objects):
                object_list.append(pickle.load(inp))
        return object_list

class CollectionDiGraphs():

    def __init__(self, name='', is_prime_collection = False):
        """
        Initialize a DiGraphs collection
        """
        self.name = name
        self.is_prime_collection = is_prime_collection
        self.DGs = []
        self.number_of_nodes = []
        self.DG_isophorm_hash = []

    @property
    def df(self):
        '''
        Make a df out of self.DGs here!
        :return:
        '''
        df = pd.DataFrame(columns= ['number_of_nodes', 'number_of_edges', 'is_strongly_connected', 'is_prime', 'adj_', 'DiGraph'])
        for (n_nodes, DG) in zip(self.number_of_nodes, self.DGs):
            df.loc[len(df.index)] = [n_nodes, DG.number_of_edges(), DG.is_strongly_connected, DG.is_prime, DG.adj_, DG]
        return df

    def add_DGs(self, DGs, normalize = False, check_against_isomorphism = False):
        for DG in DGs:
            if check_against_isomorphism:
                if self.isomorphic_graph_exists(DG):
                    continue
            if normalize:
                DG = DG.normalize()
            self.DGs.append(DG)
            self.number_of_nodes.append(DG.number_of_nodes())
            self.DG_isophorm_hash.append(DG.isophorm_hash)

    def find_row(self, query):
        df = self.df.query(query)
        if len(df.index) == 0:
            warnings.warn("No match found for query!")
        elif len(df.index) > 1:
            warnings.warn("Multiple matches found for the query!")
            return (df.index, df)
        else:
            return (df.index[0], df)

    def list_of_highest_computed_primes(self, highest_num = None):
        if highest_num is None:
            highest_num = max(self.number_of_nodes)
        return [DG for DG, n_nodes in zip(self.DGs, self.number_of_nodes) if n_nodes==highest_num]

    def isomorphic_graph_exists(self, DG2):
        DG2_hash = DG2.isophorm_hash
        for (DG, DG_hash) in zip(self.DGs, self.DG_isophorm_hash):
            if (DG2_hash==DG_hash) and DG.is_isomorphic(DG2):
                return True
        return False

    def save_object(self, filename):
        with open(filename+'._pickle', 'wb') as outp:
            pickle.dump(self, outp, -1)
        self.df.to_csv(filename+'.csv')
