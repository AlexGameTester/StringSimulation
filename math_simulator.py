from typing import Callable

from simulation import Simulation
from simulator import Simulator

import numpy as np


class MathematicalSimulator(Simulator):
    """
    Represents a mathematical way to simulate the process
    """

    def __init__(self, params):
        # TODO: Specific way to get this values will be written later
        # assert params

        self._string_length = 10
        assert self._string_length > 0
        self._initial_positions_x = np.linspace(0, self._string_length, 2000)
        self._initial_positions_y = np.sin(3 * self._initial_positions_x)
        assert len(self._initial_positions_x.shape) == 1
        assert len(self._initial_positions_y.shape) == 1
        assert self._initial_positions_x.shape == self._initial_positions_y.shape
        self._initial_velocities_y = np.zeros(2000)
        # self._number_of_points = 5000
        # TODO: probably add data interpolation to given number of points

    def _method(self):
        pass

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        pass