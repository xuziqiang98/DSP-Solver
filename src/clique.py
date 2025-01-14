import numpy as np
import networkx as nx
import pyscipopt as scip
import gurobipy

def SCIPSolver(adj_matrix: np.ndarray):
    """
    从邻接矩阵求解最大团问题的整数规划模型。

    参数:
    adj_matrix: np.ndarray，邻接矩阵，表示无向图。邻接矩阵中的元素为1表示存在边，0表示不存在边。

    返回:
    最大团的大小和成员。
    """
    # 获取图的顶点数量
    n_vertices = adj_matrix.shape[0]
    
    # 创建 NetworkX 图对象
    G = nx.Graph()
    G.add_nodes_from(range(n_vertices))

    # 根据邻接矩阵添加边
    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if adj_matrix[i, j] == 1:
                G.add_edge(i, j)

    # 创建 SCIP 模型
    model = scip.Model("Maximum Clique")
    
    # 创建决策变量 x_i（是否包含顶点 i）
    x = {v: model.addVar(vtype="B", name=f"x_{v}") for v in range(n_vertices)}
    
    # 目标函数：最大化选中的顶点数（即最大团的大小）
    model.setObjective(sum(x[v] for v in range(n_vertices)), "maximize")
    
    # 添加约束：对于每一对不相邻的顶点 i 和 j，不能同时选中这两个顶点
    for i, j in nx.non_edges(G):  # 获取图中所有不相邻的顶点对
        model.addCons(x[i] + x[j] <= 1)
    
    # 求解模型
    model.setParam("limits/time", 45)
    model.optimize()
    
    # 获取最优解
    if model.getStatus() == "optimal":
        clique = [v for v in range(n_vertices) if model.getVal(x[v]) > 0.5]  # 获取属于团的顶点
        clique_size = len(clique)
        return clique_size, clique
    else:
        print("No optimal solution found.")
        return None, None

def GurobiSolver(adj_matrix: np.ndarray):
    """
    从邻接矩阵求解最大团问题的整数规划模型。
    
    参数:
    adj_matrix: np.ndarray，邻接矩阵，表示无向图。邻接矩阵中的元素为1表示存在边，0表示不存在边。

    返回:
    最大团的大小和成员。
    """
    # 获取图的顶点数量
    n_vertices = adj_matrix.shape[0]
    
    # 创建 NetworkX 图对象
    G = nx.Graph()
    G.add_nodes_from(range(n_vertices))

    # 根据邻接矩阵添加边
    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if adj_matrix[i, j] == 1:
                G.add_edge(i, j)

    # 创建 Gurobi 模型
    model = gurobipy.Model("Maximum Clique")

    # 创建决策变量 x_i（是否包含顶点 i）
    x = {v: model.addVar(vtype=gurobipy.GRB.BINARY, name=f"x_{v}") for v in range(n_vertices)}
    
    # 设置目标函数：最大化选中的顶点数（即最大团的大小）
    model.setObjective(sum(x[v] for v in range(n_vertices)), gurobipy.GRB.MAXIMIZE)
    
    # 添加约束：对于每一对不相邻的顶点 i 和 j，不能同时选中这两个顶点
    for i, j in nx.non_edges(G):  # 获取图中所有不相邻的顶点对
        model.addConstr(x[i] + x[j] <= 1)

    # 求解模型
    model.setParam('TimeLimit', 45)
    model.optimize()
    
    # 获取最优解
    if model.status == gurobipy.GRB.OPTIMAL:
        clique = [v for v in range(n_vertices) if x[v].x > 0.5]  # 获取属于团的顶点
        clique_size = len(clique)
        return clique_size, clique
    else:
        print("No optimal solution found.")
        return None, None
