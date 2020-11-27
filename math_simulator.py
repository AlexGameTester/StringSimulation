from typing import Callable

from simulation import Simulation
from simulator import Simulator


class MathematicalSimulator(Simulator):
    """
    Represents a mathematical way to simulate the process
    """
    def __init__(self, params):
        pass

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        pass