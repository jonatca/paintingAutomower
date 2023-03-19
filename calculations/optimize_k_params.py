import numpy as np
import pyswarms as ps
from calc_velocities import CalcVelocities
from simulate import Simulate

def optimize_pid(params):
    Kp, Ki, Kd, Kp90 = params
    # Instantiate CalcVelocities with the PID parameters
    pid_controller = CalcVelocities(Kp_circle=Kp, Ki_circle=Ki, Kd_circle=Kd, Kp90_circle=Kp90)
    # Instantiate Simulate class with the custom PID controller
    sim = Simulate(pid=pid_controller)
    # Run the simulation
    sim.drive()
    # Get the squared error
    square_error = sim.get_square_error()
    return square_error


def cost_function(params_array):
    cost = np.array([optimize_pid(params) for params in params_array])
    return cost


# Set the bounds for the PID parameters (Kp, Ki, Kd, Kp90)
lower_bounds = [60, 4, 7, 15]
upper_bounds = [500, 9, 14, 23]
options = {"c1": 0.5, "c2": 0.3, "w": 0.9}
optimizer = ps.single.GlobalBestPSO(
    n_particles=30, dimensions=4, options=options, bounds=(lower_bounds, upper_bounds)
)
# Perform optimization
cost, pos = optimizer.optimize(cost_function, iters=1000)
print("Optimized Kp:", pos[0], "Optimized Ki:", pos[1], "Optimized Kd:", pos[2], "Optimized Kp90:", pos[3])
pid = CalcVelocities(Kp_circle=pos[0], Ki_circle=pos[1], Kd_circle=pos[2], Kp90_circle=pos[3])
sim = Simulate(pid=pid)
sim.drive(True)
