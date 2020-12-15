import time

import pygame
import numpy as np

import calculations_manager
from config import *

CALC_NUMBER = 60000

POINT_RADIUS = 5
DRAWING_STEP = 1

POINTS_COLORS = [BLACK, RED]

FONT_SIZE = 24


class AnimationWindow:
    """
    Represents a pygame window that shows animated simulations
    """
    def __init__(self, math_simulation, phys_simulation):
        self._math_simulation = math_simulation
        self._phys_simulation = phys_simulation

        assert self._math_simulation == math_simulation
        assert self._phys_simulation == phys_simulation
        assert self._math_simulation.simulation_time == self._phys_simulation.simulation_time
        self.simulation_time = self._math_simulation.simulation_time
        """Number of frames in animation"""

        self.current_frame = 0
        self.playback_speed = 1.0
        self.paused = False
        self.finished = False
        self.screen = None
        self._font = None

    def playback_control(self, event):
        """
        Handles pygame.KEYUP events to provide control over playback process

        :param event: a pygame event object
        """
        key_pause = pygame.K_SPACE
        key_restart = pygame.K_r
        key_quit = pygame.K_ESCAPE

        key_backwards = pygame.K_LEFT
        key_forward = pygame.K_RIGHT
        step = int(0.75 * FPS)

        key_speedup = pygame.K_UP
        key_speeddown = pygame.K_DOWN
        key_reset_speed = pygame.K_s
        speed_step = 0.2
        min_speed = speed_step
        max_speed = 5

        assert self.screen

        if event and event.type == pygame.KEYUP:
            key = event.key
            if key == key_pause:
                self.paused = not self.paused
            elif key == key_quit:
                self.finished = True
            elif key == key_restart:
                self.current_frame = 0
            elif key == key_backwards:
                self.current_frame = max(0, self.current_frame - step)
            elif key == key_forward:
                self.current_frame = min(self.simulation_time - 1, self.current_frame + step)
            elif key == key_speedup:
                self.playback_speed = min(max(min_speed, self.playback_speed + speed_step), max_speed)
            elif key == key_speeddown:
                self.playback_speed = min(max(min_speed, self.playback_speed - speed_step), max_speed)
            elif key == key_reset_speed:
                self.playback_speed = 1

            self.draw_frame()

    def _init_font(self):
        pygame.font.init()
        try:
            self._font = pygame.font.SysFont('', FONT_SIZE)
        except pygame.error as e:
            print('Failed to load default font')
            fonts = pygame.font.get_fonts()
            if fonts:
                self._font = pygame.font.SysFont(fonts[0], FONT_SIZE)

    def start_animation(self):
        """
        Creates pygame window and starts showing animation. **Blocks program execution**
        """
        pygame.init()

        self._init_font()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(WHITE)

        clock = pygame.time.Clock()

        pygame.display.set_caption('StringSimulation')
        try:
            while not self.finished:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.finished = True
                    else:
                        self.playback_control(event)

                if self.current_frame < self.simulation_time and not self.paused:
                    self.draw_frame()
                    self.current_frame = min(self.current_frame + self.playback_speed, self.simulation_time - 1)

            pygame.quit()
        finally:
            pygame.quit()

    def _draw_playback_speed(self):
        if self._font:
            playback_speed = self._font.render('{:.2f}x'.format(self.playback_speed), True, BLACK)
            self.screen.blit(playback_speed, (0.15 * SCREEN_WIDTH, 0.06 * SCREEN_HEIGHT))

    def _draw_frame_number(self):
        if self._font:
            frame_number = self._font.render('{:.2f}/{}'.format(self.current_frame + 1, self.simulation_time)
                                             , True, BLACK)
            self.screen.blit(frame_number, (0.485 * SCREEN_WIDTH, 0.03 * SCREEN_HEIGHT))

    def _draw_playback_progress(self):
        # progress bar border
        start_y = int(0.05 * SCREEN_HEIGHT)
        start_x = int(0.2 * SCREEN_WIDTH)
        length_y = int(0.05 * SCREEN_HEIGHT)
        length_x = int(0.6 * SCREEN_WIDTH)
        pygame.draw.rect(self.screen, BLACK, [start_x, start_y, length_x, length_y])
        # progress bar
        pb_start_y = int(0.06 * SCREEN_HEIGHT)
        pb_start_x = int(0.21 * SCREEN_WIDTH)
        pb_length_y = int(0.03 * SCREEN_HEIGHT)
        progress = self.current_frame / self.simulation_time
        pb_length_x = int(0.58 * SCREEN_WIDTH * progress)
        pygame.draw.rect(self.screen, RED, [pb_start_x, pb_start_y, pb_length_x, pb_length_y])

    def draw_frame(self):
        frame_number = int(self.current_frame)
        self.screen.fill(WHITE)

        phys_points_coord = self._phys_simulation.get_points_at(frame_number)
        math_points_coord = self._math_simulation.get_points_at(frame_number)
        draw_points(self.screen, phys_points_coord, math_points_coord)

        self._draw_playback_progress()
        self._draw_playback_speed()
        self._draw_frame_number()

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
    for point in phys_points_coord:
        points_color = POINTS_COLORS[0]
        x, y = point
        if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
            continue

        pygame.draw.circle(screen,
                           points_color,
                           (int(x), int(10 * (y - SCREEN_HEIGHT//2) + SCREEN_HEIGHT // 2)),
                           POINT_RADIUS)

    for point in math_points_coord:
        points_color = POINTS_COLORS[1]
        x, y = point
        if x < -SCREEN_WIDTH or x > SCREEN_WIDTH or y < -SCREEN_HEIGHT or y > SCREEN_HEIGHT:
            continue

        pygame.draw.circle(screen,
                           points_color,
                           (int(x + SCREEN_WIDTH // 4), int(10 * y) + SCREEN_HEIGHT // 2),
                           POINT_RADIUS)


if __name__ == "__main__":
    main()
