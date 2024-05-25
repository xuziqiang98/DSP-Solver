import path_setup

from src.configs.common_configs import PathConfig
from src.draw_graph import DrawGraph
from src.graph import Graph
from src.split_graph import SplitGraph
from test_IRD_LP import test_LP
from test_ILP import test_gurobi

def test_draw_graph():
    split_graph = SplitGraph('SplitGraph', 10)
    # path = PathConfig.data / 'split_graphs.csv'
    # draw_graph = DrawGraph(Graph.file2adj(path))
    # draw_graph.draw()
    # print(path)
    split_graph.save2file(PathConfig.data / 'split_graphs.csv')
    draw_graph = DrawGraph(split_graph.get_adj())
    draw_graph.draw_split(split_graph.get_clique())

def test_draw_local_graph():
    path = PathConfig.data / 'split_graphs.csv'
    draw_graph = DrawGraph(Graph.file2adj(path))
    draw_graph.draw()

if __name__ == '__main__':
    # test_draw_graph()
    # test_LP()
    # test_gurobi()
    test_draw_local_graph()
    

