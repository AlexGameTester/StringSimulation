from typing import Callable
import math
import time

import pygame

from simulation import Simulation
from simulator import Simulator

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
FPS = 400

POINT_RADIUS = 5
CALC_NUMBER = 100000
DELTA_TIME = 0.0001
K = 600
M = 1

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
        self.coordinates = [[self.x, self.y]]

    def interact(self, left_point_x, left_point_y, right_point_x, right_point_y,
                 length_0):
        left_distance = math.sqrt((self.x - left_point_x) ** 2 + (self.y - left_point_y) ** 2)
        right_distance = math.sqrt((self.x - right_point_x) ** 2 + (self.y - right_point_y) ** 2)

        left_force_y = (K * math.fabs(left_distance - length_0) *
                        (left_point_y - self.y) / left_distance)
        right_force_y = (K * math.fabs(right_distance - length_0) *
                         (right_point_y - self.y) / right_distance)

        acceleration = (left_force_y + right_force_y) / M

        self.velocity -= acceleration * DELTA_TIME

    def move(self):
        self.y -= self.velocity * DELTA_TIME
        self.coordinates.append([self.x, int(self.y)])


class PhysicalSimulator(Simulator):
    """
    Represents a physical way to simulate the process
    """

    def __init__(self, params, length_0):
        super().__init__(params)
        self.points = []
        self.my_time = 0
        self.length_0 = length_0
        with open("physical_points.txt") as points_file:
            number = 0
            for data_string in points_file:
                x, y, y_velocity = data_string.split()
                point = Point(x, y, y_velocity, number)
                self.points.append(point)
                number += 1

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        pass

    def simulate(self):
        for i in range(CALC_NUMBER):
            for point in self.points:
                if point.number != 0 and point.number != len(self.points) - 1:
                    point.interact(self.points[point.number - 1].x,
                                   self.points[point.number - 1].y,
                                   self.points[point.number + 1].x,
                                   self.points[point.number + 1].y,
                                   self.length_0)
                    point.move()

    def draw(self):
        screen.fill(WHITE)
        for point in self.points:
            if point.number != 0 and point.number != len(self.points) - 1:
                pygame.draw.circle(screen,
                                   BLACK,
                                   point.coordinates[self.my_time],
                                   POINT_RADIUS)
            else:
                pygame.draw.circle(screen,
                                   BLACK,
                                   point.coordinates[0],
                                   POINT_RADIUS)
        if self.my_time < CALC_NUMBER:
            self.my_time += 10
            return False
        else:
            time.sleep(3)
            return True


def main():
    amount_of_points = 40
    length = SCREEN_WIDTH // 2
    max_velocity = 200

    length_0 = create_init_params(amount_of_points, length, max_velocity)

    phys_sim = PhysicalSimulator(10, length_0)
    phys_sim.simulate()

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

        anim_is_ended = phys_sim.draw()
        if anim_is_ended:
            finished = True
    
        pygame.display.set_caption(str(clock.get_fps()))

        pygame.display.update()


def create_init_params(amount_of_points, length, max_velocity):
    delta_r = length // amount_of_points
    x = 0
    y = 0
    with open("physical_points.txt", "w") as points:
        for i in range(amount_of_points):
            velocity = int(max_velocity * math.sin(3 * math.pi * i / amount_of_points))
            point = str(x) + " " + str(y) + " " + str(velocity) + "\n"
            points.write(point)

            x += delta_r

    return delta_r // 400


if __name__ == "__main__":
    main()
