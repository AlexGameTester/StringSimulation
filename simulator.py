from abc import ABC, abstractmethod
from multiprocessing import Value

from simulation import Simulation


class Simulator(ABC):
    """
    Represents a class that simulates a process
    """

    @abstractmethod
    def __init__(self, params):
        pass

    @abstractmethod
    def get_simulation(self) -> Simulation:
        """
        Returns a calculated simulation

        :return: a Simulation instance that contains information about simulation
        """
        pass

    @abstractmethod
    def simulate(self, percentage: Value, finished: Value):
        """
        Starts a simulation.
        Periodically sends completion percentage to progressbar

        :param percentage: TODO: Docs
        :param finished:
        """
        pass


