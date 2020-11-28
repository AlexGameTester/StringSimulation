from math_simulator import MathematicalSimulator
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    math_sim = MathematicalSimulator(None)

    finished = False
    while not finished:
        finished = math_sim._fourier_solver.calculate_next()
    points_at = math_sim._fourier_solver.get_points_function()
    x = math_sim._initial_positions_x
    plt.plot(x, points_at(0.345))
    plt.plot(x, points_at(8.345))
    plt.plot(x, points_at(12.35))
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



