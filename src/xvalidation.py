import numpy as np

from abc import ABC, abstractmethod
from gurobipy import Model, GRB, quicksum
from src.utils import postorder_traversal, find_parents, GraphType

validation_dict = {'rDP':[GraphType.TREE], 'RDRDP':[GraphType.TREE]}

class ValidationFactory:

    def get(self, id, adj) -> 'ValidationBase':
        class_name = f'{id}Validation'
        try:
            ValidationClass = globals()[class_name]
            return ValidationClass(adj)
        except KeyError:
            raise NotImplementedError(f'{class_name} is not implemented')

class ValidationBase(ABC):
    
    def __init__(self, adj) -> None:
        self.adj = adj
    
    @abstractmethod
    def solve(self):
        pass

class rDPValidation(ValidationBase):
    
    def __init__(self, adj) -> None:
        super().__init__(adj)
        self.n = len(self.adj)
        self.dynamic_table = [[float('inf')] * self.n for _ in range(4)]
        for i in range(4):
            for j in range(self.n):
                if i == 0:
                    self.dynamic_table[i][j] = 1
                elif i == 3:
                    self.dynamic_table[i][j] = 0
        self.tree_order = postorder_traversal(self.adj)
        self.root = self.tree_order[-1]
        self.parents = find_parents(self.adj, self.tree_order)
    
    def solve(self):
        for i, j in enumerate(self.tree_order[:-1]):
            k = self.parents[i]
            self.dynamic_table[0][k] = min(self.dynamic_table[0][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[3][j])
            self.dynamic_table[1][k] = self.dynamic_table[1][k] + self.dynamic_table[0][j]
            self.dynamic_table[2][k] = min(self.dynamic_table[1][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[1][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[0][j])
            self.dynamic_table[3][k] = min(self.dynamic_table[3][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[2][j])
        return None, min(self.dynamic_table[0][self.root], self.dynamic_table[2][self.root])

class RDRDPValidation(ValidationBase):

    def __init__(self, adj) -> None:
        self.adj = adj
        super().__init__(adj)
        self.n = len(self.adj)
        self.dynamic_table = [[float('inf')] * self.n for _ in range(10)]
        for i in range(10):
            for j in range(self.n):
                if i == 1:
                    self.dynamic_table[i][j] = 1
                elif i == 2:
                    self.dynamic_table[i][j] = 2
                elif i == 3:
                    self.dynamic_table[i][j] = 3
                elif i == 8:
                    self.dynamic_table[i][j] = 0
        self.tree_order = postorder_traversal(self.adj)
        self.root = self.tree_order[-1]
        self.parents = find_parents(self.adj, self.tree_order)

    def solve(self):
        for i, j in enumerate(self.tree_order[:-1]):
            k = self.parents[i]
            self.dynamic_table[0][k] = min(self.dynamic_table[0][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[0][k] + self.dynamic_table[5][j],
                                           self.dynamic_table[5][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[5][k] + self.dynamic_table[5][j],
                                           self.dynamic_table[6][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[7][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[7][k] + self.dynamic_table[3][j])
            self.dynamic_table[1][k] = min(self.dynamic_table[1][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[1][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[1][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[1][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[4][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[4][k] + self.dynamic_table[3][j])
            self.dynamic_table[2][k] = min(self.dynamic_table[2][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[4][j],
                                           self.dynamic_table[2][k] + self.dynamic_table[7][j])
            self.dynamic_table[3][k] = min(self.dynamic_table[3][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[4][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[6][j],
                                           self.dynamic_table[3][k] + self.dynamic_table[7][j])
            self.dynamic_table[4][k] = min(self.dynamic_table[4][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[4][k] + self.dynamic_table[1][j])
            self.dynamic_table[5][k] = min(self.dynamic_table[5][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[5][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[5][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[8][k] + self.dynamic_table[3][j],
                                           self.dynamic_table[9][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[9][k] + self.dynamic_table[3][j])
            self.dynamic_table[6][k] = min(self.dynamic_table[6][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[6][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[6][k] + self.dynamic_table[5][j],
                                           self.dynamic_table[8][k] + self.dynamic_table[5][j])
            self.dynamic_table[7][k] = min(self.dynamic_table[6][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[7][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[7][k] + self.dynamic_table[1][j],
                                           self.dynamic_table[7][k] + self.dynamic_table[5][j],
                                           self.dynamic_table[9][k] + self.dynamic_table[0][j],
                                           self.dynamic_table[9][k] + self.dynamic_table[5][j])
            self.dynamic_table[8][k] = self.dynamic_table[8][k] + self.dynamic_table[1][j]
            self.dynamic_table[9][k] = min(self.dynamic_table[8][k] + self.dynamic_table[2][j],
                                           self.dynamic_table[9][k] + self.dynamic_table[1][j])
        return None, min(self.dynamic_table[0][self.root], self.dynamic_table[1][self.root],
                         self.dynamic_table[2][self.root], self.dynamic_table[3][self.root])