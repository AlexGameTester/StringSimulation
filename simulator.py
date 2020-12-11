from abc import ABC, abstractmethod
from typing import Callable

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
    def simulate(self, progressbar):
        """
        Starts a simulation.
        Periodically sends completion percentage to progressbar

        :param progressbar: a ProgressBar instance
        """
        pass


