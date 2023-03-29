#!/usr/bin/env python
import sys

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

def convert_to_xy(lat, lon, lat_start, lon_start):
    x = (lat - lat_start) * 111139
    y = (lon - lon_start) * 111139
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
    angle_start *= 0
    angle_diff = np.pi/4 # why does this work? 
    angle_north -=  angle_diff
    x_local = dx * math.cos(angle_north-angle_start) + dy * math.sin(angle_north-angle_start)
    y_local = -dx * math.sin(angle_north-angle_start) + dy * math.cos(angle_north-angle_start)
    return x_local, y_local



def plot_data(GPS=True, filename="data.json"):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    x_start = x[0]
    y_start = y[0]
    x_goal = data["x_goal"]
    y_goal = data["y_goal"]
    angle_start = np.arctan2(np.mean(y[0:70]) - y[0], np.mean(x[0:70]) - x[0])
    print(angle_start, "angle_start1")
    for i in range(len(x)):
        x[i],y[i] = inv_change_coord_sys(x[i], y[i] ,x_start, y_start, angle_start)
    angle_start = np.arctan2(np.mean(y[0:70]) - y[0], np.mean(x[0:70]) - x[0])
    print(angle_start, "angle_start2")
    if GPS:
        x_gps = data["x_gps"]
        y_gps = data["y_gps"]
        lat = data["lat"]
        lon = data["lon"]
        lat_start = data["lat_start"][0]
        lon_start = data["lon_start"][0]
        print(angle_start)
        for i in range(len(lat)):
            x_gps[i], y_gps[i] = convert_to_xy2(lat[i], lon[i], lat_start, lon_start, x_start, y_start, angle_start)
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

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Path and Goal")
    plt.legend()
    plt.axis("equal")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    timestamp = int(timestamp.replace("-", ""))
    plt.savefig("plots/plot-latest.png")
    plt.savefig("plots/plot-%d.png" % timestamp)
    print("Saved plot to plots/plot-", {timestamp}, ".png")


if __name__ == "__main__":
    plot_data(GPS = True, filename="../data/motnorr.json")
