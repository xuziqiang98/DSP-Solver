import path_setup
import numpy as np

from src.split_graph import SplitGraph
from src.configs.common_configs import PathConfig

def test_split_graph():
    path = PathConfig.data / 'split_graphs.csv'
    split_graph = SplitGraph('SplitGraph', 20)
    split_graph.save2file(path)
    # adj = np.loadtxt(path, delimiter=',', dtype=int)
    adj = SplitGraph.file2adj(path)
    
    if np.array_equal(adj, split_graph.get_adj()):
        print('Test passed.')
    else:
        print('Test failed.')
        print('Expected: ')
        print(split_graph.get_adj())
        print('Got: ')
        print(adj)

if __name__ == '__main__':
    test_split_graph()