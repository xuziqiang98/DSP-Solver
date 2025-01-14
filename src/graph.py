import scripts.path_setup
import abc
import random

import numpy as np
import networkx as nx

from typing import List
from abc import ABC, abstractmethod
from src.utils import GraphType
from math import ceil, floor
from random import randint

class GraphFactory:
    
    def get(self, type, n_vertices: int, *args) -> 'GraphBase':
        # if type == GraphType.RANDOM:
        #     return RandomGraph(n_vertices, *args)
        # elif type == GraphType.SPLIT:
        #     return SplitGraph(n_vertices, *args)
        # elif type == GraphType.ER:
        #     return ErdosRenyiGraph(n_vertices, *args)
        # elif type == GraphType.BA:
        #     return BarabasiAlbertGraph(n_vertices, *args)
        # elif type == GraphType.REGULAR:
        #     return RegularGraph(n_vertices, *args)
        # elif type == GraphType.WS:
        #     return WattsStrogatzGraph(n_vertices, *args)
        # else:
        #     raise NotImplementedError()
        class_name = type.name.capitalize() + 'Graph'
        try:
            GraphClass = globals()[class_name]
            return GraphClass(n_vertices, *args)
        except KeyError:
            raise NotImplementedError(f'{class_name} is not implemented')

class GraphBase(ABC):

    def __init__(self, n_vertices) -> None:
        self.n_vertices = n_vertices

    @abstractmethod
    def get(self) -> np.ndarray:
        raise NotImplementedError

class RandomGraph(GraphBase):
    '''
    Attributes:
        self.get_w (lambda): get the weight of the edge
    '''
    def __init__(self, n_vertices) -> None:
        '''
        Attributes:
            n_vertices (int): number of vertices
        '''
        super().__init__(n_vertices)
        
        self.get_w = lambda : np.random.choice([0, 1])

    def get(self) -> np.ndarray:
        '''
        Attributes:
            n (int): number of vertices
            density (float): edge density
            
        Returns:
            matrix (np.ndarray): adjacency matrix
        '''
        n = self.n_vertices
        density = np.random.uniform()
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i):
                if np.random.uniform() < density:
                    w = self.get_w()
                    matrix[i, j] = w
                    matrix[j, i] = w

        return matrix

class ErdosRenyiGraph(GraphBase):

    def __init__(self, n_vertices=20, p_connection=[0.1,0]):
        '''
        Args:
            n_vertices (int): number of vertices
            p_connection (list): mean and standard deviation of the edge probability
            
        Attributes:
            self.get_connection_mask (lambda): get the connection mask
        '''    
        super().__init__(n_vertices)

        if type(p_connection) not in [list,tuple]:
            p_connection = [p_connection, 0]
        assert len(p_connection)==2, "p_connection must have length 2"
        self.p_connection  = p_connection

        # def get_connection_mask():
        #     mask = 1. * np.random.randint(2, size=(self.n_vertices, self.n_vertices))
        #     mask = np.tril(mask) + np.triu(mask.T, 1)
        #     return mask
        
        # self.get_connection_mask = get_connection_mask

    def get(self) -> np.ndarray:

        p = np.clip(np.random.normal(*self.p_connection),0,1)

        g = nx.erdos_renyi_graph(self.n_vertices, p)
        # adj = np.multiply(nx.to_numpy_array(g), self.get_connection_mask())

        # No self-connections (this modifies adj in-place).
        # np.fill_diagonal(adj, 0)

        return nx.to_numpy_array(g)

class BarabasiAlbertGraph(GraphBase):

    def __init__(self, n_vertices=20, m_insertion_edges=4) -> np.ndarray:
        super().__init__(n_vertices)

        self.m_insertion_edges = m_insertion_edges

        # def get_connection_mask():
        #     mask = 1. * np.random.randint(2, size=(self.n_vertices, self.n_vertices))
        #     mask = np.tril(mask) + np.triu(mask.T, 1)
        #     return mask
        
        # self.get_connection_mask = get_connection_mask

    def get(self) -> np.ndarray:

        g = nx.barabasi_albert_graph(self.n_vertices, self.m_insertion_edges)
        # adj = np.multiply(nx.to_numpy_array(g), self.get_connection_mask())

        # No self-connections (this modifies adj in-place).
        # np.fill_diagonal(adj, 0)

        return nx.to_numpy_array(g)
    
class RegularGraph(GraphBase):

    def __init__(self, n_vertices=20, d_node=[2,0]):
        super().__init__(n_vertices)

        if type(d_node) not in [list,tuple]:
            d_node = [d_node, 0]
        assert len(d_node)==2, "k_neighbours must have length 2"
        self.d_node  = d_node

        # def get_connection_mask():
        #     mask = 1. * np.random.randint(2, size=(self.n_vertices, self.n_vertices))
        #     mask = np.tril(mask) + np.triu(mask.T, 1)
        #     return mask
        # self.get_connection_mask = get_connection_mask

    def get(self) -> np.ndarray:
        k = np.clip(int(np.random.normal(*self.d_node)),0,self.n_vertices)

        g = nx.random_regular_graph(k, self.n_vertices)
        # adj = np.multiply(nx.to_numpy_array(g), self.get_connection_mask())

        return nx.to_numpy_array(g)
    
class WattsStrogatzGraph(GraphBase):

    def __init__(self, n_vertices=20, k_neighbours=[2,0]):
        super().__init__(n_vertices)

        if type(k_neighbours) not in [list,tuple]:
            k_neighbours = [k_neighbours, 0]
        assert len(k_neighbours)==2, "k_neighbours must have length 2"
        self.k_neighbours  = k_neighbours

        # def get_connection_mask():
        #     mask = 1. * np.random.randint(2, size=(self.n_vertices, self.n_vertices))
        #     mask = np.tril(mask) + np.triu(mask.T, 1)
        #     return mask
        # self.get_connection_mask = get_connection_mask

    def get(self, with_padding=False):
        k = np.clip(int(np.random.normal(*self.k_neighbours)),0,self.n_vertices)

        g = nx.watts_strogatz_graph(self.n_vertices, k, 0)
        # adj = np.multiply(nx.to_numpy_array(g), self.get_connection_mask())

        return nx.to_numpy_array(g)
    
class SplitGraph(GraphBase):
    def __init__(self, n_vertices:int = 20, clique_size:int = 10, independent_set_size:int = 10, edge_probability: float = 0.5) -> None:
        super().__init__(n_vertices)
        
        self.clique_size = clique_size
        self.independent_set_size = independent_set_size
        
        if clique_size + independent_set_size != n_vertices:
        #     raise ValueError("clique_size + independent_set_size must be equal to n_vertices")
        # if clique_size < 0 or independent_set_size < 0:
        #     raise ValueError("clique_size and independent_set_size must be non-negative")
        # if clique_size is None or independent_set_size is None:
            self.clique_size = randint(0, n_vertices)
            self.independent_set_size = n_vertices - self.clique_size

        self.edge_probability = edge_probability
        
    def get(self) -> np.ndarray:
        G = nx.Graph()
        
        # add clique nodes
        clique_nodes = range(self.clique_size)
        G.add_nodes_from(clique_nodes)
        
        # add edges to the clique
        for i in clique_nodes:
            for j in clique_nodes:
                if i < j:
                    G.add_edge(i, j)
        
        # add independent set nodes
        independent_nodes = range(self.clique_size, self.clique_size + self.independent_set_size)
        G.add_nodes_from(independent_nodes)
        
        # add edges between clique and independent set by edge_probability
        for i in clique_nodes:
            for j in independent_nodes:
                if np.random.rand() < self.edge_probability:
                    G.add_edge(i, j)

        return nx.to_numpy_array(G)
    
class TreeGraph(GraphBase):
    def __init__(self, n_vertices:int = 20) -> None:
        super().__init__(n_vertices)
        
    def get(self) -> np.ndarray:
        G = nx.random_tree(self.n_vertices)
        
        return nx.to_numpy_array(G)

# 顶点带权重的随机图
class RandomWeightedGraph(GraphBase):
    def __init__(self, n_vertices:int = 20) -> None:
        super().__init__(n_vertices)
        
    def get(self) -> np.ndarray:
        G = nx.Graph()
        for i in range(self.n_vertices):
            G.add_node(i)
        for i in range(self.n_vertices):
            for j in range(i + 1, self.n_vertices):
                G.add_edge(i, j, weight=randint(1, 10))
        
        return nx.to_numpy_array(G)

# 生成随机的无权稠密图
class RandomDenseGraph(GraphBase):
    """
    n_vertices: 顶点数
    density: 图的密度
    """
    def __init__(self, n_vertices:int = 20, density:float = 0.6) -> None:
        super().__init__(n_vertices)
        self.density = density
        
    def get(self) -> np.ndarray:
        G = nx.dense_gnm_random_graph(self.n_vertices, ceil(self.n_vertices * (self.n_vertices - 1) * self.density / 2))
        
        return nx.to_numpy_array(G)