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
    def get_method(self) -> Callable[[None], None]:
        """
        Returns a method that is called in cycle of CalculationsManager

        :return: a method that will be called in CalculationsManager
        """
        pass

    @abstractmethod
    def get_simulation(self) -> Simulation:
        """
        Returns a calculated simulation

        :return: a Simulation instance that contains information about simulation
        """
        pass

    @abstractmethod
    def get_completion_percentage(self) -> float:
        """
        Returns completion percentage of calculations

        :return: a float completion percentage between 0(0%) and 1(100%)
        """
        pass


