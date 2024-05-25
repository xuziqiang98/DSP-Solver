import path_setup
import os
import time

from tqdm import tqdm
from src.IRD_HA import IRD_HA
from src.configs.common_configs import PathConfig
from src.split_graph import SplitGraph
from src.IRD_LP import IRD_LP
from src.ILP import ILP
from src.draw_graph import DrawGraph

def test_HA():
    # os.system('cls' if os.name == 'nt' else 'clear')  # clear the terminal output
    split_graph = SplitGraph('SplitGraph', 100)
    split_graph.save2file(PathConfig.data / 'split_graphs.csv')
    adj = split_graph.get_adj()
    lp_path = PathConfig.data / 'LPs.lp'
    lp = IRD_LP(adj, lp_path)
    lp.generate_lp()
    # env = Env()
    # env.setParam('OutputFlag', 0)
    # ilp = ILP(str(lp_path), env)
    ilp = ILP(str(lp_path))
    # ilp._model.setParam('OutputFlag', 0)
    ilp.optimize()
    print(f'ILP output: {ilp.getValues()}')
    ha = IRD_HA(split_graph)
    ha.optimize()
    print(f'Maximun degree: {split_graph.get_max_degree()}')
    print(f'HA output: {ha.getValues()}')
    # draw_graph = DrawGraph(split_graph.get_adj())
    # draw_graph.draw_split(split_graph.get_clique())
    if ilp.getValues() == ha.getValues():
        print('Test passed.')
    else:
        print('Test failed.')
    
    # save the results at the end of the file
    with open(PathConfig.data / 'results.txt', 'a') as f:
        f.write(f'ILP output: {ilp.getValues()}\n')
        # f.write(f'Maximum degree: {split_graph.get_max_degree()}\n')
        f.write(f'HA output: {ha.getValues()}\n')
        # if ilp.getValues() == ha.getValues() print passed, otherwise failed
        f.write('Test passed.\n\n' if ilp.getValues() == ha.getValues() else 'Test failed.\n\n')

if __name__ == '__main__':
    for _ in tqdm(range(100)):
        test_HA()
        # time.sleep(0.1)  # wait for a while to make the progress bar visible
    