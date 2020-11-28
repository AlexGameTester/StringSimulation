from typing import Callable
import math

from simulation import Simulation
from simulator import Simulator

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Point:

    def __init__(self, x, y_velocity):
        self.x = x
        self.velocity = y_velocity


class PhysicalSimulator(Simulator):
    """
    Represents a physical way to simulate the process
    """

    def __init__(self, params):
        super().__init__(params)

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        pass


def main():
    amount_of_points = 10
    length = SCREEN_WIDTH // 3
    max_velocity = 30

    create_init_params(amount_of_points, length, max_velocity)


def create_init_params(amount_of_points, length, max_velocity):
    delta_r = length // amount_of_points
    x = 0
    with open("physical_points.txt", "w") as points:
        for i in range(amount_of_points):
            velocity = max_velocity * math.sin(2 * math.pi * i / amount_of_points)
            point = str(x) + " " + str(velocity) + "\n"
            points.write(point)

            x += delta_r


if __name__ == "__main__":
    main()
