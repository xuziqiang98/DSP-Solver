import scripts.path_setup
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from graph import SplitGraph

class DrawGraph:
    def __init__(self, adj) -> None:
        self.adj = adj

    # draw the graph according to the adjacency matrix
    def draw(self) -> None:
        G = nx.from_numpy_array(self.adj)
        nx.draw(G, with_labels=True)
        plt.show()

    # draw the split graph
    # k is the number of vertices in the clique
    def draw_split(self, k) -> None:
        G = nx.from_numpy_array(self.adj)
        colors = ['red'] * k + ['blue'] * (len(G.nodes) - k)
        nx.draw(G, with_labels=True, node_color=colors)
        plt.show()
