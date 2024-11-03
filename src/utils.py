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