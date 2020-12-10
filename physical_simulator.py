from typing import Callable
import math
import time

import pygame
import numpy as np

from simulation import Simulation
from simulator import Simulator

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
POINT_RADIUS = 5
FPS = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ALPHA = 0.01


class PhysicalSimulation(Simulation):
    """
       Represents a discrete function of time and coordinate that represents a simulation of string motion
    """
    def __init__(self, simulation_time, counts_per_frame, points):
        super(PhysicalSimulation, self).__init__(simulation_time)
        self.points = points
        self.counts_per_frame = counts_per_frame

    def get_points_at(self, time_moment: int) -> list:
        """
                Returns a numpy array of y-coordinates of points **in consecutive order**
                 that represents a string at specific moment of time

                :param time_moment: a list of points represented as tuples TODO: choose another type
        """
        points_coord = []
        for point in self.points:
            points_coord.append(point.coordinates[time_moment * self.counts_per_frame])

        return points_coord


class Point:
    """
    Class of physical point (parts of the cord)
    """

    def __init__(self, x, y, y_velocity, number):
        """
        init a point

        x, y - coordinates of the point on the window
        velocity - velocity on y axis
        number - number of point in the cord
        """
        self.x = x + SCREEN_WIDTH // 4
        self.y = y + SCREEN_HEIGHT // 2
        self.velocity = y_velocity
        self.number = number
        self.coordinates = [(self.x, self.y)]

    def interact(self, left_point_x, left_point_y,
                 right_point_x, right_point_y,
                 coefficient, length_0, delta_time):
        """
        interaction of the point with the others

        left_point_x, left_point_y - coordinates of the left point
        right_point_x, right_point_y - coordinates of the right point
        coefficient - ratio of K to M for the cord
        length_0 - unstretched spring length
        """
        left_distance = math.sqrt((self.x - left_point_x) ** 2 + (self.y - left_point_y) ** 2)
        right_distance = math.sqrt((self.x - right_point_x) ** 2 + (self.y - right_point_y) ** 2)

        left_delta_y = left_point_y - self.y
        right_delta_y = right_point_y - self.y

        left_acceleration = (coefficient * left_delta_y *
                             math.fabs(left_distance - length_0) / left_distance)

        right_acceleration = (coefficient * right_delta_y *
                              math.fabs(right_distance - length_0) / right_distance)

        acceleration = left_acceleration + right_acceleration

        self.velocity -= acceleration * delta_time

    def move(self, delta_time):
        """
        moves the point on y axis
        """
        self.y -= self.velocity * delta_time

    def make_a_record(self):
        """
        makes a record to a coordinates list
        """
        self.coordinates.append((self.x, self.y))


class PhysicalSimulator(Simulator):
    """
    Represents a physical way to simulate the process
    """

    def get_completion_percentage(self) -> float:
        pass

    def __init__(self, params):
        super().__init__(params)
        self.points = []
        self.my_time = 0

        self.speed_of_sound = params.speed_of_sound
        self.amount_of_points = params.number_of_points
        self.delta_time = 1 / (100 + params.accuracy)
        self.counts_per_frame = int(1 / self.delta_time)
        self.calc_count = params.simulation_time * self.counts_per_frame

        ratio = int(len(params.initial_positions_x) / params.number_of_points)
        point_number = 0

        x_linted = np.linspace(0, params.string_length, params.number_of_points)
        y_linted = np.interp(x_linted, params.initial_positions_x, params.initial_positions_y)
        y_linted[0] = 0
        y_linted[len(y_linted) - 1] = 0

        y_vel_linted = np.interp(x_linted, params.initial_positions_x, params.initial_velocities_y)
        y_vel_linted[0] = 0
        y_vel_linted[len(y_vel_linted) - 1] = 0

        for number, point in enumerate(zip(x_linted,
                                           y_linted,
                                           y_vel_linted)):
            x, y, y_velocity = point
            point = Point(x, y, y_velocity, number)
            self.points.append(point)

    def get_method(self) -> Callable[[float], None]:
        pass

    def get_simulation(self) -> Simulation:
        """
        creates and returns an object of PhysicalSimulation class
        """
        physical_simulation = PhysicalSimulation(self.calc_count // self.counts_per_frame,
                                                 self.counts_per_frame, self.points)

        return physical_simulation

    def simulate(self, progressbar):
        length = SCREEN_WIDTH // 2
        coefficient = (self.speed_of_sound ** 2 * self.amount_of_points *
                       (self.amount_of_points - 1) / (length ** 2 * (1 - ALPHA)))
        length_0 = ALPHA * length / (self.amount_of_points - 1)

        i = 0
        while i < self.calc_count:
            for point in self.points:
                if point.number != 0 and point.number != len(self.points) - 1:
                    left_point_number = self.points[point.number - 1]
                    right_point_number = self.points[point.number + 1]
                    point.interact(left_point_number.x,
                                   left_point_number.y,
                                   right_point_number.x,
                                   right_point_number.y,
                                   coefficient, length_0, self.delta_time)
                    point.move(self.delta_time)
                point.make_a_record()

            if i % 100 == 0:
                progressbar.set_percentage(phys_percentage=i / self.calc_count)
            i += 1

        progressbar.set_percentage(phys_percentage=1)

        progressbar.phys_finished()

    def draw(self, screen):
        """
        draws points of the cord on window "screen"

        drawing_step - the number of time moments between two frames
        """
        screen.fill(WHITE)
        for point in self.points:
            if point.number != 0 and point.number != len(self.points) - 1:
                x, y = point.coordinates[self.my_time]
                pygame.draw.circle(screen,
                                   BLACK,
                                   (int(x), int(10 * (y - SCREEN_HEIGHT // 2) + SCREEN_HEIGHT // 2)),
                                   POINT_RADIUS)
            else:
                x, y = point.coordinates[0]
                pygame.draw.circle(screen,
                                   BLACK,
                                   (int(x), int(10 * (y - SCREEN_HEIGHT // 2) + SCREEN_HEIGHT // 2)),
                                   POINT_RADIUS)
        if self.my_time < self.calc_count - 30:
            self.my_time += 30
            return False
        else:
            time.sleep(3)
            return True


def main():
    import calculations_manager
    import inputwindow

    start_params = inputwindow.StartParameters(1, 100, 40, 1, 1)
    calc_manager = calculations_manager.CalculationsManager(10, start_params)

    sim_params = calc_manager._get_simulation_parameters()

    sim_params.speed_of_sound = 3
    sim_params.number_of_points = 40
    sim_params.simulation_time = 5
    sim_params.accuracy = 1000

    phys_sim = PhysicalSimulator(sim_params)
    phys_sim.simulate()

    phys_simulation = phys_sim.get_simulation()

    print("1 - draw phys_sim, 2 - get coordinates in time: ")
    act = int(input())

    if act == 1:
        draw_phys_sim(phys_sim)
    elif act == 2:
        get_coord(phys_simulation)


def create_init_params(amount_of_points, length, max_velocity):
    """
    test function, which create a text file with initial coordinates
    and velocities of points in the cord

    amount_of_points - amount of points in the cord
    length - the full length of the cord
    max_velocity - maximal initial velocity of some points in the cord
    """
    delta_r = length // amount_of_points
    x = 0
    y = 0
    with open("physical_points.txt", "w") as points:
        for i in range(amount_of_points):
            velocity = int(max_velocity * (math.sin(2 * math.pi * i / amount_of_points) +
                                           math.sin(1 * math.pi * i / amount_of_points)))
            point = str(x) + " " + str(y) + " " + str(velocity) + "\n"
            points.write(point)

            x += delta_r

    return delta_r // 400


def draw_phys_sim(phys_sim):
    """
    function for unit-tests
    draws the animation
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

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

        anim_is_ended = phys_sim.draw(screen)
        if anim_is_ended:
            finished = True

        pygame.display.set_caption(str(clock.get_fps()))

        pygame.display.update()


def get_coord(physical_simulation):
    """
    function for unit-tests
    prints a list of coordinates of all points at a certain point in time
    """
    finished = False
    while not finished:
        print("\nEnter time (int): {(-1) - exit}")
        time_moment = int(input())
        if time_moment != -1:
            coordinates = physical_simulation.get_points_at(time_moment)
            print(coordinates)
        else:
            finished = True


if __name__ == "__main__":
    main()
