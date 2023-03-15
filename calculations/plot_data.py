import json
import matplotlib

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
radius = data["radius"]
x_mid = data["x_mid"]
y_mid = data["y_mid"]

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

# Save the plot to a file instead of displaying it on the screen
plt.savefig("plot.png")
