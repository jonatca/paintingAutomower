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
from coord_sys_trans import *

def plot_data(GPS=True, filename="data.json"):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    x_min = min(x)
    y_min = min(y)
    x_max = max(x)
    y_max = max(y)
    if GPS and True:
        x_gps = []
        y_gps = []
        for i in range(len(data["lat"])):
            lat = data["lat"][i]
            lon = data["lon"][i]
            x_gps_temp, y_gps_temp = convert_lat_lon_to_utm(lat, lon)
            x_gps.append(x_gps_temp)
            y_gps.append(y_gps_temp)
        print("x_gps: ", x_gps)
        print("y_gps: ", y_gps)
        plt.plot(x_gps, y_gps, "o-", label="Path GPS", markersize=20)
        x_min = min(min(x), min(x_gps))
        x_max = max(max(x), max(x_gps))
        y_min = min(min(y), min(y_gps))
        y_max = max(max(y), max(y_gps))
    plt.plot(x, y, "o-", label="Path Ordometri", markersize=3)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    print("x_min: ", x_min, " x_max: ", x_max, " y_min: ", y_min, " y_max: ", y_max)
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