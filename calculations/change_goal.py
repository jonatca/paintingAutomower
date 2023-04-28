# from coord_sys_trans import change_coord_sys
import numpy as np 
from imu import *

from coord_sys_trans import *
def change_goal(self, simulation = False):
    # print(simulation)
    if len(self.order) > 0:
        # self.angle_north = get_yaw_angle() 
        print("angle north", self.angle_north)
        # print("current_angle", self.current_angle)
        self.calc_velocities.not_in_circle()
        if "end" in self.order[0]:
            _handle_end(self)
            _update_data(self, simulation)
        elif "after_end" in self.order[0]:
            _handle_after_end(self, simulation)
        else:
            _handle_no_end(self, simulation)
        # _print_progress(self)
    else:
        self.reached_goal = True

def _handle_end(self):
    self.drive_in_circle = False
    if self.order[0]["type"] == "circle":
        self.drive_in_circle = True
        self.radius = self.order[0]["radius"]
        self.x_mid, self.y_mid = self.order[0]["center"]
        direction = self.order[0]["direction"]
        self.calc_velocities.set_circle_params(self.radius, self.x_mid, self.y_mid, direction)
    self.x_goal, self.y_goal = self.order[0]["end"]
    self.order[0].pop("end")

def _handle_after_end(self, simulation):
    i = 0 # index of the line that has the after_end, which is the first line in the order at first
    while len(self.order[i]["after_end"]) > 0: # while there are lines after the line that has the after_end
        go_to_line = self.order[i]["after_end"].pop(0)
        self.order.insert(i, go_to_line) 
        i += 1 # the index of the line that has the after_end is now the next line
    self.order.pop(i)
    change_goal(self, simulation)

def _handle_no_end(self, simulation):
    self.order.pop(0) # remove the line that has lines to go to anymore
    change_goal(self, simulation)

def _update_data(self, simulation):
    if not simulation:
        self.x_goal, self.y_goal = change_coord_sys(self, self.x_goal, self.y_goal)
        # if self.drive_in_circle:
            # self.x_mid, self.y_mid = change_coord_sys(self, self.x_mid, self.y_mid)
    self.data["x_goal"].append(self.x_goal)
    self.data["y_goal"].append(self.y_goal)
    if self.drive_in_circle:
        self.data["radius"].append(self.radius)
        self.data["x_mid"].append(self.x_mid)
        self.data["y_mid"].append(self.y_mid)
    self.calc_velocities.set_goal_coords(self.x_goal, self.y_goal)

def change_coord_sys(
    self, x_goal_prim, y_goal_prim
):  # automowers relative coordinates => global coordinates
    x_goal_automower = (
        self.x_start_automower
        + x_goal_prim * np.cos(self.init_angle)
        - y_goal_prim * np.sin(self.init_angle)
    )
    y_goal_automower = (
        self.y_start_automower
        + x_goal_prim * np.sin(self.init_angle)
        + y_goal_prim * np.cos(self.init_angle)
    )
    print("x_goal_automower: ", x_goal_automower, "y_goal_automower: ", y_goal_automower)
    print("self.x_start", self.x_start, "self.y_start", self.y_start)
    x_goal, y_goal = convert_automower_to_utm(self, x_goal_automower, y_goal_automower)
    print("changed goal to: ", x_goal, y_goal)
    return x_goal, y_goal  # utm coords 

def _print_progress(self):
    progress = round(len(self.order) / self.tot_num_lines * 100, 1)
    print("The process has", progress, "percent left.")