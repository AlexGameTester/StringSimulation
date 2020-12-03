from typing import Callable

from simulation import Simulation
from simulator import Simulator

import numpy as np


class MathSimulation(Simulation):
    def __init__(self, points):
        self.points = points

    def get_points_at(self, time: int) -> np.ndarray:
        return self.points[time]


class MathematicalSimulator(Simulator):
    """
    Represents a mathematical way to simulate the process
    """

    def get_completion_percentage(self) -> float:
        pass

    def __init__(self, params):
        """
        Creates MathematicalSimulator instance

        :param params: a SimulationParameters instance
        """
        from calculations_manager import SimulationParameters
        if not isinstance(params, SimulationParameters):
            raise TypeError("Expected <class 'calculations_manager.SimulationParameters'> for params, but got",
                            type(params))

        self._string_length = params.string_length
        self._speed_of_sound = params.speed_of_sound
        self._initial_positions_x = params.initial_positions_x
        self._initial_positions_y = params.initial_positions_y
        self._initial_velocities_y = params.initial_velocities_y
        self._simulation_time = params.simulation_time
        self._number_of_points = params.number_of_points
        self._apply_accuracy(params.accuracy, self._initial_positions_x.shape[0])

        self._fourier_solver = FourierSolver(self._initial_positions_y, self._initial_velocities_y,
                                             self._initial_positions_x, self._speed_of_sound,
                                             self._string_length, self._fourier_sum_elements_number)

        self._calculated_points = []

    def _apply_accuracy(self, accuracy: int, start_points_number: int):
        min_fourier_sum_elements_number = 12
        accuracy_divider = 3000
        self._fourier_sum_elements_number = int(min_fourier_sum_elements_number \
                                            + accuracy / accuracy_divider * start_points_number)
        print('Number of sum elements is', self._fourier_sum_elements_number)

    def _method(self):
        pass

    def get_method(self) -> Callable[[None], None]:
        pass

    def simulate(self):
        """
        Initial implementation of simulation process. **Blocks program execution**
        """
        finished = False
        while not finished:
            finished = self._fourier_solver.calculate_next()
        points_at = self._fourier_solver.get_points_function()

        for i in range(self._simulation_time):
            self._calculated_points.append(points_at(i, self._number_of_points))

    def get_simulation(self) -> Simulation:
        return MathSimulation(self._calculated_points)


class FourierSolver:
    """
    Solves wave equation using fourier method

    See more:
        http://window.edu.ru/resource/137/47137/files/sssu081.pdf p. 16
    """

    def __init__(self, y_pos, y_vel, x, c: float, length: float, number: int):
        """
        Fourier solver constructor

        :param y_pos: a numpy array of start y positions of points
        :param y_vel: a numpy array of start y velocities of points
        :param x: a numpy array of x positions of points
        :param c: speed of sound in string
        :param length: length of the string
        :param number: a number of terms of fourier sum to compute (defines the accuracy)
        """
        assert number > 0
        assert c > 0

        self._sin_coefficients = []
        self._cos_coefficients = []
        self._k = 1

        self.y_pos = y_pos
        self.y_vel = y_vel
        self.x = x
        self.a = 1 / c
        self.length = length
        self.number = number
        self.number_of_points = y_pos.shape[0]

    def get_cos_coefficient(self, k: float) -> float:
        """
        Calculates coefficient of cosine in sum

        :param k: number of term in sum
        :return: a float value of the coefficient
        """
        x = self.x
        y = self.y_pos
        length = self.length

        func = 2 / length * y * np.sin(k * np.pi * x / length)
        return np.trapz(func, x)

    def get_sin_coefficient(self, k: float) -> float:
        """
        Calculates coefficient of sine in sum

        :param k: number of term in sum
        :return: a float value of the coefficient
        """
        x = self.x
        y_ = self.y_vel
        a = self.a
        length = self.length

        func = 2 / (k * np.pi * a) * y_ * np.sin(k * np.pi * x / length)
        return np.trapz(func, x)

    def calculate_next(self) -> bool:
        """
        Calculates coefficients of next term of sum

        :return: if the calculation is finished
        """
        if self._k > self.number:
            return True

        self._sin_coefficients.append(self.get_sin_coefficient(self._k))
        self._cos_coefficients.append(self.get_cos_coefficient(self._k))

        self._k += 1

        return False

    def get_points_function(self) -> Callable[[float, int], np.ndarray]:
        """
        Gives a function that returns points positions at some time

        :return: function of signature (time: float) -> numpy array that returns y coordinates
         of string points in the given point in time
        """
        assert self._sin_coefficients
        assert self._cos_coefficients
        assert self._k >= self.number, "Calculation isn't finished"

        number = self.number
        a = self.a
        length = self.length
        cos_coefficients = np.array(self._cos_coefficients)
        sin_coefficients = np.array(self._sin_coefficients)

        def points_at(time: float, number_of_points: int):
            assert number_of_points > 0
            k_vals = np.array(range(number)) + 1

            x = np.linspace(0, self.length, number_of_points)

            # TODO: check this code somehow
            cos_sum_time_part = np.tile(cos_coefficients * np.cos(k_vals * np.pi * a * time / length),
                                        (number_of_points, 1))
            cos_sum_part = cos_sum_time_part * np.sin(np.pi / length * np.tensordot(x, k_vals, axes=0))
            cos_part = np.sum(cos_sum_part, 1)

            sin_sum_time_part = np.tile(sin_coefficients * np.sin(k_vals * np.pi * a * time / length),
                                        (number_of_points, 1))
            sin_sum_part = sin_sum_time_part * np.sin(np.pi / length * np.tensordot(x, k_vals, axes=0))
            sin_part = np.sum(sin_sum_part, 1)

            return cos_part + sin_part

        return points_at
