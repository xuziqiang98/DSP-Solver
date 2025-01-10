import click 
import scripts.path_setup

from pathlib import Path
from tqdm import tqdm
from src.configs.common_configs import PathConfig
from src.utils import GraphType, read_mtx
from src.graph import GraphFactory
from src.env import make
from src.draw_graph import DrawGraph
from src.xvalidation import validation_dict, ValidationFactory

from src.test import GurobiSolver, SCIPSolver

@click.group()
def run():
    pass

@click.command()
@click.option('--problem', required = True, type = str, help = 'a variant of domination problem')
@click.option('--graph', required = True, type = str, help='special graph type')
@click.option('--order', default = 10, type = int, help = 'graph order', show_default = True)
@click.option('--cross_validation', is_flag = True, default = False, help = 'cross validation')
def auto_gen(problem, graph, order, cross_validation):
    """
    Automatic generation of graphs.
    """
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
        
@click.command()
# @click.option('--problem', required = True, type = str, help = 'a variant of domination problem')
@click.option('--mtx', required = True, type = str, help='mtx file path')
@click.option('--solver', required = True, type = str, help = 'solver type')
def manual_gen(mtx, solver):
    """
    Manual generation of graphs.
    """
    data_dir = PathConfig().data
    
    # Get all the mtx files in the data directory
    dir_dict = {}
    for file in data_dir.iterdir():
        if file.is_dir():
            dir_dict[file] = []
            for mtx_file in file.iterdir():
                if mtx_file.is_file() and mtx_file.suffix == '.mtx':
                    dir_dict[file].append(mtx_file)
    
    if mtx.split('.')[-1] != 'mtx':
        mtx += '.mtx'
    
    # 获取mtx文件所在的文件夹
    mtx_dir = None
    for dir, files in dir_dict.items():
        for file in files:
            if file.name == mtx:
                mtx_dir = dir
                break
        if mtx_dir is not None:
            break
    
    if mtx_dir is None:
        raise FileNotFoundError(f'[-] {mtx} is not found in the data directory.')
    
    mtx_path = data_dir / mtx_dir / mtx
    print(f'[+] The mtx file path is {mtx_path}.')
    
    graph = read_mtx(str(mtx_path))
    # print(graph)
    
    if solver == 'gurobi':
        model = GurobiSolver(graph)
        model.solve()
    elif solver == 'scip':
        model = SCIPSolver(graph)
        model.solve()
        
        # print(f'[+] The gap is {gap:.2f}%')
    else:
        raise NotImplementedError(f'[-] {solver} is not implemented.')

# Add the commands to the group
run.add_command(auto_gen)
run.add_command(manual_gen)

if __name__ == '__main__':
    run()