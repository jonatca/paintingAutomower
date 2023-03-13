import numpy as np


class PID:
    def __init__(self, x_start, y_start, x_goal, y_goal, update_freq):
        self.Kp_l = 0.5
        self.Kp_a = 0.5
        self.x_start = x_start
        self.y_start = y_start
        self.x_goal = x_goal
        self.y_goal = y_goal
        self.update_time = 1.0 / update_freq

    def calc_vel(self, current_angle, x, y):
        # Calculate linear velocity
        error_lin = np.sqrt((self.x_goal - x) ** 2 + (self.y_goal - y) ** 2)
        vel_lin = self.Kp_l * error_lin
        vel_lin = np.clip(vel_lin, -0.3, 0.3)
        self.prev_error_lin = error_lin

        # Calculate angular velocity
        goal_angle = np.arctan2(self.y_goal - y, self.x_goal - x)
        error_ang = goal_angle - current_angle
        error_ang = (error_ang + np.pi) % (2 * np.pi) - np.pi
        # vel_ang = self.Kp_a * error_ang
        # vel_ang = np.clip(vel_ang, -0.8, 0.8)
        vel_ang = np.sign(error_ang) * 0.2
        if error_lin < 0.1:
            vel_lin = 0
            vel_ang = 0
        if np.abs(error_ang) > 0.3:
            vel_lin = 0
        print(
            "error_lin: ",
            round(error_lin, 2),
            "vel_lin: ",
            round(vel_lin, 2),
        )
        print(
            "current_angle",
            round(current_angle, 2),
            "goal_angle",
            round(goal_angle, 2),
            "error_ang: ",
            round(error_ang, 2),
            "vel_ang: ",
            round(vel_ang, 2),
        )
        return vel_lin, vel_ang
