import click 
import scripts.path_setup

from pathlib import Path
from tqdm import tqdm
from src.configs.common_configs import PathConfig
from src.utils import GraphType
from src.graph import GraphFactory
from src.env import make
from src.draw_graph import DrawGraph

@click.command()
@click.option('--problem', required = True, type = str, help = 'a variant of domination problem')
@click.option('--graph', required = True, type = str, help='special graph type')
@click.option('--order', default = 10, type = int, help = 'graph order', show_default = True)
def run(problem, graph, order):
    graph_type = GraphType[graph]
    graph_factory = GraphFactory()
    graph = graph_factory.get(graph_type, order)
    graph_adj = graph.get()
    env = make(problem, graph_adj)
    dominating_set, domination_number = env.solve()
    if isinstance(dominating_set, list) and not any(isinstance(item, list) for item in dominating_set):
        dominating_set = [dominating_set]
    print(f'[+] The problem {problem} has been solved in graph {graph}.')
    print(f'[+] The domination number is {domination_number}.')
    for i in range(len(dominating_set)):
        print(f'[+] And the specific resulted set assigned {i} is {dominating_set[i]}.')
    draw_graph = DrawGraph(graph_adj)
    draw_graph.draw()

if __name__ == '__main__':
    run()