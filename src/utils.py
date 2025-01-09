import inspect
# import torch
import random

import numpy as np

from types import MethodType, FunctionType
from pathlib import Path
from enum import Enum


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


def read_mtx(file_path: str) -> np.ndarray:
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # 跳过第一行（以%%开头的那行）
        data_lines = lines[1:]
        # 从第二行获取矩阵的行数和列数（假设格式相对简单，第二行是类似'3 3'表示3行3列这样的格式）
        n_rows, n_cols, _ = map(int, data_lines[0].split())
        adj_matrix = np.zeros((n_rows, n_cols), dtype=int)
        for line in data_lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                u, v = map(int, parts[:2])
                # 添加索引范围验证，避免越界
                if 1 <= u <= n_rows and 1 <= v <= n_cols:
                    adj_matrix[u - 1][v - 1] = 1
                    if n_rows == n_cols:  # 处理无向图情况，保证对称
                        adj_matrix[v - 1][u - 1] = 1
    return adj_matrix
    
# 获取指定文件夹下的所有文件
def get_files(path: str) -> list[str]:
    return [str(file) for file in Path(path).iterdir()]