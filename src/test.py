import gurobipy
import numpy as np
import pyscipopt as scip

class GurobiSolver():
    
    def __init__(self, matrix) -> None:
        self.model = gurobipy.Model('DSP')
        self.matrix = matrix

        # 创建变量
        n = matrix.shape[0]
        x = self.model.addVars(range(n), name="x", vtype=gurobipy.GRB.BINARY)

        # 设置目标函数
        self.model.setObjective(gurobipy.quicksum(x[v] for v in range(n)), gurobipy.GRB.MINIMIZE)

        # 添加约束条件
        for v in range(n):
            if sum(matrix[v]) == 0:
                self.model.addConstr(x[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(n) if matrix[v][u] == 1]
                self.model.addConstr(x[v] + gurobipy.quicksum(x[u] for u in neighbors) >= 1, f"dominate_{v}")
    
    def solve(self):
        # 求解模型
        self.model.setParam('TimeLimit', 45)
        self.model.optimize()
        
class SCIPSolver():
    
    def __init__(self, matrix) -> None:
        self.model = scip.Model("DSP")
        self.matrix = matrix

        # Define variables
        n = matrix.shape[0]
        x = {}
        for i in range(n):
            x[i] = self.model.addVar(vtype="B", name=f"x_{i}")
        
        # Define constraints
        for v in range(n):
            if np.sum(matrix[v]) == 0:  # Check for isolated nodes
                self.model.addCons(x[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(n) if matrix[v][u] == 1]
                self.model.addCons(x[v] + scip.quicksum(x[u] for u in neighbors) >= 1, f"dominate_{v}")
        
        # Define objective
        self.model.setObjective(scip.quicksum(x[v] for v in range(n)), sense="minimize")
    
    def solve(self):
        # 求解模型
        self.model.setParam("limits/time", 45)
        self.model.optimize()
        ub = self.model.getPrimalbound()
        lb = self.model.getDualbound()
        # 用百分数表示gap
        gap = (ub - lb) / ub * 100
        return gap