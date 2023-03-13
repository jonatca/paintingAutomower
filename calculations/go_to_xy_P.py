import numpy as np


class P:
    def __init__(self, x_start, y_start, x_goal, y_goal, update_freq):
        self.Kp_l = 0.7
        self.Kp_a = 0.8
        self.x_start = x_start
        self.y_start = y_start
        self.x_goal = x_goal
        self.y_goal = y_goal
        self.update_time = 1.0 / update_freq
        self.tol_lin = 0.05
        self.tol_ang = 0.2
        self.current_ang = None
        self.error_lin = None
        self.vel_lin = None
        self.x = None
        self.y = None
        self.prev_error_lin = 0
        self.max_vel_lin = 0.3
        self.max_vel_ang = 0.8

    def calc_vel(self, current_ang, x, y):
        self.current_ang = current_ang
        self.x = x
        self.y = y
        self.error_lin = np.sqrt(
            (self.x_goal - self.x) ** 2 + (self.y_goal - self.y) ** 2
        )
        self.vel_lin = self.Kp_l * self.error_lin
        self.vel_lin = np.clip(self.vel_lin, -self.max_vel_lin, self.max_vel_lin)
        self.prev_error_lin = self.error_lin

        # Calculate angular velocity
        self.goal_ang = np.arctan2(self.y_goal - self.y, self.x_goal - self.x)
        self.error_ang = self.goal_ang - self.current_ang
        self.error_ang = (self.error_ang + np.pi) % (2 * np.pi) - np.pi
        self.vel_ang = self.Kp_a * self.error_ang
        self.vel_ang = np.clip(self.vel_ang, -self.max_vel_ang, self.max_vel_ang)
        if self.error_lin < self.tol_lin:  # dont move if close to goal
            self.vel_lin = 0
            self.vel_ang = 0
        if np.abs(self.error_ang) > self.tol_ang:  # dont move if not facing goal
            self.vel_lin = 0
        self.log_message()
        return self.vel_lin, self.vel_ang

    def log_message(self):
        print(
            "error_lin: ",
            round(self.error_lin, 2),
            "vel_lin: ",
            round(self.vel_lin, 2),
        )
        print(
            "current_ang",
            round(self.current_ang, 2),
            "goal_ang",
            round(self.goal_ang, 2),
            "error_ang: ",
            round(self.error_ang, 2),
            "vel_ang: ",
            round(self.vel_ang, 2),
        )
        print(
            "x",
            round(self.x, 2),
            "y",
            round(self.y, 2),
            "x_goal",
            round(self.x_goal, 2),
            "y_goal",
            round(self.y_goal, 2),
            "lin_vel",
            round(self.vel_lin, 2),
            "ang_vel",
            round(self.vel_ang, 2),
        )
