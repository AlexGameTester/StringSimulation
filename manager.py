from inputwindow import StartParameters, InputWindow
from simulation import Simulation


class Manager:

    def __init__(self):
        self._input_window = None
        self._start_parameters = None
        self._mathematical_simulation = None
        self._physical_simulation = None

    def start(self):
        """
        Starts execution of the program
        """
        self._input_window = InputWindow(self)

    def start_calculation(self, params: StartParameters, close_function):
        """
        Starts calculation of solutions

        :param close_function: a function called to close InputWindow to avoid cyclic references
        :param params: a set of parameters set by user
        """
        assert params

        self._start_parameters = params
        print('Starting calculation')
        close_function()

    def set_simulations(self, math_simulation: Simulation, phys_simulation: Simulation) -> None:
        """
        Saves simulation of some type into manager

        :param phys_simulation: a simulation provided by physical simulator
        :param math_simulation: a simulation provided by mathematical simulator
        """
        assert phys_simulation
        assert math_simulation

        self._physical_simulation = phys_simulation
        self._mathematical_simulation = math_simulation


    def on_calculation_ended(self) -> None:
        """
        Called (by CalculationsManager) when calculation of simulation is ended
        """
        pass

    def start_output(self):
        """
        Starts process of showing animated string and plots
        """
        pass
