import scripts.path_setup

from .algorithm import Algorithm
from .split_graph import SplitGraph

class IRD_HA(Algorithm):
    def __init__(self, graph: 'SplitGraph') -> None:
        self._name = "heuristic algorighm for IRD"
        self._graph = graph

    def optimize(self) -> None:
        self._value = 2 + self._graph.num_vertices - self._graph.get_max_degree() - 1

    def getValues(self) -> float:
        return self._value

    def saveResults(self, path: str) -> None:
        pass

    def __repr__(self) -> str:
        return self._name