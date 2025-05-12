import inspect
# import torch
import random

import numpy as np

from types import MethodType, FunctionType
from pathlib import Path
from enum import Enum
from scipy.io import mmread, mmwrite
from scipy.sparse import csr_matrix


class OptimizationTarget(Enum):
    
    # Dominating Set Problem
    DSP = 1
    # Roman Domination Problem
    RDP = 2
    # Independent Roman Domination Problem
    IRDP = 3
    # Restrained Double Roman Domination Problem
    RDRDP = 4
    # restrained Domination Problem
    rDP = 5
    # Minus k-Dominating Set Problem
    MkD = 6

class GraphType(Enum):
    
    # Random Graph
    RANDOM = 1
    # Split Graph
    SPLIT = 2
    # Erdos Renyi Graph
    ER = 3
    # Barabasi Albert Graph
    BA = 4
    # Regular Graph
    REGULAR = 5
    # Watts Strogatz Graph
    WS = 6
    # Ramdom Connected Tree
    TREE = 7

# def enable_grad_for_hf_llm(func: MethodType | FunctionType) -> MethodType | FunctionType:
#     return func.__closure__[1].cell_contents


def get_script_name() -> str:
    caller_frame_record = inspect.stack()[1]
    module_path = caller_frame_record.filename
    return Path(module_path).stem

def postorder_traversal(adj_matrix):
    n = len(adj_matrix)  # 节点数
    visited = [False] * n
    postorder = []

    def dfs(node):
        visited[node] = True
        for neighbor, is_connected in enumerate(adj_matrix[node]):
            if is_connected and not visited[neighbor]:
                dfs(neighbor)
        postorder.append(node)
    
    # 假设从节点0开始遍历（树的根节点）
    dfs(0)

    return postorder

def find_parents(adj_matrix, postorder):
    n = len(adj_matrix)
    parent = [-1] * n  # 初始化父节点数组，-1 表示无父节点

    for idx, node in enumerate(postorder):
        neighbors = [u for u in range(n) if adj_matrix[node][u] == 1]
        for p in postorder[idx + 1:]:
            if p in neighbors:
                parent[idx] = p
                break

    return parent

import numpy as np


def read_mtx(file_path):
    """
    读取无向图的 .mtx 文件并返回邻接矩阵的 np.ndarray 格式。

    :param file_path: str, .mtx 文件路径
    :return: np.ndarray, 邻接矩阵
    """
    # 读取 .mtx 文件为稀疏矩阵
    sparse_matrix = mmread(file_path)
    
    # 确保是无向图（矩阵对称）
    adjacency_matrix = sparse_matrix + sparse_matrix.T
    
    # 转换为 NumPy 的邻接矩阵格式
    adjacency_matrix = adjacency_matrix.toarray()
    
    # 将非零元素设置为 1（表示无权图）
    adjacency_matrix[adjacency_matrix != 0] = 1.

    return adjacency_matrix
    
# 获取指定文件夹下的所有文件
def get_files(path: str) -> list[str]:
    return [str(file) for file in Path(path).iterdir()]

def save_mtx(file_path: str, adj_matrix: np.ndarray):
    """
    将邻接矩阵保存为 .mtx 文件。

    :param file_path: str, 保存路径
    :param adj_matrix: np.ndarray, 邻接矩阵
    """
    # 将邻接矩阵转换为稀疏矩阵
    sparse_matrix = csr_matrix(adj_matrix)
    
    # 保存为 .mtx 文件
    mmwrite(file_path, sparse_matrix)
    