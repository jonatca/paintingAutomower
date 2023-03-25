# from pyproj import Proj, Transformer
import numpy as np
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



# def latlon_to_utm(lat, lon, zone_number=None, zone_letter=None):
#     if zone_number is None or zone_letter is None:
#         proj_utm = Proj(proj='utm', ellps='WGS84', preserve_units=False)
#         x, y = proj_utm(lon, lat)
#         return x, y
#     else:
#         proj_utm = Proj(proj='utm', zone=zone_number, zone_letter=zone_letter, ellps='WGS84', preserve_units=False)
#         x, y = proj_utm(lon, lat)
#         return x, y

