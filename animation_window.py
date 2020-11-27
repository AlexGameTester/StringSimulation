class AnimationWindow:
    """
    Represents a pygame window that shows animated simulations
    """
    def __init__(self, output_manager, math_simulation, phys_simulation):
        self.output_manager = output_manager
        self._math_simulation = math_simulation
        self._phys_simulation = phys_simulation

    def start_animation(self):
        """
        Creates pygame window and starts showing animation. **Blocks program execution**
        """
        pass
