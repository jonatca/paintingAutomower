#!/usr/bin/env python
import sys
import pyproj
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
    # Define the coordinate reference system for WGS84
    wgs84 = pyproj.CRS("EPSG:4326")
    # Define the coordinate reference system for SWEREF99 TM
    sweref = pyproj.CRS("EPSG:3006")
    transformer = pyproj.Transformer.from_crs(wgs84, sweref, always_xy=True)
    x_start, y_start = transformer.transform(lon_start, lat_start)
    x, y = transformer.transform(lon, lat)
    return x, y 

def lat_lon_to_cartesian(lat, lon):
    x = R * math.radians(lon) * math.cos(math.radians(lat))
    y = R * math.radians(lat)
    return x, y


def plot_data(GPS=True, filename="data.json"):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    angle_north = -np.pi/2 #+ np.pi/4 
    if GPS:
        x_gps = np.zeros(len(data["lat"]))
        y_gps = np.zeros(len(data["lat"]))
        lat = data["lat"]
        lon = data["lon"]
        x_gps_start, y_gps_start = lat_lon_to_cartesian(lat[0], lon[0])
        x_gps_north, y_gps_north = lat_lon_to_cartesian(90, 0)
        delta_x = np.abs(x_gps_north - x_gps_start)
        delta_y = np.abs(y_gps_north - y_gps_start)
        y_north_angle = np.arctan2(delta_x, delta_y)
        print(y_north_angle * 180/np.pi, "y_north_angle")
        # angle_start = np.arctan2(np.mean(y[0:70]) - y[0], np.mean(x[0:70]) - x[0])        
        angle = np.pi/2 - angle_north + y_north_angle# + angle_start
        for i in range(len(lat)):
            x_gps[i], y_gps[i] = lat_lon_to_cartesian(lat[i], lon[i])
            x_gps[i] -= x_gps_start
            y_gps[i] -= y_gps_start
            x_gps[i], y_gps[i] = inverse_change_coord_sys(x_gps[i], y_gps[i],x[0],y[0], angle)
    if GPS:
        plt.plot(x_gps, y_gps, "o-", label="Path GPS", markersize=1)
    plt.plot(x, y, "o-", label="Path Ordometri", markersize=3)
    plt.xlabel("x ")
    plt.ylabel("y ")
    plt.title("Path and Goal")
    plt.legend()
    plt.axis("equal")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    timestamp = int(timestamp.replace("-", ""))
    plt.savefig("plots/plot-latest.png")
    print("Saved plot to plots/plot-", {timestamp}, ".png")
if __name__ == "__main__":
    plot_data(GPS = True, filename="../data/motost.json")
