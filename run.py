import click 
import scripts.path_setup
import src.split_graph

from pathlib import Path
from tqdm import tqdm
from src.configs.common_configs import PathConfig

@click.group()
def main():
    pass

'''
Generate special graphs' adjacent matrix.
'''
@main.command()
@click.option('-g', '--graph', required = True, type = str, help='special graph type')
@click.option('-o', '--order', default = 10, type = int, help = 'graph order', show_default = True)
@click.option('-n', '--num', default = 5, type = int, help = "graph's number", show_default = True)
@click.option('-p', '--path', default = PathConfig.data, type = str, help='storage path', show_default = True)
def generate_graph(graph, order, num, path):
    click.echo(f'Generating matrices of {num} {graph} with order {order}.')
    for i in tqdm(range(num)):
        save_file = Path(path) / f"{graph.replace(' ', '_')}_{i+1}.csv"
        save_path = Path(path) / save_file
        split_graph = src.split_graph.SplitGraph(graph, order)
        split_graph.save2file(save_path)
        click.echo(f'Generating {i+1}th {graph}.')
    click.echo(f'All matrices are saved in {path}.')

@main.command()
@click.option('-d', '--domination', required = True, type = str, help = 'domination type')
@click.option('-g', '--graph', required = True, type = str, help='special graph type')
@click.option('-m', '--method', default = 'Gurobi', type = str, help = 'calculation method', show_default = True)
@click.option('-p', '--path', default = PathConfig.data, type = str, help='storage path', show_default = True)
def calculate_domination(domination, graph, method, path):
    click.echo(f'Calculating {domination} number in {graph} by {method}.')
    click.echo(f'All results are saved in {path}.')


if __name__ == '__main__':
    main()