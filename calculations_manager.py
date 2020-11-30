from inputwindow import StartParameters
from math_simulator import MathematicalSimulator
from physical_simulator import PhysicalSimulator

import numpy as np


class SimulationParameters:
    """
    Represents a list of parameters that is set by CalculationsManager and given to simulators
    """

    def __init__(self, simulation_time: float,
                 speed_of_sound: float,
                 initial_positions_x: np.ndarray,
                 initial_positions_y: np.ndarray,
                 initial_velocities_y: np.ndarray,
                 accuracy=1,
                 number_of_points=100,
                 **kwargs):
        assert simulation_time > 0
        self.simulation_time = simulation_time
        """Time period in seconds that is simulated"""

        assert speed_of_sound > 0
        self.speed_of_light = speed_of_sound
        """Speed of sound in the string"""

        assert initial_positions_x.shape == initial_positions_y.shape == initial_velocities_y.shape
        assert len(initial_positions_x.shape) == 1
        assert initial_positions_x.shape[0] > 0
        self.initial_positions_x = initial_positions_x
        """Numpy array with points initial x-coordinates"""
        self.initial_positions_y = initial_positions_y
        """Numpy array with points initial y-coordinates"""
        self.initial_velocities_y = initial_velocities_y
        """Numpy array with points initial y-velocities"""

        assert accuracy > 0
        self.accuracy = accuracy
        """Integer parameter proportional to accuracy of calculations"""

        assert number_of_points > 0
        self.number_of_points = number_of_points
        """Number of points in simulated string"""

        if 'string_length' in kwargs.keys():
            self.string_length = kwargs['string_length']
        else:
            string_length = abs(initial_positions_x[0] - initial_positions_x[len(initial_positions_x)])
            self.string_length = string_length


class ProgressBar:
    """
    Represents a window that shows progress bar during calculations
    """
    def show_status(self, percentage: float):
        """
        Called when percentage of completion of calculations is changed to show it
        :param percentage: a percentage of completion of calculations
        """
        pass


class CalculationsManager:
    """
    Controls process of simulation of the system
    """
    def __init__(self, manager, params: StartParameters):
        self.manager = manager
        self.start_parameters = params
        self._physical_simulator = None
        self._mathematical_simulator = None

    def _get_simulation_parameters(self) -> SimulationParameters:
        """
        Sets simulation parameters to an instance of SimulationParameters and returns it

        :return: a SimulationParameters instance with set parameters
        """
        pass

    def start_calculation(self):
        """
        Prepares to start of calculation and starts a calculation cycle
        """
        sim_params = self._get_simulation_parameters()
        self._physical_simulator = PhysicalSimulator(sim_params)
        self._mathematical_simulator = MathematicalSimulator(sim_params)

    def _do_cycle(self):
        pass

    def _show_progress_bar(self):
        pass

    def _end_calculation(self):
        assert self._physical_simulator
        assert self._mathematical_simulator

        phys_sim = self._physical_simulator.get_simulation()
        math_sim = self._mathematical_simulator.get_simulation()

        self.manager.set_simulations(math_simulation=math_sim, phys_simulation=phys_sim)

        self.manager.on_calculation_ended()


