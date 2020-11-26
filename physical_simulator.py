from typing import Callable

from simulator import Simulator


class PhysicalSimulator(Simulator):
    """
    Represents a physical way to simulate the process
    """
    def __init__(self, params):
        pass

    def get_method(self) -> Callable[[float], None]:
        pass