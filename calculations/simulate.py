import json
import numpy as np
from calc_velocities import CalcVelocities
from paint import get_paint_order
from comb_cut import get_comb_cut_order
from plot_data import plot_data


class Simulate:
    def __init__(self):
        paint_order = get_paint_order()
        comb_cut_order = get_comb_cut_order()
        self.order = paint_order
        self.update_freq = 10.0  # Hz but doesn't work? stuck at 10 Hz
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
        self.current_ang = 0
        self.len_vel = 0
        self.ang_vel = 0
        self.radius = None
        self.drive_in_circle = False
        self.reached_goal = False
        self.pid = CalcVelocities(self.update_freq)
        self.change_goal()
        self.dt = 1 / self.update_freq
        self.time_elapsed = 0
        self.max_time = 4000

    def drive(self):
        while not self.reached_goal and self.time_elapsed < self.max_time:
            # calculates new x and y position based on the last velocities and last position
            self.x += self.len_vel * np.cos(self.current_ang) * self.dt
            self.y += self.len_vel * np.sin(self.current_ang) * self.dt
            self.current_ang += self.ang_vel * self.dt
            self.len_vel, self.ang_vel = self.pid.calc_vel(
                self.current_ang, self.x, self.y
            )
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
            if self.len_vel == 0 and self.ang_vel == 0:
                self.change_goal()
            self.time_elapsed += self.dt
        self.stop()

    def stop(self):
        print("Stopping")
        print("This trip whould have taken", round(self.time_elapsed, 4), "seconds")
        with open("data.json", "w") as json_file:
            json.dump(self.data, json_file)
        plot_data()

    ##if ctrl+c is pressed, run self.stop()
    def ctrlc_shutdown(self, signum, frame):
        self.stop()
        print("Shutting down")
        raise KeyboardInterrupt

    def change_goal(self):
        if len(self.order) > 0:
            if "start" in self.order[0]:
                print(self.order[0])
                self.x_goal, self.y_goal = self.order[0]["start"]
                self.order[0].pop("start")
            elif "end" in self.order[0]:
                print("end")
                self.drive_in_circle = False
                print(self.order[0])
                if self.order[0]["type"] == "circle":  # start to go in circle
                    print("start to go in circle")
                    self.radius = self.order[0]["radius"]
                    self.x_mid, self.y_mid = self.order[0]["center"]
                    self.drive_in_circle = True
                    self.pid.set_circle_params(self.radius, self.x_mid, self.y_mid)
                self.x_goal, self.y_goal = self.order[0]["end"]
                self.order[0].pop("end")  # unnecessary
                self.order.pop(0)  # removes the line from the list
            else:
                self.reached_goal = True
                raise ValueError("Invalid line")
            self.data["x_goal"].append(self.x_goal)
            self.data["y_goal"].append(self.y_goal)
            if self.drive_in_circle:
                self.data["radius"].append(self.radius)
                self.data["x_mid"].append(self.x_mid)
                self.data["y_mid"].append(self.y_mid)
            print("changed goal to", self.x_goal, self.y_goal)
            self.pid.set_goal_coords(self.x_goal, self.y_goal)
        else:
            self.reached_goal = True


if __name__ == "__main__":
    sim = Simulate()
    sim.drive()
