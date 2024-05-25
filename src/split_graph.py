import scripts.path_setup
import random
import numpy as np

from typing import List
from .graph import Graph

class SplitGraph(Graph):

    def __init__(self, graph_type, num_vertices) -> None:
        super().__init__(graph_type, num_vertices)
        self._adj = self.graph2adj()

    # split the graph into a clique and an independent set
    def split2part(self) -> None:    
        random_integer = random.randint(1, self.num_vertices-1)
        self._clique = random_integer
        self._independent_set = self.num_vertices - random_integer
    
    # return the adjacency matrix of the split graph
    def graph2adj(self) -> np.ndarray:
        self.split2part()
        adj = [[0 for _ in range(self.num_vertices)] for _ in range(self.num_vertices)]
        # vertices in the clique are connected
        for i in range(self._clique):
            for j in range(i+1, self._clique):
                adj[i][j] = 1
                adj[j][i] = 1
        # vertices in the independent set are not connected
        for i in range(self._clique, self.num_vertices):
            for j in range(i+1, self.num_vertices):
                adj[i][j] = 0
                adj[j][i] = 0
        # the edges between the clique and the independent set are randomly connected
        # but each vertex in the independent set is at least connected to one vertex in the clique
        for i in range(self._clique, self.num_vertices):
            for j in range(self._clique):
                adj[i][j] = random.randint(0, 1)
                adj[j][i] = adj[i][j]
            # if the vertex in the independent set is not connected to any vertex in the clique
            # then it is connected to a random vertex in the clique
            if sum(adj[i][:self._clique]) == 0:
                j = random.randint(0, self._clique-1)
                adj[i][j] = 1
                adj[j][i] = 1
            # if the vertex in the independent set is connected to all vertices in the clique
            # then it is not connected to a random vertex in the clique
            if self._clique is not 1:
                while sum(adj[i][:self._clique]) == self._clique:
                    j = random.randint(0, self._clique-1)
                    adj[i][j] = 0
                    adj[j][i] = 0
        return np.array(adj)
    
    def get_adj(self) -> np.ndarray:
        return self._adj
    
    def get_clique(self) -> int:
        return self._clique
    
    # return the maximum degree of the split graph
    def get_max_degree(self) -> int:
        return max([sum(self._adj[i]) for i in range(self.num_vertices)])
    
    def get_independent_set(self) -> int:  
        return self._independent_set
    
    # save the adjacency matrix of the split graph to a .csv file
    def save2file(self, path) -> None:
        adj = self._adj
        np.savetxt(path, adj, delimiter=',', fmt='%d')

    def __repr__(self) -> str:
        return (f'SplitGraph({self.graph_type}, {self.num_vertices})')
    
    def __str__(self) -> str:
        return (f'SplitGraph({self.graph_type}, {self.num_vertices}): '
                f'clique = {self._clique}, independent set = {self._independent_set}')
