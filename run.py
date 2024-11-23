import click 
import scripts.path_setup

from pathlib import Path
from tqdm import tqdm
from src.configs.common_configs import PathConfig
from src.utils import GraphType
from src.graph import GraphFactory
from src.env import make
from src.draw_graph import DrawGraph
from src.xvalidation import validation_dict, ValidationFactory

@click.command()
@click.option('--problem', required = True, type = str, help = 'a variant of domination problem')
@click.option('--graph', required = True, type = str, help='special graph type')
@click.option('--order', default = 10, type = int, help = 'graph order', show_default = True)
@click.option('--cross_validation', is_flag = True, default = False, help = 'cross validation')
def run(problem, graph, order, cross_validation):
    ################################
    # Set up the environment       #
    ################################
    
    graph_type = GraphType[graph]
    graph_factory = GraphFactory()
    graph = graph_factory.get(graph_type, order)
    graph_adj = graph.get()
    env = make(problem, graph_adj)
    valid_step = 50 
    
    ################################
    # Solve the problem            #
    ################################
    
    if cross_validation:
        validation_factory = ValidationFactory()
        if graph_type not in validation_dict[problem]:
            raise NotImplementedError(f'[-] {problem} is not implemented')
        for t in tqdm(range(valid_step)):
            _, gurobi_result = env.solve()
            validation = validation_factory.get(problem, graph_adj)
            _, valid_result = validation.solve()
            if int(gurobi_result) == int(valid_result):
                print(f'[+] TIMESTEP {t}: The problem {problem} has been passed validation in graph {graph}.')
            else:
                print(f'[-] TIMESTEP {t}: Something wrong happened in graph {graph}.')
                print(f'[-] Check the result in the follwing graph with adjacency matrix:')
                print(graph_adj)
                break
    else:   
        dominating_set, domination_number = env.solve()
        # if isinstance(dominating_set, list) and not any(isinstance(item, list) for item in dominating_set):
        if not isinstance(dominating_set[0], list):
            dominating_set = [dominating_set]
        print(f'[+] The problem {problem} has been solved in graph {graph}.')
        print(f'[+] The domination number is {domination_number}.')
        for i in range(len(dominating_set)):
            print(f'[+] And the specific resulted set assigned {i+1} is {dominating_set[i]}.')
    
        draw_graph = DrawGraph(graph_adj)
        draw_graph.draw()

if __name__ == '__main__':
    run()