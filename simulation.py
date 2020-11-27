from typing import List, Tuple
from enum import Enum, auto


class Simulation:
    """
    Represents a discrete function of time and coordinate that represents a simulation of string motion
    """
    def pack_time(self, times: List[float]) -> None:
        """
        Saves information about time in this object

        :param times: an array of moments of time that were simulated
        """
        pass

    def get_points(self, time: float) -> List[Tuple[float, float]]:
        """
        Returns a set of points **in consecutive order** that represents a string at specific moment of time

        :param time: a list of points represented as tuples TODO: choose another type
        """
        pass