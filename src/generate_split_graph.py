import scripts.path_setup

from .generate_graph import GenerateGraph
from .split_graph import SplitGraph
from .graph import Graph

class GenerateSplitGraph(GenerateGraph):
    _instance = None

    # Singleton pattern
    def __new__(cls, *args, **kwargs) -> 'GenerateSplitGraph':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, graph_type: str, num_vertices: int) -> None:
        self.graph_type = graph_type
        self.num_vertices = num_vertices

    def generate_graph(self) -> 'Graph':
        return SplitGraph(self.graph_type, self.num_vertices)
    
    def __repr__(self) -> str:
        return f'GenerateSplitGraph({self.graph_type}, {self.num_vertices})'