from inputwindow import StartParameters
from simulation import Simulation, SimulationType


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
        pass

    def start_calculation(self, params: StartParameters):
        """
        Starts calculation of solutions
        :param params: a set of parameters set by user
        """
        assert params

        self._start_parameters = params

    def set_simulation(self, simulation: Simulation, simulation_type: SimulationType) -> None:
        """
        Saves simulation of some type into manager
        :param simulation: a simulation
        :param simulation_type: a type of simulation
        """
        assert simulation
        assert simulation_type
        if simulation_type == SimulationType.mathematical:
            self._mathematical_simulation = simulation
        else:
            self._physical_simulation = simulation

    def on_calculation_ended(self):
        """
        Called (by CalculationsManager) when calculation of simulation is ended
        """
        pass
