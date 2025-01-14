import path_setup
from src.clique import SCIPSolver, GurobiSolver
import numpy as np
from src.draw_graph import DrawGraph
from src.graph import GraphFactory, RandomDenseGraph
from src.utils import GraphType

# adj_matrix = np.array([
#         [0, 1, 1, 0, 0],
#         [1, 0, 1, 1, 0],
#         [1, 1, 0, 1, 1],
#         [0, 1, 1, 0, 1],
#         [0, 0, 1, 1, 0]
#     ])

# graph = 'RANDOM'
order = 180
dens = 0.6
# graph_type = GraphType[graph]
# graph_factory = GraphFactory()
# graph = graph_factory.get(graph_type, order)
graph = RandomDenseGraph(order, dens)
graph_adj = graph.get()

# 求解最大团问题
SCIPSolver(graph_adj)
# GurobiSolver(graph_adj)

# draw_graph = DrawGraph(graph_adj)
# draw_graph.draw()