import json
import numpy as np
from calc_velocities import CalcVelocities
from paint import get_paint_order
from comb_cut import get_comb_cut_order
from plot_data import plot_data


class Simulate:
    def __init__(self, pid=None):
        self.max_time = 1500
        paint_order = get_paint_order()
        comb_cut_order = get_comb_cut_order()
        self.order = paint_order # välj om comb_cut eller paint order
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
        if pid is None:
            self.pid = CalcVelocities() #TODO add update freq
        else:
            self.pid = pid
        self.change_goal()
        self.dt = 1 / self.update_freq
        self.time_elapsed = 0

    def get_square_error(self):
        if self.time_elapsed >= self.max_time - 10: # if the robot did not reach the goal
            return 99999999 
        return self.pid.square_error_radius**2 * self.time_elapsed**(0.3) * (self.pid.times_above_tol_ang + 1) ** (1.8)
        

    def drive(self, save_data=False):
        i = 0
        while not self.reached_goal and self.time_elapsed < self.max_time:
            # calculates new x and y position based on the last velocities and last position
            position_noise = np.random.normal(loc=0, scale=0.000, size=(2,))
            vel_noise_lin = np.random.normal(loc=0, scale=0.000, size=(1,))
            vel_noise_ang = np.random.normal(loc=0, scale=0.000, size=(1,))
            self.x += (self.len_vel + vel_noise_lin[0]) * np.cos(self.current_ang) * self.dt + position_noise[0]
            self.y += (self.len_vel + vel_noise_lin[0])* np.sin(self.current_ang) * self.dt + position_noise[1]
            self.current_ang += (self.ang_vel + vel_noise_ang[0]) * self.dt
            self.len_vel, self.ang_vel = self.pid.calc_vel(
                self.current_ang, self.x, self.y
            )
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
            if self.len_vel == 0 and self.ang_vel == 0:
                self.change_goal()
            self.time_elapsed += self.dt
            if i % 20== 0: #to plot every 2 seconds
                self.stop()
            i+=1
        if save_data:
            self.stop()


    def stop(self):
        # print("This trip whould have taken", round(self.time_elapsed, 4), "seconds")
        # print("the sqaure error was", round(self.get_square_error(), 4))
        # print("the times above tolerance was", round(self.pid.times_above_tol_ang, 4))
        # print("sqare error radius was", round(self.pid.square_error_radius, 4))
        # print("This trip whould have taken", round(self.time_elapsed, 4), "seconds")
        # print("the sqaure error was", round(self.get_square_error(), 4))
        # print("the times above tolerance was", round(self.pid.times_above_tol_ang, 4))
        # print("sqare error radius was", round(self.pid.square_error_radius, 4))
        # print("position", self.x, self.y)
        filename = "simulatedData.json"
        with open(filename, "w") as json_file:
            json.dump(self.data, json_file)
        plot_data(GPS = False, filename = filename)
        pass

    ##if ctrl+c is pressed, run self.stop()
    def ctrlc_shutdown(self, signum, frame):
        self.stop()
        print("Shutting down")
   
    def change_goal(self):
        # print(self.order, "order")
        if len(self.order) > 0: #if there are still lines to drive
            self.pid.not_in_circle() #always assume not a circle
            # if "start" in self.order[0]: #TODO remove this if statement
            #     self.x_goal, self.y_goal = self.order[0]["start"]
            #     self.order[0].pop("start")
            if "end" in self.order[0]:
                self.drive_in_circle = False
                if self.order[0]["type"] == "circle":  # start to go in circle
                    self.radius = self.order[0]["radius"]
                    self.x_mid, self.y_mid = self.order[0]["center"]
                    direction = self.order[0]["direction"]
                    self.drive_in_circle = True
                    self.pid.set_circle_params(self.radius, self.x_mid, self.y_mid, direction)
                self.x_goal, self.y_goal = self.order[0]["end"]
                self.order[0].pop("end") 
                # self.order.pop(0)
            elif "after_end" in self.order[0]:
                i = 0
                while len(self.order[i]["after_end"]) > 0:
                    go_to_line = self.order[i]["after_end"].pop(0)
                    self.order.insert(i, go_to_line) 
                    i += 1
                self.order.pop(i)
                self.change_goal()
            else: # if has no after_end (probably was a after_end) 
                self.order.pop(0)
                self.change_goal()
            self.data["x_goal"].append(self.x_goal)
            self.data["y_goal"].append(self.y_goal)
            if self.drive_in_circle:
                self.data["radius"].append(self.radius)
                self.data["x_mid"].append(self.x_mid)
                self.data["y_mid"].append(self.y_mid)
            # print("changed goal to", self.x_goal, self.y_goal)
            # print("changed goal to", self.x_goal, self.y_goal)
            self.pid.set_goal_coords(self.x_goal, self.y_goal)
            print("The process has ", round(len(self.order) / self.tot_num_lines * 100, 1), "procent left")
        else:
            self.reached_goal = True


if __name__ == "__main__":
    sim = Simulate()
    sim.drive(True)
