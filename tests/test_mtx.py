import path_setup
import numpy as np
from src.configs.common_configs import PathConfig
from src.utils import read_mtx as new_read_mtx

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

data_dir = PathConfig().data
mtx_file = 'johnson8-2-4.mtx'
mtx_path = data_dir / 'DIMACS' / mtx_file

print('Old read_mtx:')
print(read_mtx(mtx_path))

print('New read_mtx:')
print(new_read_mtx(mtx_path))