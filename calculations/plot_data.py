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


def convert_to_xy(lat, lon, lat_start, lon_start):
    x = (lat - lat_start) * 111139
    y = (lon - lon_start) * 111139
    return x, y 

def plot_data(GPS=True, filename="data.json"):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    x_goal = data["x_goal"]
    y_goal = data["y_goal"]
    if GPS:
        x_gps = data["x_gps"]
        y_gps = data["y_gps"]
        lat = data["lat"]
        lon = data["lon"]
        lat_start = data["lat_start"][0]
        lon_start = data["lon_start"][0]
        for i in range(len(lat)):
            x_gps[i], y_gps[i] = convert_to_xy(lat[i], lon[i], lat_start, lon_start) 
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
