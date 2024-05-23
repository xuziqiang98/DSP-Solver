import scripts.path_setup
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from .split_graph import SplitGraph

class DrawGraph:
    def __init__(self, adj) -> None:
        self.adj = adj

    # draw the graph according to the adjacency matrix
    def draw(self) -> None:
        G = nx.from_numpy_array(self.adj)
        nx.draw(G, with_labels=True)
        plt.show()
