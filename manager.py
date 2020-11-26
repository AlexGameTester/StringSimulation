from inputwindow import StartParameters


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
