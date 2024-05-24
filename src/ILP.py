import scripts.path_setup
import gurobipy as gp

from .algorithm import Algorithm

class ILP(Algorithm):
    def __init__(self, path) -> None:
        self._name = "Gurobi"
        self._model = gp.read(path)

    def optimize(self) -> None:
        self._model.optimize()

    def getValues(self) -> float:
        return self._model.getObjective().getValue()
    
    def saveResults(self, path: str) -> None:
        self._model.write(path)

    def __repr__(self) -> str:
        return self._name
