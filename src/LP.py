import scripts.path_setup
import abc

class LP:
    def __init__(self, adj, path) -> None:
        self.adj = adj
        # path to save the LP file
        self.path = path

    @abc.abstractmethod
    def generate_lp(self) -> None:
        pass