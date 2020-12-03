import time

import pygame
import numpy as np

import math_simulator
import physical_simulator
import calculations_manager

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
FPS = 400

POINT_RADIUS = 5
DRAWING_STEP = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

POINTS_COLORS = [BLACK, RED]


class AnimationWindow:
    """
    Represents a pygame window that shows animated simulations
    """

    def __init__(self, math_simulation, phys_simulation):
        self._math_simulation = math_simulation
        self._phys_simulation = phys_simulation

        self.animation_time = 0

    def start_animation(self):
        """
        Creates pygame window and starts showing animation. **Blocks program execution**
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

            if self.animation_time < physical_simulator.CALC_NUMBER - DRAWING_STEP:
                phys_points_coord = self._phys_simulation.get_points_at(self.animation_time)
                math_points_coord = self._math_simulation.get_points_at(self.animation_time)
                # math_points_coord = [(20, 20), (40, 40), (60, 60), (100, 100), (200, 200), (600, 600)]
                # points_coordinates = [phys_points_coord, math_points_coord]
                draw_points(screen, phys_points_coord, math_points_coord)

                self.animation_time += DRAWING_STEP
            else:
                time.sleep(2)
                finished = True

            pygame.display.set_caption(str(clock.get_fps()))

            pygame.display.update()


def main():
    params = get_params()
    math_sim = math_simulator.MathematicalSimulator(params)
    math_sim.simulate()
    math_simulation = math_sim.get_simulation()

    phys_sim = physical_simulator.PhysicalSimulator(10, 1)
    phys_sim.simulate()
    phys_simulation = phys_sim.get_simulation()

    animation = AnimationWindow(math_simulation, phys_simulation)
    animation.start_animation()


def get_params():
    initial_pos_x = np.linspace(0, SCREEN_WIDTH // 2, 2000)
    initial_pos_y = 30e5 * np.sin(3 * np.pi * initial_pos_x) + 30e5 * np.sin(12 * np.pi * initial_pos_x + 7/8 * np.pi)
    # initial_pos_y = initial_pos_x * 0
    initial_pos_y[0] = 0
    initial_pos_y[initial_pos_y.shape[0] - 1] = 0
    initial_vel_y = initial_pos_x * 0
    # initial_vel_y[1000] = 18

    number_of_points = 40

    params = calculations_manager.SimulationParameters(1000, 1/3, initial_pos_x, initial_pos_y, initial_vel_y, accuracy=5,
                                                       number_of_points=number_of_points)

    return params


def draw_points(screen, phys_points_coord, math_points_coord):
    screen.fill(WHITE)
    for point in phys_points_coord:
        points_color = POINTS_COLORS[0]
        x, y = point
        pygame.draw.circle(screen,
                           points_color,
                           (int(x), int(y)),
                           POINT_RADIUS)

    for point in math_points_coord:
        points_color = POINTS_COLORS[1]
        x, y = point
        pygame.draw.circle(screen,
                           points_color,
                           (int(x + SCREEN_WIDTH // 4), int(y) + SCREEN_HEIGHT // 2),
                           POINT_RADIUS)


if __name__ == "__main__":
    main()
