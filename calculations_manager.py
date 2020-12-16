import tkinter as tk
import tkinter.ttk as ttk
import multiprocessing as mp
import os
import ctypes

from playsound import playsound
import numpy as np

from input_window import StartParameters
from math_simulator import MathematicalSimulator
from physical_simulator import PhysicalSimulator
import image_reading
from config import *


class SimulationParameters:
    """
    Represents a list of parameters that is set by CalculationsManager and given to simulators
    """

    def __init__(self, simulation_time: int,
                 speed_of_sound: float,
                 initial_positions_x: np.ndarray,
                 initial_positions_y: np.ndarray,
                 initial_velocities_y: np.ndarray,
                 simulation_method: str,
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

        assert simulation_method
        self.simulation_method = simulation_method
        """Method to use for physical simulation"""

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

    @staticmethod
    def _play_music(path):
        try:
            playsound(path)
        except UnicodeDecodeError:
            print('Can\'t read music file')
        else:
            ProgressBar._play_music(path)

    def __init__(self, on_closed):
        """
        Creates ProgressBar instance

        :param on_closed: () -> None function that is called when progressbar is closed before calculation ended
        """
        self.math_percentage = mp.Value(ctypes.c_float, 0.0)
        self.math_finished = mp.Value(ctypes.c_bool, False)
        self.phys_percentage = mp.Value(ctypes.c_float, 0.0)
        self.phys_finished = mp.Value(ctypes.c_bool, False)

        self._music_thread = mp.Process(target=ProgressBar._play_music, args=(f'./music/{ACTIVE_MUSIC}',))

        self._on_closed = on_closed

        app = tk.Tk()

        self.app = app
        app.title(self.app_title)
        app.geometry()
        app.resizable(False, False)

        app.protocol('WM_DELETE_WINDOW', self.close)

        main_frame = tk.Frame(app)
        main_frame.pack(side=tk.TOP, fill='both')

        self.progressbar = ttk.Progressbar(main_frame, length=340)
        self.progressbar.grid(row=1, column=0, padx=(30, 30), pady=(0, 40))
        self.pb_label = tk.Label(main_frame)
        self.pb_label.grid(row=0, column=0, padx=(30, 30), pady=(40, 0))
        self.pb_label['text'] = self.label_text.format(0)
        self._job_id = None

    def start(self):
        self.start_updating()
        self._music_thread.start()
        self.app.mainloop()

    def is_finished(self):
        return self.phys_finished.value and self.math_finished.value

    def close(self):
        try:
            self._music_thread.terminate()
            if not self.is_finished():
                self._on_closed()
        finally:
            self.app.destroy()

    def start_updating(self):
        delay = 100

        def update():
            val = int(100 * 1/2 * (self.math_percentage.value + self.phys_percentage.value))
            self.progressbar['value'] = val
            self.pb_label['text'] = self.label_text.format(val)

            if self.is_finished():
                if self._job_id:
                    self.app.after_cancel(self._job_id)

                self.close()

            self.app.after(delay, update)

        self._job_id = self.app.after(delay, update)


class CalculationsManager:
    """
    """

    def __init__(self, manager, params: StartParameters):
        self.manager = manager
        self.start_parameters = params
        self._physical_simulator = None
        self._mathematical_simulator = None

        self._phys_process = None
        self._math_process = None

        self.canceled = False

    def _get_simulation_parameters(self) -> SimulationParameters:
        """
        Sets simulation parameters to an instance of SimulationParameters and returns it

        :return: a SimulationParameters instance with set parameters
        """

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

        sim_time = int(start_params.simulation_time * FPS)

        file_picked = start_params.file_picked
        file, ext = os.path.splitext(file_picked)

        if ext in TEXT_EXTENSIONS:
            x, y, y_vel = read_parameters(file_picked)
        elif ext in IMG_EXTENSIONS:
            x, y = image_reading.read_points(file_picked, length=450, max_y=8)
            y_vel = y * 0
        else:
            raise ValueError()

        return SimulationParameters(sim_time, start_params.speed_of_sound,
                                    x, y, y_vel, start_params.method, accuracy=start_params.precision,
                                    number_of_points=start_params.number_of_points)

    def on_progressbar_closed(self):
        """
        Called when progressbar was urgently closed to end program execution properly
        """
        self.canceled = True
        self._abort_calculation()

    def start_calculation(self):
        """
        Prepares to start of calculation and starts a calculation cycle
        """
        sim_params = self._get_simulation_parameters()

        self._physical_simulator = PhysicalSimulator(sim_params)
        self._mathematical_simulator = MathematicalSimulator(sim_params)

        pb = ProgressBar(self.on_progressbar_closed)

        result_queue = self._start_calculation_processes(pb)

        pb.start()

        if self.canceled:
            self.manager.is_closed = True
            self._abort_calculation()
        else:
            self._get_results_from_processes(result_queue)
            self._send_results()

    def _start_calculation_processes(self, progressbar):
        """
        Starts processes where mathematical and physical calculations are performed

        :param progressbar: a ProgressBar instance where shared variables are located
        :return: a queue where results will be sent
        """
        result_queue = mp.Queue()

        self._math_process = mp.Process(target=self._mathematical_simulator.simulate, args=(progressbar.math_percentage,
                                                                                            progressbar.math_finished,
                                                                                            result_queue))
        self._phys_process = mp.Process(target=self._physical_simulator.simulate, args=(progressbar.phys_percentage,
                                                                                        progressbar.phys_finished,
                                                                                        result_queue))

        self._math_process.start()
        self._phys_process.start()

        return result_queue

    def _get_results_from_processes(self, result_queue):
        """
        Gets results from processes and joins them

        :param result_queue: a queue where results were sent
        """
        r1, r2 = result_queue.get(), result_queue.get()

        if self._math_process:  # do I need to join them at the end?
            self._math_process.join()
        if self._phys_process:
            self._phys_process.join()

        for type_, obj_ in [r1, r2]:
            if type_ == 'math':
                self._mathematical_simulator = obj_
            else:
                self._physical_simulator = obj_

    def _abort_calculation(self):
        """
        Terminates processes where calculations are being performed
        """
        if self._math_process:
            self._math_process.terminate()
        if self._phys_process:
            self._phys_process.terminate()

    def _send_results(self):
        """
        Sends results of calculations to manager
        """
        assert self._physical_simulator
        assert self._mathematical_simulator

        phys_sim = self._physical_simulator.get_simulation()
        math_sim = self._mathematical_simulator.get_simulation()

        self.manager.set_simulations(math_simulation=math_sim, phys_simulation=phys_sim)
