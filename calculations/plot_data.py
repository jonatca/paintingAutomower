import json
import matplotlib
import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

matplotlib.use(
    "Agg"
)  # Set the backend to Agg (non-interactive) to avoid display errors


def plot_data():
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
    x = data["x"]
    y = data["y"]
    x_goal = data["x_goal"]
    y_goal = data["y_goal"]
    try:
        radius = data["radius"][0]
        x_mid = data["x_mid"][0]
        y_mid = data["y_mid"][0]
        # Add the optimal circle
        circle = Circle((x_mid, y_mid), radius, edgecolor="blue", facecolor="none")
        plt.gca().add_patch(circle)
    except:
        pass
    plt.plot(x, y, "o-", label="Path")
    plt.plot(x_goal, y_goal, "rx", markersize=10, label="Goal")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Path and Goal")
    plt.legend()
    plt.axis("equal")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    plt.savefig("plots/plot-", {timestamp}, ".png")
    plt.savefig("plots/plot-latest.png")
    print("Saved plot to plots/plot-", {timestamp}, ".png")


if __name__ == "__main__":
    plot_data()
