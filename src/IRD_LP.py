import scripts.path_setup
import numpy as np

from .LP import LP

class IRD_LP(LP):

    def __init__(self, adj_path, lp_path):
        self.adj = np.loadtxt(adj_path, delimiter=',')  # read the adj_path as a 2D array
        self.lp_path = lp_path

    def generate_lp(self) -> None:
        with open(self.lp_path, 'w') as f:
            # goal
            f.write('Minimize\n')
            # sum_{i=0}^{n-1}(1 x(i, 1) + 2 x(i, 2))
            for i in range(len(self.adj)):
                f.write(f'1 x({i},1) + 2 x({i},2)')
                if i != len(self.adj) - 1:
                    f.write(' + ')
                else:
                    f.write('\n')
            # conditions
            f.write('Subject To\n')
            for i in range(len(self.adj)):
                f.write(f'1 x({i},0) + 1 x({i},1) + 1 x({i},2) = 1\n')
            # if x_i is 0, then at least a neighbor x_j is 2
            for i in range(len(self.adj)):
                f.write(f'1 x({i},1) + 1 x({i},2)')
                for j in range(len(self.adj)):
                    # x_i is adjacent to x_j
                    if self.adj[i][j] == 1:
                        f.write(f' + 1 x({j},2)')
                f.write(' >= 1\n')
            # if x_i is 1 or 2, then each neighbor x_j is 0
            for i in range(len(self.adj)):
                for j in range(len(self.adj)):
                    # x_i is adjacent to x_j
                    if self.adj[i][j] == 1:
                        f.write(f'x({i},1) + x({j},1) <= 1\n')
                        f.write(f'x({i},1) + x({j},2) <= 1\n')
                        f.write(f'x({i},2) + x({j},1) <= 1\n')
                        f.write(f'x({i},2) + x({j},2) <= 1\n')         
            # variables
            f.write('Binary\n')
            for i in range(len(self.adj)):
                f.write(f'x({i},0) x({i},1) x({i},2) ')
            f.write('\n')
            f.write('End\n')
        f.close()