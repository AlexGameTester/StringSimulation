from calculations_manager import SimulationParameters
from math_simulator import MathematicalSimulator
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

if __name__ == "__main__":
    initial_pos_x = np.linspace(0, 10, 2000)
    # initial_pos_y = np.sin(3 * np.pi * initial_pos_x) + 8 * np.sin(12 * np.pi * initial_pos_x + 7/8 * np.pi)
    initial_pos_y = initial_pos_x * 0
    initial_pos_y[0] = 0
    initial_pos_y[initial_pos_y.shape[0] - 1] = 0
    initial_vel_y = initial_pos_x * 0
    initial_vel_y[1000] = 18

    number_of_points = 320

    start = time.time_ns()
    params = SimulationParameters(1000, 1, initial_pos_x, initial_pos_y, initial_vel_y, accuracy=1000,
                                  number_of_points=number_of_points)
    math_sim = MathematicalSimulator(params)
    math_sim.simulate()
    sim = math_sim.get_simulation()
    end = time.time_ns()
    print('Time of simulation is', (end - start)*1e-9, 'seconds.')

    x = np.linspace(0, params.string_length, number_of_points)

    fig, ax = plt.subplots()

    line, = ax.plot(x, sim.get_points_at(0))

    def animate(i):
        line.set_ydata(sim.get_points_at(i))
        return line,

    ani = animation.FuncAnimation(
        fig, animate, frames=np.array(range(1000)), blit=True)

    plt.show()




def performance_test():
    start = time.time_ns()
    two = [points_at(i) for i in range(1, 3)]
    end = time.time_ns()
    print("Calculating two points. Process lasted", (end - start) * 1e-9, "seconds")
    print(two[1][1800:1900])

    start = time.time_ns()
    p1000 = [points_at(i / 100) for i in range(1001)]
    end = time.time_ns()
    print("Calculating 1000 points. Process lasted", (end - start) * 1e-9, "seconds")



