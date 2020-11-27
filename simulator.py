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
    def get_method(self) -> Callable[[float], None]:
        """
        Returns a method that is called in cycle of CalculationsManager

        :return: a method that will be called in CalculationsManager
        """
        pass

    @abstractmethod
    def get_simulation(self) -> Simulation:
        """
        Returns a discrete function of time and coordinate that represents simulated string

        :return: a Simulation instance that contains information about simulation
        """
        pass


