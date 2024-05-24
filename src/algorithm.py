import scripts.path_setup
import abc

class Algorithm(abc.ABC):
    @abc.abstractmethod
    def optimize(self) -> None:
        pass

    @abc.abstractmethod
    def getValues(self) -> float:
        pass

    @abc.abstractmethod
    def saveResults(self, path: str) -> None:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass