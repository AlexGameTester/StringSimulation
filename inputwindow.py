from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class StartParameters:
    """Starting parameter which are set by the user.

    :param speed_of_sound: speed of sound in a material of a string. Less or equal than 343
    :param simulation_time: simulation modelling duration. Less or equal than 100
    :param number_of_points: number of points in a string which will be modelled. Less or equal than 1000
    :param precision: parameter which affects the step with which modelling will be done. Less or equal than 1000.
    :param method: solution method of wave equation. Options: Fourier,

    """

    def __init__(self, speed_of_sound, simulation_time, number_of_points, precision, method):
        self.speed_of_sound = speed_of_sound
        self.simulation_time = simulation_time
        self.number_of_points = number_of_points
        self.precision = precision
        self.method = method
        self.data = [speed_of_sound, simulation_time, number_of_points, precision, method]


class InputWindow:
    """
    Represents a window that is displayed when the program is launched. User sets parameters in this window
    """

    def exit1(self):
        """
        when pressed 'Quit' button shuts down the program.
        """
        box_quit = messagebox.askquestion("Quit", "Are you sure you want to quit?")
        if box_quit == "yes":
            self._close()
        else:
            pass

    def get_parameters(self) -> StartParameters:
        """
        Reads data from the window, validates it and transforms it into a list of parameters
        """
        text1 = self.sound_speed_entry.get()
        text2 = self.simulation_time_entry.get()
        text3 = self.points_entry.get()
        text4 = self.precision_entry.get()
        list_int = [text3, text4]
        list_real = [text1, text2]

        def check_int(s):
            if len(s) == 0:
                return "Blanked"
            elif s[0] in ('-', '+'):
                return s[1:].isdigit()
            return s.isdigit()

        int_check_list = [check_int(item) for item in list_int]

        if not all([text1, text2, text3, text4]):
            box1 = messagebox.askquestion("Validation Error: Blank fields",
                                          "Some of the value inputs were left empty, Do you want to use standard "
                                          "values for those which are missing?")

            if box1 == "yes":
                if len(text1) == 0:
                    self.sound_speed_entry.insert(0, 1)
                if len(text2) == 0:
                    self.simulation_time_entry.insert(0, 1)
                if len(text3) == 0:
                    self.points_entry.insert(0, 1)
                if len(text4) == 0:
                    self.precision_entry.insert(0, 1)

        elif not all([string.isnumeric() for string in list_int]):

            messagebox.showerror("Non-numeric validation error",
                                 "Please check whether number of points and precision parameters are positive integers")
        elif any([getdouble(item) < 0 for item in (list_int + list_real)]):

            messagebox.showerror("Negative value validation error", "Please check whether all values are positive")
        elif not all(item for item in int_check_list):

            messagebox.showerror("Non-integer value validation error",
                                 "Please check whether number of points and precision parameters are integers")
        elif getint(self.points_entry.get()) > 1000:

            messagebox.showerror("Parameter is out of range",
                                 "Please check whether the number of points in a chain is less or equal than 1000")
        elif getint(self.precision_entry.get()) > 1000:

            messagebox.showerror("Parameter is out of range",
                                 "Please check whether the precision parameter is less or equal than 1000")
        elif getdouble(text1) > 343:

            messagebox.showerror("Parameter is out of range",
                                 "Please check whether the speed of sound in material is less than or equal than that in an air")
        elif getdouble(text2) > 100:

            messagebox.showerror("Parameter is out of range",
                                 "Please check whether the simulation time within the required range")
        else:
            c = StartParameters(getdouble(text1), getdouble(text2), getint(text3), getint(text4),
                                method=self.pick.get())
            return c

    def __init__(self, manager):
        self.manager = manager

        app = Tk()
        app.title("String Simulation")
        self.app = app
        self.app.geometry('400x250')
        self.app.resizable(width=False, height=False)

        center_frame = Frame(self.app)
        center_frame.pack(side=TOP)

        method_options = ["Fourier method", "Method 2"]
        self.pick = StringVar()

        self.label1 = Label(center_frame, text="Speed of sound in material")
        self.label1.grid(row=0, column=0, pady=5, padx=5)
        self.sound_speed_entry = Entry(center_frame)
        self.sound_speed_entry.grid(row=0, column=1, pady=5, padx=5)

        self.label2 = Label(center_frame, text="Simulation Time")
        self.label2.grid(row=1, column=0, pady=5, padx=5)
        self.simulation_time_entry = Entry(center_frame)
        self.simulation_time_entry.grid(row=1, column=1, pady=5, padx=5)

        self.label3 = Label(center_frame, text="Number of points in a chain")
        self.label3.grid(row=2, column=0, pady=5, padx=5)
        self.points_entry = Entry(center_frame)
        self.points_entry.grid(row=2, column=1, pady=5, padx=5)

        self.label4 = Label(center_frame, text="Precision of modelling")
        self.label4.grid(row=3, column=0, pady=5, padx=5)
        self.precision_entry = Entry(center_frame)
        self.precision_entry.grid(row=3, column=1, pady=5, padx=5)

        self.label5 = Label(center_frame, text="Solution method")
        self.label5.grid(row=4, column=0, pady=5, padx=5)
        self.menu1 = ttk.Combobox(center_frame, value=method_options, textvariable=self.pick, state="readonly")
        self.menu1.current(0)
        self.menu1.grid(row=4, column=1, pady=5, padx=5)

        button1 = Button(center_frame, command=self._start, width=10,
                         height=2, font=18, text="Start")
        button1.grid(row=5)

        button2 = Button(center_frame, command=self.exit1, width=4, height=1, font=18,
                         text="Quit")
        button2.grid(row=5, column=1)

        app.mainloop()

    def _start(self):
        params = self.get_parameters()

        if params:
            self.manager.start_calculation(params, self._close)

    def _close(self):
        self.app.destroy()
        self.manager = None
