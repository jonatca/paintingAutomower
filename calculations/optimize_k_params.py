import numpy as np
import pyswarms as ps
from calc_velocities import CalcVelocities
from simulate import Simulate

def optimize_pid(params):
    Kp, Kp90 = params
    # Instantiate CalcVelocities with the PID parameters
    pid_controller = CalcVelocities(Kp_circle=Kp, Kp90_circle=Kp90)
    # Instantiate Simulate class with the custom PID controller
    sim = Simulate(pid=pid_controller)
    # Run the simulation
    sim.drive()
    return sim.get_square_error()


def cost_function(params_array):
    return np.array([optimize_pid(params) for params in params_array])


# Set the bounds for the PID parameters (Kp, Ki, Kd, Kp90)
lower_bounds = [19, 20]
upper_bounds = [400, 100]
options = {"c1": 0.5, "c2": 0.3, "w": 0.9}
optimizer = ps.single.GlobalBestPSO(
    n_particles=30, dimensions=2, options=options, bounds=(lower_bounds, upper_bounds)
)
# Perform optimization
cost, pos = optimizer.optimize(cost_function, iters=50)
print("Optimized Kp90:", pos[0], "Optimized Kp:", pos[1])
pid = CalcVelocities(Kp_circle=pos[0], Kp90_circle=pos[1]) 
sim = Simulate(pid=pid)
sim.drive(True)
