import json
import numpy as np
from calc_velocities import CalcVelocities
from paint import get_paint_order
from comb_cut import get_comb_cut_order
from plot_data import plot_data
from change_goal import change_goal

class Simulate:
    def __init__(self, calc_velocities=None):
        self.max_time = 3000000
        paint_order = get_paint_order()
        # comb_cut_order = get_comb_cut_order()
        self.order = paint_order # valj om comb_cut eller paint order
        self.tot_num_lines = len(self.order)
        self.update_freq = 10  # Hz but doesn't work? stuck at 10 Hz

        self.data = {
            "x": [],
            "y": [],
            "x_goal": [],
            "y_goal": [],
            "x_mid": [],
            "y_mid": [],
            "radius": [],
        }
        self.x = 0
        self.y = 0
        self.x_goal = None
        self.y_goal = None
        self.current_ang = 0
        self.len_vel = 0
        self.ang_vel = 0
        self.radius = None
        self.drive_in_circle = False
        self.reached_goal = False
        if calc_velocities is None:
            self.calc_velocities = CalcVelocities() #TODO add update freq
        else:
            self.calc_velocities = calc_velocities
        change_goal(self, simulation=True)
        self.dt = 1. / self.update_freq
        self.time_elapsed = 0

    def get_square_error(self):
        if self.time_elapsed >= self.max_time - 10: # if the robot did not reach the goal
            return 99999999 
        return self.calc_velocities.square_error_radius**2 * self.time_elapsed**(0.3) * (self.calc_velocities.times_above_tol_ang + 1) ** (1.8)
        

    def drive(self, save_data=False):
        i = 0
        self.save_data = save_data
        while not self.reached_goal and self.time_elapsed < self.max_time:
            # calculates new x and y position based on the last velocities and last position
            position_noise = np.random.normal(loc=0, scale=0.000, size=(2,))
            vel_noise_lin = np.random.normal(loc=0, scale=0.000, size=(1,))
            vel_noise_ang = np.random.normal(loc=0, scale=0.000, size=(1,))
            self.x += (self.len_vel + vel_noise_lin[0]) * np.cos(self.current_ang) * self.dt + position_noise[0]
            self.y += (self.len_vel + vel_noise_lin[0])* np.sin(self.current_ang) * self.dt + position_noise[1]
            self.current_ang += (self.ang_vel + vel_noise_ang[0]) * self.dt
            self.len_vel, self.ang_vel = self.calc_velocities.calc_vel(
                self.current_ang, self.x, self.y
            )
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
            if self.len_vel == 0 and self.ang_vel == 0:
                change_goal(self, simulation=True)
            self.time_elapsed += self.dt
            if i % 200000== 0 and save_data: #to plot every 2 seconds
                self.stop()
            i+=1
        if save_data:
            self.stop()


    def stop(self):
        self._prints()
        filename = "simulatedData.json"
        with open(filename, "w") as json_file:
            json.dump(self.data, json_file)
        plot_data(GPS = False, filename = filename)
        pass

    # TODO Rename this here and in `stop`
    def _prints(self):
        print("This trip whould have taken", round(self.time_elapsed, 4), "seconds")
        print("the sqaure error was", round(self.get_square_error(), 4))
        print("the times above tolerance was", round(self.calc_velocities.times_above_tol_ang, 4))
        print("sqare error radius was", round(self.calc_velocities.square_error_radius, 4))

    #if ctrl+c is pressed, run self.stop()
    def ctrlc_shutdown(self, signum, frame):
        self.stop()
        print("Shutting down")


if __name__ == "__main__":
    sim = Simulate()
    sim.drive(True)
