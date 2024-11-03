from src.solver import SolverFactory
from src.utils import OptimizationTarget

def make(id, adj):
    
    if id in OptimizationTarget.__members__:
        env = SolverFactory.get(id, adj)
    else:
        raise NotImplementedError()

    return env