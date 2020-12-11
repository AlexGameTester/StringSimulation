from time import sleep

from inputwindow import StartParameters
from math_simulator import MathematicalSimulator
from physical_simulator import PhysicalSimulator

import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import threading
import os
import image_reading


class SimulationParameters:
    """
    Represents a list of parameters that is set by CalculationsManager and given to simulators
    """

    def __init__(self, simulation_time: int,
                 speed_of_sound: float,
                 initial_positions_x: np.ndarray,
                 initial_positions_y: np.ndarray,
                 initial_velocities_y: np.ndarray,
                 accuracy=1,
                 number_of_points=100,
                 **kwargs):
        assert simulation_time > 0
        self.simulation_time = simulation_time
        """Time period in frames that is simulated"""

        assert speed_of_sound > 0
        self.speed_of_sound = speed_of_sound
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
            string_length = abs(initial_positions_x[0] - initial_positions_x[len(initial_positions_x) - 1])
            self.string_length = string_length


class ProgressBar:
    """
    Represents a window that shows progress bar during calculations
    """
    app_title = 'Simulation in progress'
    app_geometry = '400x240'
    label_text = '  {}%  '

    def __init__(self):
        self._math_percentage = 0
        self._math_finished = False
        self._phys_percentage = 0
        self._phys_finished = False

        app = tk.Tk()

        self.app = app
        app.title(self.app_title)
        app.geometry()
        app.resizable(False, False)

        main_frame = tk.Frame(app)
        main_frame.pack(side=tk.TOP, fill='both')

        self.progressbar = ttk.Progressbar(main_frame, length=340)
        self.progressbar.grid(row=1, column=0, padx=(30, 30), pady=(0, 40))
        self.pb_label = tk.Label(main_frame)
        self.pb_label.grid(row=0, column=0, padx=(30, 30), pady=(40, 0))
        self.pb_label['text'] = self.label_text.format(0)


    def start(self):
        self.app.mainloop()

    def set_percentage(self, **kwargs):
        """
        Called when percentage of completion of calculations is changed to show it

        :keyword math_percentage: percentage of completion of mathematical simulation. float from [0,1]
        :keyword phys_percentage: percentage of completion of physical simulation. float from [0,1]
        """
        assert self.progressbar
        assert self.pb_label
        if 'math_percentage' in kwargs:
            self._math_percentage = kwargs['math_percentage']

        if 'phys_percentage' in kwargs:
            self._phys_percentage = kwargs['phys_percentage']

        percentage = (self._math_percentage + self._phys_percentage) / 2

        val = int(percentage * 100)
        # TODO: put it in separate function that is called periodically
        self.progressbar['value'] = val
        self.pb_label['text'] = self.label_text.format(val)

    def math_finished(self):
        self._math_finished = True
        if self._math_finished and self._phys_finished:
            # TODO: put it in separate function that is called periodically
            self.app.destroy()

    def phys_finished(self):
        self._phys_finished = True
        if self._math_finished and self._phys_finished:
            # TODO: put it in separate function that is called periodically
            self.app.destroy()


class CalculationsManager:
    """
    Controls process of simulation of the system
    """
    fps = 400  # TODO: maybe put it somewhere else

    text_extensions = ['.txt']
    image_extensions = ['.png']

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

        '''
        def create_init_params():
            length = 900 / 2
            max_velocity = 0.4
            max_y = 900 / 6 * 0.001

            delta_r = length / start_params.number_of_points
            x = 0
            y = 0
            velocity = 0
            with open("physical_points.txt", "w") as points:
                for i in range(start_params.number_of_points):
                    velocity = (max_velocity * (math.sin(2 * math.pi * i / start_params.number_of_points) +
                                                   math.sin(1 * math.pi * i / start_params.number_of_points)))
                    if i == start_params.number_of_points-1:
                        y = 0.
                    point = str(x) + " " + str(y) + " " + str(velocity) + "\n"
                    points.write(point)

                    x += delta_r
        '''
        def read_parameters(path):
            x = y = y_velocity = np.array([])
            with open(path) as points_file:
                for data_string in points_file:
                    point_x, point_y, point_y_velocity = data_string.split()
                    x = np.append(x, float(point_x))
                    y = np.append(y, float(point_y))
                    y_velocity = np.append(y_velocity, float(point_y_velocity))
            return x, y, y_velocity


        start_params = self.start_parameters

        sim_time = int(start_params.simulation_time * self.fps)

        # create_init_params()
        file_picked = start_params.file_picked
        file, ext = os.path.splitext(file_picked)

        if ext in self.text_extensions:
            x, y, y_vel = read_parameters(file_picked)
        elif ext in self.image_extensions:
            x, y = image_reading.read_points(file_picked, length=450, max_y=8)
            y_vel = y * 0
        else:
            raise ValueError()

        '''
        x = np.linspace(0, 300, 2000)
        y = 25 * np.sin(3 * np.pi * x / 300)
        y[0] = 0
        y[len(y) - 1] = 0
        y_ = x * 0
        '''
        return SimulationParameters(sim_time, start_params.speed_of_sound,
                                    x, y, y_vel, start_params.precision,
                                    number_of_points=start_params.number_of_points)

    def start_calculation(self):
        """
        Prepares to start of calculation and starts a calculation cycle
        """
        '''
                def make_phys():
            """
            Temporary method to make physical simulator
            :return:
            """
            from physical_simulator import create_init_params
            amount_of_points = sim_params.number_of_points
            length = 900 // 2
            max_velocity = 200
            length_0 = create_init_params(amount_of_points, length, max_velocity)
            return PhysicalSimulator(sim_params, length_0)

        '''
        sim_params = self._get_simulation_parameters()
        self._physical_simulator = PhysicalSimulator(sim_params)
        self._mathematical_simulator = MathematicalSimulator(sim_params)

        pb = ProgressBar()

        def dummy(pb):
            for i in range(7):
                sleep(2)
                pb.set_percentage(phys_percentage=0.05 * i)

        math_thread = threading.Thread(target=self._mathematical_simulator.simulate, args=(pb,))
        phys_thread = threading.Thread(target=self._physical_simulator.simulate, args=(pb,))

        math_thread.start()
        phys_thread.start()
        # math_thread.join()
        # phys_thread.join()
        pb.start()
        # self._physical_simulator.simulate()
        # self._mathematical_simulator.simulate()

        self._end_calculation()

    def _show_progress_bar(self):
        pass

    def _end_calculation(self):
        assert self._physical_simulator
        assert self._mathematical_simulator

        phys_sim = self._physical_simulator.get_simulation()
        math_sim = self._mathematical_simulator.get_simulation()

        self.manager.set_simulations(math_simulation=math_sim, phys_simulation=phys_sim)

        self.manager.on_calculation_ended()


