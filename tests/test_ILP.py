import path_setup

from src.configs.common_configs import PathConfig
from src.ILP import ILP

def test_gurobi():
    path = PathConfig.data / 'LPs.lp'
    gurobi = ILP(str(path))
    gurobi.optimize()
    # print(gurobi.getValues())

if __name__ == '__main__':
    test_gurobi()