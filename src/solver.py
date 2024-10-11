import numpy as np

from abc import ABC, abstractmethod
from gurobipy import Model, GRB, quicksum

class SolverFactory:

    def get(id, adj) -> 'SolverBase':
        if id == "DSP":
            return DSPSolver(id, adj)
        elif id == "RDP":
            return RDPSolver(id, adj)
        elif id == "IRDP":
            return IRDPSolver(id, adj)
        elif id == "RDRDP":
            return RDRDPSolver(id,adj)
        else:
            raise NotImplementedError()

class SolverBase(ABC):
    
    def __init__(self, id, adj) -> None:
        self.model = Model(id)
        self.adj = adj
    
    @abstractmethod
    def solve(self):
        pass

class DSPSolver(SolverBase):
    
    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)

        # 创建变量
        self._n = len(adj)
        self._x = self.model.addVars(range(self._n), name="x", vtype=GRB.BINARY)

        # 设置目标函数
        self.model.setObjective(quicksum(self._x[v] for v in range(self._n)), GRB.MINIMIZE)

        # 添加约束条件
        for v in range(self._n):
            if sum(adj[v]) == 0:
                self.model.addConstr(self._x[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(self._n) if adj[v][u] == 1]
                self.model.addConstr(self._x[v] + quicksum(self._x[u] for u in neighbors) >= 1, f"dominate_{v}")
    
    def solve(self):
        # 求解模型
        self.model.optimize()

        # 获取结果
        dominating_set = [v for v in range(self._n) if self._x[v].X > 0.5]
        minimum_domination = self.model.ObjVal

        return dominating_set, minimum_domination

class RDPSolver(SolverBase):
    
    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)
        
    def solve(self):
        pass
    
class IRDPSolver(SolverBase):
        
    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)
        
    def solve(self):
        pass


class RDRDPSolver(SolverBase):

    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)

        # 创建变量
        self._n = len(adj)
        self._x = self.model.addVars(range(self._n), name="x", vtype=GRB.BINARY)
        self._y = self.model.addVars(range(self._n), name="y", vtype=GRB.BINARY)
        self._z = self.model.addVars(range(self._n), name="z", vtype=GRB.BINARY)
        # 设置目标函数
        self.model.setObjective(quicksum(self._x[v] for v in range(self._n))+ 2 * quicksum(self._y[v] for v in range(self._n)) + 3 * quicksum(self._z[v] for v in range(self._n)), GRB.MINIMIZE)
        # 添加约束条件
        for v in range(self._n):
            if sum(adj[v]) == 0:
                self.model.addConstr(self._y[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(self._n) if adj[v][u] == 1]
                self.model.addConstr(self._x[v] + self._y[v] + self._z[v] + 0.5 * quicksum(self._y[u] for u in neighbors) + quicksum(self._z[u] for u in neighbors) >= 1, f"dominate_{v}")
                self.model.addConstr(quicksum(self._y[u] for u in neighbors) + quicksum(self._z[u] for u in neighbors) >= self._x[v], f"dominate_{v}")
                self.model.addConstr(self._x[v] + self._y[v] + self._z[v] <= 1, f"dominate_{v}")
                self.model.addConstr(self._x[v] + self._y[v] + self._z[v] + quicksum(1 - self._x[u] - self._y[u] - self._z[u] for u in neighbors) >= 1, f"dominate_{v}")
    def solve(self):
        '''
        Returns:
            dominating_set(List[List]):
            minimum_domination(int):
        '''
        # 求解模型
        self.model.optimize()

        # 获取结果
        vertices_one = [v for v in range(self._n) if self._x[v].X > 0.5]
        vertices_two = [v for v in range(self._n) if self._y[v].X > 0.5]
        vertices_three = [v for v in range(self._n) if self._z[v].X > 0.5]
        dominating_set = [vertices_one, vertices_two, vertices_three]
        minimum_domination = self.model.ObjVal

        return dominating_set, minimum_domination
