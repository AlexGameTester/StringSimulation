from typing import Callable
import math
import time

import pygame

from simulation import Simulation
from simulator import Simulator

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
FPS = 200

POINT_RADIUS = 5
CALC_NUMBER = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)


class Point:
    def __init__(self, x, y, y_velocity, number):
        self.x = int(x) + SCREEN_WIDTH // 4
        self.y = int(y) + SCREEN_HEIGHT // 2
        self.velocity = int(y_velocity)
        self.number = number

    def interact(self):
        pass

    def move(self, delta_t):
        self.y += int(self.velocity * delta_t)


class PhysicalSimulator(Simulator):
    """
    Represents a physical way to simulate the process
    """

    def __init__(self, params):
        super().__init__(params)
        self.points = []
        self.my_time = time.time()
        with open("physical_points.txt") as points_file:
            number = 0
            for data_string in points_file:
                x, y, y_velocity = data_string.split()
                point = Point(x, y, y_velocity, number)
                self.points.append(point)
                number += 1
        print(self.points)

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        pass

    def simulate(self):
        delta_time = time.time() - self.my_time
        for point in self.points:
            point.interact()
            point.move(delta_time)

        self.my_time = time.time()

    def draw(self):
        screen.fill(WHITE)
        for point in self.points:
            pygame.draw.circle(screen,
                               BLACK,
                               (point.x, point.y),
                               POINT_RADIUS)


def main():
    amount_of_points = 30
    length = SCREEN_WIDTH // 2
    max_velocity = 200

    create_init_params(amount_of_points, length, max_velocity)

    phys_sim = PhysicalSimulator(10)

    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_q or key == pygame.K_ESCAPE:
                    finished = True

        phys_sim.simulate()
        phys_sim.draw()

        pygame.display.update()


def create_init_params(amount_of_points, length, max_velocity):
    delta_r = length // amount_of_points
    x = 0
    y = 0
    with open("physical_points.txt", "w") as points:
        for i in range(amount_of_points):
            velocity = int(max_velocity * math.sin(2 * math.pi * i / amount_of_points))
            point = str(x) + " " + str(y) + " " + str(velocity) + "\n"
            points.write(point)

            x += delta_r


if __name__ == "__main__":
    main()
