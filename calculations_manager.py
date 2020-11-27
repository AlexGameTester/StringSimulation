from inputwindow import StartParameters
from math_simulator import MathematicalSimulator
from physical_simulator import PhysicalSimulator


class SimulationParameters:
    """
    Represents a list of parameters that is set by CalculationsManager and given to simulators
    """
    pass


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


