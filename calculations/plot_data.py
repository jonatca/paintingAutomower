import json
import matplotlib
import datetime

matplotlib.use(
    "Agg"
)  # Set the backend to Agg (non-interactive) to avoid display errors
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Read the JSON file
with open("data.json", "r") as json_file:
    data = json.load(json_file)

# Extract the data
x = data["x"]
y = data["y"]
x_goal = data["x_goal"]
y_goal = data["y_goal"]
radius = data["radius"][0]
x_mid = data["x_mid"][0]
y_mid = data["y_mid"][0]

# Plot the data
plt.plot(x, y, "o-", label="Path")
plt.plot(x_goal, y_goal, "rx", markersize=10, label="Goal")

# Add the circle
circle = Circle((x_mid, y_mid), radius, edgecolor="blue", facecolor="none")
plt.gca().add_patch(circle)

plt.xlabel("x")
plt.ylabel("z")
plt.title("Path and Goal")
plt.legend()

# Make axes equal
plt.axis("equal")

# Get the current timestamp and format it
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Save the plot to a file with a unique name in the 'plots' folder
plt.savefig(f"plots/plot-{timestamp}.png")
