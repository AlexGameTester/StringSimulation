import tkinter
class StartParameters:
    """
    
    Represents a list of parameters set by user
    
    Parameters:
    
    **simulation_time** - simulation runtime interval, set by user
    **Tension** - tension exerted in the string
    **density** - linear density of the string
    
    
    """
    pass


class InputWindow:
    """
    Represents a window that is displayed when the program is launched. User sets parameters in this window
    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.geometry("600x400")
        
        canvas1 = tkinter.Canvas(self.root, width = 400, height = 300)
        canvas1.pack()

        simulation_time = tkinter.StringVar(self.root)
        density = tkinter.StringVar(self.root)
        tension = tkinter.StringVar(self.root)
        
        bottomframe = tkinter.Frame(self.root)
        bottomframe.pack( side = tkinter.BOTTOM )


        label1 = tkinter.Label(text = "Simultaion time")
        self.simulation_time_entry = tkinter.Entry(self.root, textvariable=simulation_time)
        canvas1.create_window(200, 140, window=self.simulation_time_entry)
        canvas1.create_window(200, 100, window=label1)

        label2 = tkinter.Label(text = "density")
        self.density_entry = tkinter.Entry(self.root, textvariable=density)
        canvas1.create_window(200, 200, window=self.density_entry)
        canvas1.create_window(200, 160, window=label2)

        label3 = tkinter.Label(text = "tension")
        self.tension_entry = tkinter.Entry(self.root, textvariable=tension)
        canvas1.create_window(200, 260, window=self.tension_entry)
        canvas1.create_window(200, 220, window=label3)


        self.start_button = tkinter.Button(bottomframe, text="Start", command=self._get_start_parameters(),   width=17, 
                                        height=3, font=18)
        self.start_button.pack( side = tkinter.BOTTOM)
        
    
    

    def _get_start_parameters(self) -> StartParameters:
        """
        Reads data from the window and transforms it into a list of parameters
        """
        
        
        
        
        if len(self.simulation_time_entry.get()) == 0:
            simulation_time_double = 10
        elif tkinter.getdouble(self.simulation_time_entry.get()) < 0:
            simulation_time_double = 11
        else :
            a = tkinter.getdouble(self.simulation_time_entry.get())
            simulation_time_double = a
        
        if len(self.density_entry.get()) == 0:
            density_double = 16
        elif tkinter.getdouble(self.density_entry.get()) < 0:
            density_double = 18
        else :
            b = tkinter.getdouble(self.density_entry.get())
            density_double = b

        if len(self.tension_entry.get()) == 0:
            tension_double = 10
        elif tkinter.getdouble(self.tension_entry.get()) < 0:
            simulation_time_double = 11
        else :
            c = tkinter.getdouble(self.tension_entry.get())
            tension_double = c
        
        

        parameters = [simulation_time_double, tension_double, density_double]  
        print(parameters)
        return parameters
       

    def _close(self):
        pass

    def start_calculation(self):
        """
        Called when user presses 'Start' button. Starts calculation of parameters
        """
        self.manager.start_calculation(self._get_start_parameters())
        self._close()

app = tkinter.Tk()
a = InputWindow(app, manager=1)
app.mainloop()
