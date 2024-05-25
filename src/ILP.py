import scripts.path_setup
import gurobipy as gp

from .algorithm import Algorithm

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
