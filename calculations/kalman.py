import numpy as np

import matplotlib.pyplot as plt
class EKF2D:
    def __init__(self, initial_state, initial_input, initial_covariance, process_noise, measurement_noise):
        self.state = initial_state   #state tre värden: x y theta
        self.input= initial_input  # två värden v  omega
        self.P_k = initial_covariance   # vi använder P_k istället för bara covariance
        self.Q_k = process_noise    # state model noise, cov matrix
        self.measurement_noise = measurement_noise
        self.theta = initial_state[2] ### går det göra så?

    def get_B(self, theta, dt): #räkna ut B matris från värden 
         B = np.array([[np.cos(theta)*dt, 0],
                      [np.sin(theta)*dt, 0
                       [0, dt]]])
         return B
    def predict(self, delta_x, delta_y, dt):
                                                #F = np.array([
                                                #    [1, 0, dt, 0],
                                                #    [0, 1, 0, dt],
                                                #    [0, 0, 1, 0],
                                                #    [0, 0, 0, 1]
                                                #])#gammal kod
        
        #  (1): [x(k), y(k), theta(k)]^T = A * [x(k-1), y(k-1),theta(k-1)]^T + B* [v(k-1), omega(k-1)] + noise

        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B = self.get_B(self.theta, dt)  #np.array([[np.cos(theta)*dt, 0],
                                                # [np.sin(theta)*dt, 0
                                                    #[0, dt]]])
        
        #u = np.array([delta_x, delta_y, delta_x, delta_y])
        # self.state = np.dot(A, self.state) + u
        noise= np.array([[0],[0],[0]]) # ngt ryp av noise får läggas till

        self.state = np.dot(A, self.state) + np.dot(B, self.input) + noise #beräkna state funktion med ekv (1)

        self.P_k = np.dot(A, np.dot(self.P_k, A.T)) + self.Q_k
        ################ predict Klar##############
    def get_state(self):
        return self.state
    
    def update_gps(self, gps_x, gps_y): #fixa funktion sen?
        return self.update(gps_x, gps_y, self.measurement_noise)
    
    def update(self, gps_x, gps_y, position_covariance):
        self.R_k= position_covariance   #covariance matris för mätbara

        H_k = np.array([
            [1, 0, 0 ],
            [0, 1, 0 ],
            [0, 0, 1]
        ])
        yaw =0  ## lägga in data för nya sensorn med vinkel
        y_k = np.array([gps_x, gps_y, yaw]) - np.dot(H_k, self.state)   # Calculate the difference between the actual sensor measurements
                                                                        # at time k minus what the measurement model prmeaedicted 
                                                                        # the sensor measurements would be for the current timestep k.

        S_k = np.dot(H_k, np.dot(self.P_k, H_k.T)) + self.R_k           # R_k=position_covariance
        K_k = np.dot(self.P_k, np.dot(H_k.T, np.linalg.inv(S_k)))       #np.linalg.pinv??

        self.state = self.state + np.dot(K_k, y_k)
        self.P_k = self.P_k - np.dot(K_k, np.dot(H_k, self.P_k))        #uppdatera state covariance för tid k    # np.dot(np.eye(4) - np.dot(K_k, H_k), self.covariance)



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
x_varden=[0]
y_varden=[0]
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
    x_varden.append(state[0])
    y_varden.append(state[1])
    print(f"x_varden={x_varden}, y_varden={y_varden}")
plt.plot(x_varden,y_varden,'ro')
plt.show()