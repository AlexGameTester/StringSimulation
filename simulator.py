from abc import ABC, abstractmethod
from typing import Callable


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
        :return: a method that will be called in CalculationsManager
        """
        pass


