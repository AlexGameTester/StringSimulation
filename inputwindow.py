class StartParameters:
    """
    Represents a list of parameters set by user
    """
    pass


class InputWindow:
    """
    Represents a window that is displayed when the program is launched. User sets parameters in this window
    """
    def __init__(self, manager):
        self.manager = manager

    def _get_start_parameters(self) -> StartParameters:
        """
        Reads data from the window and transforms it into a list of parameters
        """
        pass

    def _close(self):
        pass

    def start_calculation(self):
        """
        Called when user presses 'Start' button. Starts calculation of parameters
        """
        self.manager.start_calculation(self._get_start_parameters())
        # TODO: this method is likely to be never called. Probably one should put closing of a window somewhere earlier
        self._close()
