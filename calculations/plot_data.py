import json
import matplotlib
import datetime
matplotlib.use(
    "Agg"
)  # Set the backend to Agg (non-interactive) to avoid display errors
import matplotlib.pyplot as plt
from matplotlib.patches import Circle



def plot_data(GPS=True, simulated=False):
    matplotlib.use(
        "Agg"
    )  # Set the backend to Agg (non-interactive) to avoid display errors
    file = "data.json"
    if simulated:
        file = "simulatedData.json"
    with open(file, "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    x_goal = data["x_goal"]
    y_goal = data["y_goal"]
    if GPS:
        x_gps = data["x_gps"]
        y_gps = data["x_gps"]
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
    # plt.savefig("plots/plot-%d.png" % timestamp)
    # print("Saved plot to plots/plot-", {timestamp}, ".png")


if __name__ == "__main__":
    plot_data()
