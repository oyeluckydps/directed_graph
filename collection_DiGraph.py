import networkx as nx
from pickle_large_objects import StreamingPickler
import warnings
import pandas as pd
from pathlib import Path

import extended_DiGraph as edg
from utils import time_block

def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)

def load_object(filename, number_of_objects = 1):
    if number_of_objects == 1:
        return StreamingPickler.load_in_chunks(filename+'._pickle')
    else:
        object_list = []
        for i in range(number_of_objects):
            object_list.append(StreamingPickler.load_in_chunks(filename))
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
        self.hash_dict = dict()

    @property
    def df(self):
        '''
        Make a df out of self.DGs using vectorized operations
        :return: pandas DataFrame containing graph information
        '''
        # Create a dictionary of lists for all columns
        data = {
            'isomorphic_hash': self.DG_isophorm_hash,
            'number_of_nodes': self.number_of_nodes,
            'number_of_edges': [DG.number_of_edges() for DG in self.DGs],
            'is_strongly_connected': [DG.is_strongly_connected for DG in self.DGs],
            'is_prime': [DG.is_prime for DG in self.DGs],
            'adj_': [DG.adj_ for DG in self.DGs],
            'DiGraph': self.DGs
        }

        # Create DataFrame in one go
        return pd.DataFrame(data)

    def add_DGs(self, DGs, normalize = False, check_against_isomorphism = False):
        for DG in DGs:
            if check_against_isomorphism:
                if self.isomorphic_graph_exists(DG):
                    continue
            if normalize:
                DG = DG.normalize()
            self.DGs.append(DG)
            self.number_of_nodes.append(DG.number_of_nodes())
            DG_hash = DG.isophorm_hash
            self.DG_isophorm_hash.append(DG_hash)
            if DG_hash in self.hash_dict.keys():
                self.hash_dict[DG_hash].append(len(self.DGs)-1)
            else:
                self.hash_dict[DG_hash] = [len(self.DGs)-1]

    def find_row(self, query):
        df = self.df.query(query)
        if len(df.index) == 0:
            warnings.warn("No match found for query!")
        elif len(df.index) > 1:
            warnings.warn("Multiple matches found for the query!")
            return (df.index, df)
        else:
            return (df.index[0], df)

    def list_of_computed_DGs(self, num = None):
        if num is None:
            num = max(self.number_of_nodes)
        return [DG for DG, n_nodes in zip(self.DGs, self.number_of_nodes) if n_nodes==num]

    def count_of_computed_DGs(self, num = None):
        if num is None:
            num = max(self.number_of_nodes)
        return self.number_of_nodes.count(num)

    def isomorphic_graph_exists(self, DG2):
        with time_block("isomorphic_graph_exists: Calculating Hash"):
            DG2_hash = DG2.isophorm_hash
        with time_block("isomorphic_graph_exists: Hash exists in list"):
           flag1 = DG2_hash in self.hash_dict.keys()
        if flag1:
            for index in self.hash_dict[DG2_hash]:
                if DG2.is_isomorphic(self.DGs[index]):
                    return True
        return False

    def save_object(self, filename, path_prefix = ''):
        StreamingPickler.save_in_chunks(self, Path(path_prefix) / Path(filename+'._pickle'))
        self.df.to_csv(filename+'.csv')
