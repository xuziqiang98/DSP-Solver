import click 
import scripts.path_setup
import src.split_graph

from pathlib import Path
from tqdm import tqdm
from src.configs.common_configs import PathConfig
from src.split_graph import SplitGraph
from src.ILP import ILP
from src.IRD_LP import IRD_LP
from src.IRD_HA import IRD_HA

# @click.group()
# def main():
#     pass

# @main.command()
# @click.option('-g', '--graph', required = True, type = str, help='special graph type')
# @click.option('-o', '--order', default = 10, type = int, help = 'graph order', show_default = True)
# @click.option('-n', '--num', default = 5, type = int, help = "graph's number", show_default = True)
# @click.option('-p', '--path', default = PathConfig.data, type = str, help='storage path', show_default = True)
# def generate_graph(graph, order, num, path):
#     click.echo(f'Generating matrices of {num} {graph} with order {order}.')
#     for i in tqdm(range(num)):
#         save_file = Path(path) / f"{graph.replace(' ', '_')}_{i+1}.csv"
#         save_path = Path(path) / save_file
#         split_graph = src.split_graph.SplitGraph(graph, order)
#         split_graph.save2file(save_path)
#         click.echo(f'Generating {i+1}th {graph}.')
#     click.echo(f'All matrices are saved in {path}.')

# @main.command()
# @click.option('-d', '--domination', required = True, type = str, help = 'domination type')
# @click.option('-g', '--graph', required = True, type = str, help='special graph type')
# @click.option('-m', '--method', default = 'Gurobi', type = str, help = 'calculation method', show_default = True)
# @click.option('-p', '--path', default = PathConfig.data, type = str, help='storage path', show_default = True)
# def calculate_domination(domination, graph, method, path):
#     click.echo(f'Calculating {domination} number in {graph} by {method}.')
#     click.echo(f'All results are saved in {path}.')

@click.command()
@click.option('-g', '--graph', required = True, type = str, help='special graph type')
@click.option('-o', '--order', default = 10, type = int, help = 'graph order', show_default = True)
@click.option('-n', '--num', default = 5, type = int, help = "graph's number", show_default = True)
@click.option('-d', '--domination', required = True, type = str, help = 'domination type')
def main(graph, order, num, domination):
    click.echo(f'Generating adjacent matrices of {num} {graph} with order {order}.')
    for i in tqdm(range(num)):
        graph_name = PathConfig.data / f"{graph.replace(' ', '_')}_{i+1}.csv"
        adj_path = PathConfig.data / graph_name
        special_graph = SplitGraph(graph, order)
        special_graph.save2file(adj_path)
        click.echo(f'Generating {i+1}th {graph}.')
        click.echo(f'Calculating {domination} number in {graph}.')
        ilp_path = PathConfig.data / f'{graph.replace(" ", "_")}_{i+1}.lp'
        lp_file = IRD_LP(str(adj_path), str(ilp_path))
        lp_file.generate_lp()
        ilp = ILP(str(ilp_path))
        ilp.optimize()
        click.echo(f'ILP output: {ilp.getValues()}')
        ha = IRD_HA(special_graph)
        ha.optimize()
        click.echo(f'HA output: {ha.getValues()}')
        if ilp.getValues() == ha.getValues():
            click.echo('Test passed.')
        else:
            click.echo('Test failed.')
        with open(PathConfig.data / 'results.txt', 'a') as f:
            f.write(f'ILP output: {ilp.getValues()}\n')
            f.write(f'HA output: {ha.getValues()}\n')
            f.write('Test passed.\n\n' if ilp.getValues() == ha.getValues() else 'Test failed.\n\n')

    click.echo(f'All matrices are saved in {PathConfig.data}.')     

    click.echo(f'All results are saved in {PathConfig.data}.')

    click.echo('All tasks are done.')

if __name__ == '__main__':
    main()