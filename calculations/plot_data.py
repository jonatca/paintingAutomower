#!/usr/bin/env python
import sys
# import pyproj
sys.path.append("/home/kandidatarbete/450/src/calculations")
import json
import matplotlib
import datetime
matplotlib.use(
    "Agg"
)  # Set the backend to Agg (non-interactive) to avoid display errors
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import numpy as np

R = 6371000  # Earth's radius in meters

def inv_change_coord_sys(x_goal, y_goal,x_start, y_start, init_angle):  # global coordinates => automowers relative coordinates
    x_goal_prim = (
        (x_goal - x_start) * np.cos(init_angle)
        + (y_goal - y_start) * np.sin(init_angle)
    )
    y_goal_prim = (
        -(x_goal - x_start) * np.sin(init_angle)
        + (y_goal - y_start) * np.cos(init_angle)
    )
    return x_goal_prim, y_goal_prim  # automowers relative coordinates

def inverse_change_coord_sys(x_local, y_local, x_start, y_start, init_angle):
    x_global = x_start + x_local * np.cos(init_angle) + y_local * np.sin(init_angle)
    y_global = y_start - x_local * np.sin(init_angle) + y_local * np.cos(init_angle)
    return x_global, y_global

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

def convert_to_xy(lat, lon, lat_start, lon_start):
    # # Define the coordinate reference system for WGS84
    # wgs84 = pyproj.CRS("EPSG:4326")
    # # Define the coordinate reference system for SWEREF99 TM
    # sweref = pyproj.CRS("EPSG:3006")
    # transformer = pyproj.Transformer.from_crs(wgs84, sweref, always_xy=True)
    # x_start, y_start = transformer.transform(lon_start, lat_start)
    # x, y = transformer.transform(lon, lat)
    # x -= x_start
    # y -= y_start

    # x = (lat - lat_start) * 111139
    # y = (lon - lon_start) * 111139
    return
    return x, y 

def convert_to_xy2(lat_start, lon_start, lat, lon, x_start, y_start, angle_start):
    x_gps_start, y_gps_start = lat_lon_to_cartesian(lat_start, lon_start)
    x_gps,y_gps = lat_lon_to_cartesian(lat, lon)
    angle_north = 0 #The angle of the robot's x-axis with respect to the true north (in degrees
    x_local, y_local = global_to_local(x_gps, y_gps, x_gps_start, y_gps_start, angle_north, x_start, y_start, angle_start)
    return x_local, y_local

def lat_lon_to_cartesian(lat, lon):
    x = R * math.radians(lon) * math.cos(math.radians(lat))
    y = R * math.radians(lat)
    return x, y

def global_to_local(x_gps, y_gps, x_gps_start, y_gps_start, angle_north, x_start, y_start, angle_start):
    dx = x_gps - x_gps_start
    dy = y_gps - y_gps_start
    # angle_start *= 0
    # angle_diff = np.pi/4 # why does this work? 
    # angle_north -=  angle_diff
    x_local = x_start + dx * math.cos(angle_north-angle_start) + dy * math.sin(angle_north-angle_start)
    y_local = y_start -dx * math.sin(angle_north-angle_start) + dy * math.cos(angle_north-angle_start)
    return x_local, y_local


def plot_data(GPS=True, filename="data.json"):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    print(filename)
    x = data["x"]
    y = data["y"]
    x_start = x[0]
    y_start = y[0]
    x_goal = data["x_goal"]
    y_goal = data["y_goal"]
    angle_start = np.arctan2(np.mean(y[0:70]) - y[0], np.mean(x[0:70]) - x[0])
    print(angle_start, "angle_start1")
    # for i in range(len(x)):
        # x[i],y[i] = inv_change_coord_sys(x[i], y[i] ,x_start, y_start, angle_start)
    angle_start = np.arctan2(np.mean(y[0:70]) - y[0], np.mean(x[0:70]) - x[0])
    angle_north = -np.pi/2
    print(angle_start, "angle_start2")
    if GPS:
        # x_gps = data["x_gps"]
        # y_gps = data["y_gps"]
        x_gps = np.zeros(len(data["lat"]))
        y_gps = np.zeros(len(data["lat"]))
        lat = data["lat"]
        lon = data["lon"]
        lat_start = data["lat_start"][0]
        lon_start = data["lon_start"][0]
        # x_gps[0], y_gps[0] = convert_to_xy(lat[0], lon[0], 0, 0)
        x_gps_start, y_gps_start = lat_lon_to_cartesian(lat[0], lon[0])
        delta_x, delta_y = lat_lon_to_cartesian(lat[0], 90 - lon[0])
        y_north_angle = np.arctan2(delta_x, delta_y)
        print(y_north_angle * 180/np.pi, "y_north_angle")
        angle = np.pi/2 - angle_north + y_north_angle 
        x_gps_start, y_gps_start = inverse_change_coord_sys(x_gps_start, y_gps_start, 0, 0, angle)
        for i in range(len(lat)):
            # x_gps[i], y_gps[i] = convert_to_xy2(lat[i], lon[i], lat_start, lon_start, x_start, y_start, angle_start)
            # x_gps[i], y_gps[i] = convert_to_xy(lat[i], lon[i], lat_start, lon_start)
            # x_gps[i], y_gps[i] = lat_lon_to_cartesian(lat[i], lon[i])

            x_gps[i], y_gps[i] = lat_lon_to_cartesian(lat[i], lon[i])
            print(x_gps[i], y_gps[i], "x_gps[i], y_gps[i]")
            print(x_gps_start, y_gps_start, "x_gps_start, y_gps_start")
            print(x_gps[i] - x_gps_start, y_gps[i] - y_gps_start, "x_gps[i] - x_gps_start, y_gps[i] - y_gps_start")
            x_gps[i], y_gps[i] = inverse_change_coord_sys(x_gps[i], y_gps[i],x_gps_start, y_gps_start, angle)

            # x_gps[i], y_gps[i] -= x_gps_start, y_gps_start # type: ignore
            # x_gps[i] -= x_gps_start 
            # y_gps[i] -= y_gps_start 
    try:
        radius = data["radius"][0]
        x_mid = data["x_mid"][0]
        y_mid = data["y_mid"][0]
        # Add the optimal circle
        circle = Circle((x_mid, y_mid), radius, edgecolor="red", facecolor="none")
        plt.gca().add_patch(circle)
    except:
        pass
    plt.plot(x, y, "o-", label="Path Ordometri", markersize=3)
    plt.plot(x_goal, y_goal, "rx", markersize=3, label="Goal")
    if GPS:
        plt.plot(x_gps, y_gps, "o-", label="Path GPS", markersize=1)
    # print(np.arctan2(np.mean(x_gps[0:70]) - y[0], np.mean(y_gps[0:70]) - x[0]), "angle_start3")
    plt.xlabel("x ")
    plt.ylabel("y ")
    plt.title("Path and Goal")
    plt.legend()
    plt.axis("equal")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    timestamp = int(timestamp.replace("-", ""))

    # formatter = plt.FuncFormatter(lambda x, pos: f'{x / 10**6:.0f}') # type: ignore
    # plt.gca().xaxis.set_major_formatter(formatter)
    # plt.gca().yaxis.set_major_formatter(formatter)

    # # Set x and y axis limits
    # plt.xlim(2 * 10**5, 2 * 10**7)
    # plt.ylim(2 * 10**5, 2 * 10**7)
    plt.savefig("plots/plot-latest.png")
    # plt.savefig("plots/plot-%d.png" % timestamp)
    print("Saved plot to plots/plot-", {timestamp}, ".png")


if __name__ == "__main__":
    plot_data(GPS = True, filename="../data/motost.json")
