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
        columns = ['number_of_nodes', 'number_of_edges', 'is_strongly_connected', 'is_prime', 'adj_', 'DiGraph']
        self.df = pd.DataFrame(columns= columns)

    def add_DGs(self, DGs, normalize = False, check_against_isomorphism = False):
        df = pd.DataFrame(columns = self.df.columns)
        start_index = self.df.index[-1]+1 if len(self.df.index)>0 else 0
        for index_offset, DG in enumerate(DGs):
            if check_against_isomorphism:
                for row in self.df.iterrows():
                    if DG.is_isomrphic(row.DiGraph):
                        raise ValueError('One of the DiGraphs is isomorphic to existing DG.')
                for row in df.iterrows():
                    if DG.is_isomrphic(row.DiGraph):
                        raise ValueError('Two of the DiGraphs are isomorphic among themselves.')
            if normalize:
                DG = DG.normalize()
            df.loc[start_index + index_offset] = [DG.number_of_nodes(), DG.number_of_edges(), \
                                                  DG.is_strongly_connected, DG.is_prime, DG.adj_, DG]
        self.df = pd.concat([self.df, df])

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
            highest_num = max(self.df['number_of_nodes'])
        indices, query_df = self.find_row('(number_of_nodes == ' + str(highest_num) + ') & (is_prime == ' + str(True) + ')')
        return list(query_df.DiGraph)

    def isomorphic_graph_exists(self, DG):
        for _, row in self.df.iterrows():
            if DG.is_isomorphic(row.DiGraph):
                return True
        return False

    def save_object(self, filename):
        with open(filename+'._pickle', 'wb') as outp:
            pickle.dump(self, outp, -1)
        self.df.to_csv(filename+'.csv')
