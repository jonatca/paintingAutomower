import numpy as np
import math

# Constants
max_lin_vel = 0.3
max_ang_vel = 0.8
start_slow_lin = 15 * np.pi / 180  # starts to slow down when error less than this
start_slow_ang = 0.5
tolerance_position = 0.01  # meters
tolerance_angle = 5 * np.pi / 180
kp_linear = 1  # these are tested to be good, not sure if they are the best
kp_angular = 0.5
ki_linear = 0.1
ki_angular = 0.05
kd_linear = 0.05
kd_angular = 0.025


class PIDController:
    def __init__(self, update_freq):
        self.update_freq = update_freq
        self.last_time = None
        self.integral_linear = 0
        self.integral_angular = 0
        self.last_error_linear = 0
        self.last_error_angular = 0

    def update(self, z_dir, w_dir, x, y, x_goal, y_goal):
        # Calculate error
        error_linear = math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
        error_angular = _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal)

        delta_t = 1 / self.update_freq
        # Calculate derivatives
        derivative_linear = (error_linear - self.last_error_linear) / delta_t
        derivative_angular = (error_angular - self.last_error_angular) / delta_t

        # Update integral
        self.integral_linear += error_linear * delta_t
        self.integral_angular += error_angular * delta_t

        # Calculate PID terms
        p_term_linear = kp_linear * error_linear
        i_term_linear = ki_linear * self.integral_linear
        d_term_linear = kd_linear * derivative_linear
        p_term_angular = kp_angular * error_angular
        i_term_angular = ki_angular * self.integral_angular
        d_term_angular = kd_angular * derivative_angular

        # Calculate velocity commands
        lin_vel = p_term_linear + i_term_linear + d_term_linear
        ang_vel = p_term_angular + i_term_angular + d_term_angular

        # Apply speed limits and start slowing down when close to goal
        if error_linear < start_slow_lin:
            lin_vel *= error_linear / start_slow_lin
        lin_vel = np.clip(lin_vel, -max_lin_vel, max_lin_vel)
        if error_angular < start_slow_ang:
            ang_vel *= error_angular / start_slow_ang
        ang_vel = np.clip(ang_vel, -max_ang_vel, max_ang_vel)

        # Save last error for next iteration
        self.last_error_linear = error_linear
        self.last_error_angular = error_angular

        return lin_vel, ang_vel


def _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal):
    # Convert quaternion orientation into yaw angle using formula from https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
    t3 = +2.0 * (w_dir * z_dir)
    t4 = +1.0 - 2.0 * (z_dir * z_dir)
    current_angle = math.atan2(t3, t4)
    # Calculate desired angle that points towards goal position using trigonometry
    desired_angle = math.atan2(y_goal - y, x_goal - x)
    # Calculate error between desired and current angles
    error_angle = math.fmod(desired_angle - current_angle, 2 * math.pi)
    if error_angle > math.pi:
        error_angle -= 2 * math.pi
    elif error_angle < -math.pi:
        error_angle += 2 * math.pi
    return error_angle
