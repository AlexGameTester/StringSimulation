import time

import pygame
import numpy as np

import calculations_manager

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
CALC_NUMBER = 60000
FPS = 400

POINT_RADIUS = 5
DRAWING_STEP = 1

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
        self.paused = False
        self.finished = False
        self.screen = None

    def playback_control(self, event):
        key_pause = pygame.K_p
        key_restart = pygame.K_r
        key_backwards = pygame.K_LEFT
        key_forward = pygame.K_RIGHT
        key_quit = pygame.K_ESCAPE
        step = 300

        assert self.screen

        if event.type == pygame.KEYUP:
            key = event.key
            if key == key_pause:
                self.paused = not self.paused
            elif key == key_restart:
                self.animation_time = 0
                self.draw_frame()
            elif key == key_backwards:
                self.animation_time = max(0, self.animation_time - step)
                self.draw_frame()
            elif key == key_forward:
                self.animation_time = min(self._math_simulation.simulation_time, self.animation_time + step)
                self.draw_frame()
            elif key == key_quit:
                self.finished = True

    def start_animation(self):
        """
        Creates pygame window and starts showing animation. **Blocks program execution**
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(WHITE)

        clock = pygame.time.Clock()

        assert self._math_simulation.simulation_time == self._phys_simulation.simulation_time, \
            'Math: {}, Phys: {}'.format(self._math_simulation.simulation_time,
                                        self._phys_simulation.simulation_time)

        while not self.finished:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                else:
                    self.playback_control(event)

            if self.animation_time < self._math_simulation.simulation_time and not self.paused:
                self.draw_frame()
                self.animation_time += DRAWING_STEP

            pygame.display.set_caption(str(clock.get_fps()))

    def draw_frame(self):
        phys_points_coord = self._phys_simulation.get_points_at(self.animation_time)
        math_points_coord = self._math_simulation.get_points_at(self.animation_time)
        draw_points(self.screen, phys_points_coord, math_points_coord)

        pygame.display.update()


def main():
    import inputwindow
    import math_simulator
    import physical_simulator

    params = get_params()
    math_sim = math_simulator.MathematicalSimulator(params)
    math_sim.simulate()
    math_simulation = math_sim.get_simulation()

    start_params = inputwindow.StartParameters(1, 100, 40, 1, 1)
    calc_manager = calculations_manager.CalculationsManager(10, start_params)
    sim_params = calc_manager._get_simulation_parameters()
    sim_params.speed_of_sound = 150
    sim_params.number_of_points = 40
    sim_params.simulation_time = 5
    sim_params.accuracy = 10000
    phys_sim = physical_simulator.PhysicalSimulator(sim_params)
    phys_sim.simulate()

    phys_simulation = phys_sim.get_simulation()

    animation = AnimationWindow(math_simulation, phys_simulation)
    animation.start_animation()


def get_params():
    """
    function for unit-tests
    gets parameters for math simulation
    """
    initial_pos_x = np.linspace(0, SCREEN_WIDTH // 2, 2000)
    initial_pos_y = 30e5 * np.sin(3 * np.pi * initial_pos_x) + 30e5 * np.sin(12 * np.pi * initial_pos_x + 7/8 * np.pi)
    # initial_pos_y = initial_pos_x * 0
    initial_pos_y[0] = 0
    initial_pos_y[initial_pos_y.shape[0] - 1] = 0
    initial_vel_y = initial_pos_x * 0
    # initial_vel_y[1000] = 18

    number_of_points = 40

    params = calculations_manager.SimulationParameters(1000, 1/3, initial_pos_x, initial_pos_y, initial_vel_y,
                                                       accuracy=5,
                                                       number_of_points=number_of_points)

    return params


def draw_points(screen, phys_points_coord, math_points_coord):
    """
    draws two cords: one from the physical simulation
    and another one from the mathematical simulation on screen

    screen - an active screen
    phys_points_coord - coordinates of points of physically simulated cord
    math_points_coord - coordinates of points of mathematically simulates cord
    """
    screen.fill(WHITE)
    for point in phys_points_coord:
        points_color = POINTS_COLORS[0]
        x, y = point
        pygame.draw.circle(screen,
                           points_color,
                           (int(x), int(10 * (y - SCREEN_HEIGHT//2) + SCREEN_HEIGHT // 2)),
                           POINT_RADIUS)

    for point in math_points_coord:
        points_color = POINTS_COLORS[1]
        x, y = point
        pygame.draw.circle(screen,
                           points_color,
                           (int(x + SCREEN_WIDTH // 4), int(10 * y) + SCREEN_HEIGHT // 2),
                           POINT_RADIUS)


if __name__ == "__main__":
    main()
