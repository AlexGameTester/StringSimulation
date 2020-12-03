from animation_window import AnimationWindow


class OutputManager:
    """
    Provides visual representation of given simulations
    """
    def __init__(self, manager, math_simulation, phys_simulation):
        assert math_simulation
        assert phys_simulation

        self.manager = manager
        self._math_simulation = math_simulation
        self._phys_simulation = phys_simulation
        print(math_simulation)
        print(phys_simulation)
        self._animation_window = AnimationWindow(math_simulation=math_simulation, phys_simulation=phys_simulation)

    def start_animation(self):
        """
        Starts pygame window with animation. **Blocks program execution**
        """
        self._animation_window.start_animation()

    def show_plots(self):
        """
        Creates matplotlib window with necessary plots
        """
        pass
