from abc import ABC, abstractmethod

import numpy as np


class Simulation(ABC):
    """
    Represents a discrete function of time and coordinate that represents a simulation of string motion
    """

    @abstractmethod
    def __init__(self, simulation_time: int):
        self.simulation_time = simulation_time

    @abstractmethod
    def get_points_at(self, time: int) -> list:
        """
        Returns a numpy array of y-coordinates of points **in consecutive order**
         that represents a string at specific moment of time

        :param time: a list of points represented as tuples TODO: choose another type
        """
        pass
