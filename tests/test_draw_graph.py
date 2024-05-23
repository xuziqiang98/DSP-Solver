import path_setup

from src.configs.common_configs import PathConfig
from src.draw_graph import DrawGraph
from src.split_graph import SplitGraph

def test_draw_graph():
    # split_graph = SplitGraph('SplitGraph', 10)
    path = PathConfig.data / 'split_graphs.csv'
    draw_graph = DrawGraph(SplitGraph.file2adj(path))
    draw_graph.draw()
    # print(path)

if __name__ == '__main__':
    test_draw_graph()

