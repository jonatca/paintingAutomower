# from pyproj import Proj, Transformer
import numpy as np
import utm
import math
def convert_to_xy(lat, lon, lat_start, lon_start):
    x = (lat - lat_start) * 111139
    y = (lon - lon_start) * 111139
    return x, y 

def change_coord_sys(
    x_goal_prim, y_goal_prim, x_start, y_start, init_angle
):  # automowers relative coordinates => global coordinates 
    x_goal = (
        x_start
        + x_goal_prim * np.cos(init_angle)
        - y_goal_prim * np.sin(init_angle)
    )
    y_goal = (
        y_start
        + x_goal_prim * np.sin(init_angle)
        + y_goal_prim * np.cos(init_angle)
    )
    return x_goal, y_goal  # automowers global coordinates

def inverse_change_coord_sys(x_goal, y_goal, x_start, y_start, init_angle): #TODO test this function. Then we can use it in plot
    x_goal_prim = (
        (x_goal - x_start) * np.cos(init_angle)
        + (y_goal - y_start) * np.sin(init_angle)
    )
    y_goal_prim = (
        -(x_goal - x_start) * np.sin(init_angle)
        + (y_goal - y_start) * np.cos(init_angle)
    )
    return x_goal_prim, y_goal_prim  # automowers relative coordinates


def convert_automower_to_utm(self, x_automower, y_automower):
    x_utm = self.x_start - x_automower*math.sin(self.angle_north) - y_automower*math.cos(self.angle_north)
    y_utm = self.y_start + x_automower*math.cos(self.angle_north) - y_automower*math.sin(self.angle_north)
    return x_utm, y_utm

def convert_lat_lon_to_utm(lat, lon):
    east, north, number, letter = utm.from_latlon(lat, lon)
    print(north)
    return east, north
