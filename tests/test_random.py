import path_setup
import numpy as np

from src.utils import GraphType, save_mtx
from src.graph import GraphFactory, RandomDenseGraph
from src.test import GurobiSolver, SCIPSolver
from src.env import make
from src.configs.common_configs import PathConfig

graph = 'RANDOM'
# order = 200
# problem = 'DSP'
graph_type = GraphType[graph]
graph_factory = GraphFactory()
# graph = graph_factory.get(graph_type, order)
# graph_adj = graph.get()

# env = make(problem, graph_adj)
# gurobi = GurobiSolver(graph_adj)
# scip = SCIPSolver(graph_adj)

# print('[+] Solve the problem with Gurobi:')
# gurobi.solve()
# print('\n\n[+] Solve the problem with SCIP:')
# scip.solve()

counter700 = 1
counter800 = 1
counter900 = 1
counter1000 = 1
counter1100 = 1

for _ in range(50):
    order = np.random.randint(160, 240)
    graph = graph_factory.get(graph_type, order)
    matrix = graph.get()
    data_dir = PathConfig().data / 'RANDOM'
    if order <= 799:
        mtx_file = f'RANDOM-700-{counter700}.mtx'
        counter700 += 1
    elif order in range(800, 899):
        mtx_file = f'RANDOM-800-{counter800}.mtx'
        counter800 += 1
    elif order in range(900, 999):
        mtx_file = f'RANDOM-900-{counter900}.mtx'
        counter900 += 1
    else:
        mtx_file = f'RANDOM-1000-{counter1000}.mtx'
        counter1000 += 1
    mtx_path = data_dir / mtx_file
    save_mtx(mtx_path, matrix)
    print(f'Saved {mtx_file} with order {order}.')