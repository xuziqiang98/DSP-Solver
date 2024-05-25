import scripts.path_setup
import abc

from .graph import Graph

class GenerateGraph(abc.ABC):
    @abc.abstractmethod
    def generate_graph(self) -> 'Graph':
        pass