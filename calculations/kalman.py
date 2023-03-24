import numpy as np

class EKF2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        self.state = initial_state
        self.covariance = initial_covariance
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

    def predict(self, delta_x, delta_y, dt):
        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        u = np.array([delta_x, delta_y, delta_x, delta_y])

        self.state = np.dot(F, self.state) + u
        self.covariance = np.dot(F, np.dot(self.covariance, F.T)) + self.process_noise
    def get_state(self):
        return self.state
    
    def update_gps(self, gps_x, gps_y):
        return self.update(gps_x, gps_y, self.measurement_noise)
    
    def update(self, gps_x, gps_y, position_covariance):
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        y = np.array([gps_x, gps_y]) - np.dot(H, self.state)
        S = np.dot(H, np.dot(self.covariance, H.T)) + position_covariance
        K = np.dot(self.covariance, np.dot(H.T, np.linalg.inv(S)))

        self.state = self.state + np.dot(K, y)
        self.covariance = np.dot(np.eye(4) - np.dot(K, H), self.covariance)

import numpy as np

# Initialize the EKF
initial_state = np.array([0, 0, 0, 0])
initial_covariance = np.eye(4) * 0.1
process_noise = np.eye(4) * 0.001
position_covariance = np.eye(2) * 0.01

ekf = EKF2D(initial_state, initial_covariance, process_noise, position_covariance)

# Simulate the robot's motion with odometry and GPS measurements
odometry_data = [
    # (delta_x, delta_y, dt)
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
    (1, 0, 0.1),
]

gps_data = [
    # (gps_x, gps_y)
    (9.5, 0.2),
]

for i, (delta_x, delta_y, dt) in enumerate(odometry_data):
    # Predict the robot's position using odometry
    ekf.predict(delta_x, delta_y, dt)

    # If a GPS measurement is available, update the state
    if i % 10 == 9:  # GPS data
        gps_measurement = gps_data.pop(0)  # Get the next GPS measurement
        ekf.update_gps(*gps_measurement)

    # Print the current estimated position
    state = ekf.get_state()
    print(f"Estimated position at time step {i + 1}: x={state[0]:.2f}, y={state[1]:.2f}")