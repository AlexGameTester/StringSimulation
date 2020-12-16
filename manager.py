from calculations_manager import CalculationsManager
from input_window import StartParameters, InputWindow
from output_manager import OutputManager
from simulation import Simulation


class Manager:

    def __init__(self):
        self._input_window = None
        self._mathematical_simulation = None
        self._physical_simulation = None
        self._calculations_manager = None
        self._output_manager = None

        self.start_parameters = None
        self.is_closed = False

        self.close_message = 'User has closed the program before starting calculation'

    def start(self):
        """
        Starts execution of the program
        """
        self._input_window = InputWindow(self)
        self._input_window.start_loop()

        self.close_message = 'User has closed the program before ending calculation'

        if not self.is_closed:
            self.start_calculation()
        else:
            print(self.close_message)
            return

        if not self.is_closed:
            self.start_output()
        else:
            print(self.close_message)

    def start_calculation(self):
        """
        Starts calculation of solutions
        """
        assert self.start_parameters

        print('Starting calculation')

        self._calculations_manager = CalculationsManager(self, self.start_parameters)
        self._calculations_manager.start_calculation()

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

    def start_output(self):
        """
        Starts process of showing animated string and plots
        """
        assert self._mathematical_simulation
        assert self._physical_simulation

        self._output_manager = OutputManager(self, self._mathematical_simulation, self._physical_simulation)

        self._output_manager.start_animation()
