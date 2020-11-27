from inputwindow import StartParameters
from simulation import Simulation, SimulationType


class Manager:

    def __init__(self):
        self.parameters = None

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
        self.parameters = params

    def set_simulation(self, simulation: Simulation, simulation_type: SimulationType) -> None:
        pass

    def on_calculation_ended(self):
        pass
