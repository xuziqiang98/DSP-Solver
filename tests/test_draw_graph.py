import path_setup

from src.configs.common_configs import PathConfig
from src.draw_graph import DrawGraph
from src.graph import SplitGraph, ErdosRenyiGraph, BarabasiAlbertGraph, RegularGraph, WattsStrogatzGraph, GraphFactory
# from src.split_graph import SplitGraph
# from test_IRD_LP import test_LP
# from test_ILP import test_gurobi
import matplotlib.pyplot as plt
import networkx as nx
from src.utils import GraphType

# def test_draw_graph():
#     split_graph = SplitGraph('SplitGraph', 10)
#     # path = PathConfig.data / 'split_graphs.csv'
#     # draw_graph = DrawGraph(Graph.file2adj(path))
#     # draw_graph.draw()
#     # print(path)
#     split_graph.save2file(PathConfig.data / 'split_graphs.csv')
#     draw_graph = DrawGraph(split_graph.get_adj())
#     draw_graph.draw_split(split_graph.get_clique())

# def test_draw_local_graph():
#     path = PathConfig.data / 'split_graphs.csv'
#     draw_graph = DrawGraph(Graph.file2adj(path))
#     draw_graph.draw()

# if __name__ == '__main__':
#     # test_draw_graph()
#     # test_LP()
#     # test_gurobi()
#     test_draw_local_graph()
    
# draw_graph = DrawGraph(SplitGraph(5, 3, 2).get())
# draw_graph.draw()

# draw_graph = DrawGraph(ErdosRenyiGraph(10, 0.4).get())
# draw_graph.draw()

# draw_graph = DrawGraph(RegularGraph(4, 3).get())
# draw_graph.draw()

graph_factory = GraphFactory()
split_graph = graph_factory.get(GraphType.SPLIT, 5, 3, 2)
draw_graph = DrawGraph(split_graph.get())
draw_graph.draw()