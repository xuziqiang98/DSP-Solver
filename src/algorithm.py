import scripts.path_setup
import abc

import gurobipy as gp

from graph import SplitGraph

class Algorithm(abc.ABC):
    @abc.abstractmethod
    def optimize(self) -> None:
        pass

    @abc.abstractmethod
    def getValues(self) -> float:
        pass

    @abc.abstractmethod
    def saveResults(self, path: str) -> None:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass
    
class ILP(Algorithm):
    def __init__(self, path) -> None:
        self._name = "Gurobi"
        self._model = gp.read(path)
        # self._model = env.read(lp_path) if env else read(lp_path)

    def optimize(self) -> None:
        self._model.optimize()

    def getValues(self) -> int:
        return int(self._model.getObjective().getValue())
    
    def saveResults(self, path: str) -> None:
        self._model.write(path)

    def __repr__(self) -> str:
        return self._name
    
class IRD_HA(Algorithm):
    def __init__(self, graph: SplitGraph) -> None:
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