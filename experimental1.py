import tkinter
root = tkinter.Tk()
root.geometry("600x400")
canvas1 = tkinter.Canvas(root, width = 400, height = 300)
canvas1.pack()

simulation_time = tkinter.StringVar(root)
density = tkinter.StringVar(root)
tension = tkinter.StringVar(root)
#def __init__(self, manager: Manager):
    # self.manager = manager

def _get_start_parameters(self): 
    """
    Reads data from the window and transforms it into a list of parameters
    """
    parameters = just_read()
    print(parameters)
    
    
    pass

def just_read():
    
    print(simulation_time_entry.get())
    
    
    
    if len(simulation_time_entry.get()) == 0:
        simulation_time_double = 10
    elif tkinter.getdouble(simulation_time_entry.get()) < 0:
        simulation_time_double = 11
    else :
        a = tkinter.getdouble(simulation_time_entry.get())
        simulation_time_double = a
    
    if len(density_entry.get()) == 0:
        density_double = 16
    elif tkinter.getdouble(density_entry.get()) < 0:
        density_double = 18
    else :
        b = tkinter.getdouble(density_entry.get())
        density_double = b

    if len(tension_entry.get()) == 0:
        tension_double = 10
    elif tkinter.getdouble(tension_entry.get()) < 0:
        simulation_time_double = 11
    else :
        c = tkinter.getdouble(tension_entry.get())
        tension_double = c
    
    

    parameters = [simulation_time_double, tension_double, density_double]  
    return parameters
    
def _close(self):
    pass

def start_calculation(self):
    """
    Called when user presses 'Start' button. Starts calculation of parameters
    """
    self.manager.start_calculation(self._get_start_parameters())
    self._close()

bottomframe = tkinter.Frame(root)
bottomframe.pack( side = tkinter.BOTTOM )


label1 = tkinter.Label(text = "Simultaion time")
simulation_time_entry = tkinter.Entry(root, textvariable=simulation_time)
canvas1.create_window(200, 140, window=simulation_time_entry)
canvas1.create_window(200, 100, window=label1)

label2 = tkinter.Label(text = "density")
density_entry = tkinter.Entry(root, textvariable=density)
canvas1.create_window(200, 200, window=density_entry)
canvas1.create_window(200, 160, window=label2)

label3 = tkinter.Label(text = "tension")
tension_entry = tkinter.Entry(root, textvariable=tension)
canvas1.create_window(200, 260, window=tension_entry)
canvas1.create_window(200, 220, window=label3)


start_button = tkinter.Button(bottomframe, text="Start", command=just_read,  width=17, 
                                height=3, font=18)
start_button.pack( side = tkinter.BOTTOM)



root.mainloop()
