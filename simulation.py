from abc import ABC, abstractmethod

import numpy as np


class Simulation(ABC):
    """
    Represents a discrete function of time and coordinate that represents a simulation of string motion
    """

    @abstractmethod
    def get_points_at(self, time: float) -> np.ndarray:
        """
        Returns a numpy array of y-coordinates of points **in consecutive order**
         that represents a string at specific moment of time

        :param time: a list of points represented as tuples TODO: choose another type
        """
        pass