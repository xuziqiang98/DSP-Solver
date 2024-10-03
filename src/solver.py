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