import numpy as np


class CalcVelocities:
    def __init__(self, update_freq):
        self.tol_lin = 0.05  # tolerance in meter
        self.tol_ang = 7 * np.pi / 180
        self.min_tol_ang = 0.1 * np.pi / 180  # to avoid calculations error
        self.max_vel_lin = 0.3
        self.max_vel_ang = 0.8
        self.Kp_l = 0.7
        self.Kp_a = 0.8
        self.x_goal = None  # global coordinates
        self.y_goal = None
        self.update_time = 1.0 / update_freq
        self.current_ang = None
        self.error_lin = None
        self.vel_lin = None
        self.x = None
        self.y = None
        self.paint_circle = False
        self.x_mid = None
        self.y_mid = None
        self.radius = None
        self.theoretical_vel_ang = 0

    def set_circle_params(self, radius, x_mid, y_mid):
        self.radius = radius
        self.x_mid = x_mid
        self.y_mid = y_mid
        self.theoretical_vel_ang = self._radius_vel_ang()
        self.paint_circle = True
        self.kp_a = 3
        self.max_vel_lin = 0.1
        self.tol_ang = 10 * np.pi / 180
        self.tol_lin = 0.1

    def _radius_vel_ang(self):
        theoretical_vel_ang = 0
        return theoretical_vel_ang

    def _goal_angle_line(self):
        goal_ang = np.arctan2(self.y_goal - self.y, self.x_goal - self.x)
        return goal_ang

    def _goal_angle_circle(self, x_mid, y_mid, x, y):
        # Calculate the vector from the center of the circle to the robot's position
        V_x = x - x_mid
        V_y = y - y_mid
        # Normalize the vector
        V_mag = np.sqrt(V_x**2 + V_y**2)
        V_x_norm = V_x / V_mag
        V_y_norm = V_y / V_mag
        # Calculate the tangent vector
        T_x = -V_y_norm
        T_y = V_x_norm
        # Calculate the angle theta between the robot's direction and the positive x-axis
        goal_angle = np.arctan2(T_y, T_x)
        return goal_angle

    def calc_vel(self, current_ang, x, y):
        self.current_ang = current_ang
        self.x = x
        self.y = y
        self.error_lin = np.sqrt(
            (self.x_goal - self.x) ** 2 + (self.y_goal - self.y) ** 2
        )
        self.goal_ang = self._goal_angle_line()
        if self.paint_circle:
            self.goal_ang = self._goal_angle_circle(
                self.x_mid, self.y_mid, self.x, self.y
            )
        self.vel_lin = self.Kp_l * self.error_lin  # slows down when close to goal
        self.vel_lin = np.clip(
            self.vel_lin, -self.max_vel_lin, self.max_vel_lin
        )  # limits max velocity
        self.error_ang = self.goal_ang - self.current_ang
        self.error_ang = (self.error_ang + np.pi) % (2 * np.pi) - np.pi
        if self.error_ang < self.min_tol_ang:  # to avoid calculatins error
            self.error_ang = 0
        self.vel_ang = self.Kp_a * self.error_ang  # more error => more angular velocity
        self.vel_ang = np.clip(self.vel_ang, -self.max_vel_ang, self.max_vel_ang)
        if self.error_lin < self.tol_lin:  # dont move if close to goal
            self.vel_lin = 0
            self.vel_ang = 0
        if np.abs(self.error_ang) > self.tol_ang:  # dont move if not facing goal
            self.vel_lin = 0
        self.log_message()
        return self.vel_lin, self.vel_ang

    def has_reached_goal(self):
        return self.error_lin < self.tol_lin

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

    def set_goal_coords(self, x_goal, y_goal):
        self.x_goal = x_goal
        self.y_goal = y_goal
