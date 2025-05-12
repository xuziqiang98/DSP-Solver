import numpy as np

from abc import ABC, abstractmethod
from gurobipy import Model, GRB, quicksum

class SolverFactory:

    def get(id, adj) -> 'SolverBase':
        class_name = f'{id}Solver'
        try:
            SolverClass = globals()[class_name]
            return SolverClass(id, adj)
        except KeyError:
            raise NotImplementedError(f'{class_name} is not implemented')

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

class rDPSolver(SolverBase):
    
    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)

        # 创建变量
        self._n = len(adj)
        self._x = self.model.addVars(range(self._n), name="x", vtype=GRB.BINARY)
        self._y = self.model.addVars(range(self._n), name="y", vtype=GRB.BINARY)

        # 设置目标函数
        self.model.setObjective(quicksum(self._y[v] for v in range(self._n)), GRB.MINIMIZE)

        # 添加约束条件
        for v in range(self._n):
            if sum(adj[v]) == 0:
                self.model.addConstr(self._x[v] == 0, f"isolated_{v}")
                self.model.addConstr(self._y[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(self._n) if adj[v][u] == 1]
                self.model.addConstr(self._x[v] + self._y[v] == 1, f"v assigned to 0 or 1")
                self.model.addConstr(quicksum(self._y[u] for u in neighbors) >= self._x[v], f"dominated {v}")
                self.model.addConstr(quicksum(self._x[u] for u in neighbors) >= self._x[v], f"restrained {v}")
    
    def solve(self):
        # 求解模型
        self.model.optimize()

        # 获取结果
        dominating_set = [v for v in range(self._n) if self._y[v].X > 0.5]
        minimum_domination = self.model.ObjVal

        return dominating_set, minimum_domination

class MkDSolver(SolverBase):
    
    def __init__(self, id, adj) -> None:
        super().__init__(id, adj)

        # 创建变量
        # 在顶点数量为n的图上
        # X_v = 1 if f(v) = 1, X_v = 0 if f(v) != 1
        # Y_v = 1 if f(v) = 0, Y_v = 0 if f(v) != 0
        # Z_v = 1 if f(v) = -1, Z_v = 0 if f(v) != -1
        self._n = len(adj)
        self._x = self.model.addVars(range(self._n), name="x", vtype=GRB.BINARY)
        self._y = self.model.addVars(range(self._n), name="y", vtype=GRB.BINARY)
        self._z = self.model.addVars(range(self._n), name="z", vtype=GRB.BINARY)

        # 设置目标函数
        self.model.setObjective(quicksum(self._x[v] for v in range(self._n)) - quicksum(self._z[v] for v in range(self._n)), GRB.MINIMIZE)

        # 添加约束条件
        for v in range(self._n):
            # 确保每个顶点只有一个取值
            self.model.addConstr(self._x[v] + self._y[v] + self._z[v] == 1, f"v{v}_assigned_to_one_value")
            
            if sum(adj[v]) == 0:
                # k = 1
                self.model.addConstr(self._x[v] == 1, f"isolated_{v}")
            else:
                neighbors = [u for u in range(self._n) if adj[v][u] == 1]
                self.model.addConstr(self._x[v] - self._z[v] + quicksum(self._x[u] for u in neighbors) - quicksum(self._z[u] for u in neighbors) >= 1, f"dominate_{v}")
    
    def solve(self):
        # 求解模型
        self.model.optimize()

        # 检查约束条件是否满足
        for v in range(self._n):
            sum_values = self._x[v].X + self._y[v].X + self._z[v].X
            if abs(sum_values - 1.0) > 1e-5:  # 允许一定的数值误差
                print(f"警告：顶点 {v} 的取值和为 {sum_values}，应该为1")
            
            # 更严格的检查，确保只有一个变量接近1
            if (self._x[v].X > 0.5 and self._y[v].X > 0.5) or \
               (self._x[v].X > 0.5 and self._z[v].X > 0.5) or \
               (self._y[v].X > 0.5 and self._z[v].X > 0.5):
                print(f"错误：顶点 {v} 有多个取值: x={self._x[v].X}, y={self._y[v].X}, z={self._z[v].X}")

        # 获取结果，使用更严格的判断条件
        vertices_one = [v for v in range(self._n) if self._x[v].X > 0.9]  # 使用更高的阈值
        vertices_zero = [v for v in range(self._n) if self._y[v].X > 0.9]
        vertices_neg = [v for v in range(self._n) if self._z[v].X > 0.9]
        
        # 处理边界情况
        for v in range(self._n):
            values = [self._x[v].X, self._y[v].X, self._z[v].X]
            max_value = max(values)
            max_index = values.index(max_value)
            
            # 如果最大值不够明确，则根据最大值分配
            if max_value < 0.9 and max_value > 0.5:
                if max_index == 0 and v not in vertices_one:
                    vertices_one.append(v)
                elif max_index == 1 and v not in vertices_zero:
                    vertices_zero.append(v)
                elif max_index == 2 and v not in vertices_neg:
                    vertices_neg.append(v)
        
        dominating_set = [vertices_one, vertices_zero, vertices_neg]
        minimum_domination = self.model.ObjVal
        
        return dominating_set, minimum_domination