import numpy as np
import math

max_lin_vel = 0.3
max_ang_vel = 0.8
start_slow_lin = 0.3  # starts to slow down when error less than this
start_slow_ang = 0.5
kp_linear = 0.1  # these are tested to be good, not sure if they are the best
kp_angular = 0.8
tolerance_position = 0.01  # meters
tolerance_angle = 10 * np.pi / 180


def calc_vel(z_dir, w_dir, x, y, x_goal, y_goal):
    error_angle = _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal)
    error_distance = math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
    print("error_distance=", error_distance, "error_angle=", error_angle)
    if error_distance > tolerance_position:
        if abs(error_angle) > tolerance_angle:
            z_vel = _calc_z_vel(error_angle, error_distance)
            x_vel = 0
        else:
            if error_distance < start_slow_lin:
                x_vel = kp_linear * error_distance
            x_vel = min(x_vel, max_lin_vel)  # just in case
            z_vel = 0
    else:
        x_vel = 0
        z_vel = 0
    return x_vel, z_vel


def _calc_z_vel(error_angle, error_distance):
    z_vel = np.sign(z_vel) * max_ang_vel
    if error_distance < start_slow_lin:  # when close rotate
        z_vel *= kp_linear * error_distance
    if error_angle < start_slow_ang:  # slow down when angle is small
        z_vel *= kp_angular * error_angle
    z_vel = min(z_vel, max_ang_vel)  # limit max angular velocity, just in case
    return z_vel


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
