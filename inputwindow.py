from tkinter import *

calculating = None

class StartParameters:
    
    def __init__(self, density, simulation_time, tension):
        self.density = density
        self.simulation_time = simulation_time
        self.tension = tension
        self.data = [density, simulation_time, tension]

    
class InputWindow:
    """
    Represents a window that is displayed when the program is launched. User sets parameters in this window
    """
    
    def get_parameters(self) -> StartParameters:
        """
        Reads data from the window and transforms it into a list of parameters
        """
        global calculating

        if len(self.density_entry.get()) == 0:
            density_double = 1
        elif getdouble(self.density_entry.get()) < 0:
            density_double = 2
        else:
            density_double = getdouble(self.density_entry.get())
        
        if len(self.simulation_time_entry.get()) == 0:
            simulation_time_double = 1
        elif getdouble(self.simulation_time_entry.get()) < 0:
            simulation_time_double = 2
        else:
            simulation_time_double = getdouble(self.simulation_time_entry.get())
        
        if len(self.tension_entry.get()) == 0:
            tension_double = 1
        elif getdouble(self.tension_entry.get()) < 0:
            tension_double = 2
        else:
            tension_double = getdouble(self.tension_entry.get())
        
        c = StartParameters(density_double, simulation_time_double, tension_double)
        
        calculating = True

        Action2(c.data) 
        return c.data
        
        
    def __init__(self, master, manager):
        self.manager = manager
        self.master = master
        self.master.geometry('400x200')
        self.master.resizable(width=False, height=False)
        
        center_frame = Frame(self.master)
        center_frame.pack(side=TOP)
        
        self.label1 = Label(center_frame, text="Density")
        self.label1.grid(row=0, column=0, pady=5, padx=5)
        self.density_entry = Entry(center_frame)
        self.density_entry.grid(row=0, column=1, pady=5, padx=5)

        self.label2 = Label(center_frame, text="Simulation Time")
        self.label2.grid(row=1, column=0, pady=5, padx=5)
        self.simulation_time_entry = Entry(center_frame)
        self.simulation_time_entry.grid(row=1, column=1, pady=5, padx=5)

        self.label3 = Label(center_frame, text="Tension")
        self.label3.grid(row=2, column=0, pady=5, padx=5)
        self.tension_entry = Entry(center_frame)
        self.tension_entry.grid(row=2, column=1, pady=5, padx=5)

        Button1 = Button(center_frame, command=self.get_parameters, width=10, 
                                        height=2, font=18, text="Start")
        Button1.grid(row=3)
    
    
    def _close(self):
        pass
        
def Action2(x):
    print(x)
    print("buba")
    print("Input parameters are processing, please wait.")
    print(calculating)

    

        




App = Tk()
a = InputWindow(App, 1)
a.__dict__
print(a.__dict__)
App.mainloop()
