import scripts.path_setup
import abc
import numpy as np

from typing import List

class Graph(abc.ABC):
    
    def __init__(self, graph_type, num_vertices) -> None:
        self.graph_type = graph_type
        self.num_vertices = num_vertices

    @abc.abstractmethod
    def graph2adj(self) -> np.ndarray:
        pass

    @abc.abstractmethod
    def get_adj(self) -> np.ndarray:
        pass

    @abc.abstractmethod
    def save2file(self, path) -> None:
        pass
    
    @abc.abstractmethod
    def file2adj(path) -> np.ndarray:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass



    