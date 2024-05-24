import path_setup

from src.IRD_LP import IRD_LP
from pathlib import Path
from src.configs.common_configs import PathConfig
from src.graph import Graph

def test_LP():
    lp_path = PathConfig.data / 'LPs.lp'
    adj_path = PathConfig.data / 'split_graphs.csv'
    adj = Graph.file2adj(adj_path)
    lp = IRD_LP(adj, lp_path)
    lp.generate_lp()

if __name__ == '__main__':
    test_LP()