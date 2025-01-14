import path_setup
from src.graph import RandomDenseGraph
from src.configs.common_configs import PathConfig
from src.utils import save_mtx
import numpy as np

data_path = PathConfig().data / 'DENSE'

dens = 0.6
turn = 50
for i in range(turn):
    order = np.random.randint(160, 240)
    graph = RandomDenseGraph(order, dens)
    graph_adj = graph.get()
    graph_file = data_path / f'DENSE-{i}.mtx'
    # 保存为mtx文件
    save_mtx(graph_file, graph_adj)
    print(f'Saved {graph_file} with order {order}.')