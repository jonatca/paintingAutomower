import numpy as np


class PIDController:
    def __init__(self, x_start, y_start, x_goal, y_goal, update_freq):
        self.Kp_l = 0.5
        self.Ki_l = 0.01
        self.Kd_l = 0.2
        self.Kp_a = 0.8
        self.Ki_a = 0.01
        self.Kd_a = 0.2
        self.integral_l = 0
        self.integral_a = 0
        self.prev_error_l = 0
        self.prev_error_a = 0
        self.x_start = x_start
        self.y_start = y_start
        self.x_goal = x_goal
        self.y_goal = y_goal
        self.update_time = 1.0 / update_freq

    def calc_vel(self, current_angle, x, y):
        # Calculate linear velocity
        dist_to_goal = np.sqrt((self.x_goal - x) ** 2 + (self.y_goal - y) ** 2)
        error_l = dist_to_goal
        self.integral_l += error_l * self.update_time
        derivative_l = (error_l - self.prev_error_l) / self.update_time
        output_l = (
            self.Kp_l * error_l + self.Ki_l * self.integral_l + self.Kd_l * derivative_l
        )
        output_l = np.clip(output_l, -0.3, 0.3)
        self.prev_error_l = error_l

        # Calculate angular velocity
        goal_angle = np.arctan2(self.y_goal - y, self.x_goal - x)
        error_a = goal_angle - current_angle
        if error_a > np.pi:
            error_a -= 2 * np.pi
        elif error_a < -np.pi:
            error_a += 2 * np.pi
        self.integral_a += error_a * self.update_time
        derivative_a = (error_a - self.prev_error_a) / self.update_time
        output_a = (
            self.Kp_a * error_a + self.Ki_a * self.integral_a + self.Kd_a * derivative_a
        )
        output_a = np.clip(output_a, -0.8, 0.8)
        self.prev_error_a = error_a

        return output_a, output_l
