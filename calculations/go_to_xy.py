import numpy as np
import math

max_lin_vel = 0.3
max_ang_vel = 0.8
start_slow_lin = 15 * np.pi / 180  # starts to slow down when error less than this
start_slow_ang = 0.5
kp_linear = 1  # these are tested to be good, not sure if they are the best
kp_angular = 0.5
tolerance_position = 0.1  # meters
tolerance_angle = 5 * np.pi / 180


def calc_vel(z_dir, w_dir, x, y, x_goal, y_goal, update_freq):
    error_angle = _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal)
    error_distance = math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
    print("error_distance=", error_distance, "error_angle=", error_angle)
    if error_distance > tolerance_position:
        ang_vel = _calc_ang_vel(error_angle, error_distance)  # always rotate
        if abs(error_angle) > tolerance_angle:
            lin_vel = 0
        else:  # if angle is small enough, move forward
            lin_vel = max_lin_vel * np.sign(error_distance)
            if error_distance < start_slow_lin:
                lin_vel = kp_linear * max_lin_vel * error_distance / start_slow_lin
            lin_vel = min(np.abs(lin_vel), np.abs(max_lin_vel))  # just in case
    else:
        lin_vel = 0
        ang_vel = 0

    print("lin_vel=", lin_vel, "ang_vel=", ang_vel)
    return lin_vel, ang_vel


def _calc_ang_vel(error_angle, error_distance):
    ang_vel = np.sign(error_angle) * max_ang_vel
    if error_angle < start_slow_ang:  # slow down when angle is small
        ang_vel = kp_angular * max_ang_vel * error_angle / start_slow_ang
    if np.abs(ang_vel) > np.abs(max_ang_vel):
        ang_vel = np.sign(ang_vel) * max_ang_vel  # limit angluar velocity
    return ang_vel


def _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal):
    # Convert quaternion orientation into yaw angle using formula from https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
    t3 = +2.0 * (w_dir * z_dir)
    t4 = +1.0 - 2.0 * (z_dir * z_dir)
    current_angle = math.atan2(t3, t4)
    # Calculate desired angle that points towards goal position using trigonometry
    desired_angle = math.atan2(y_goal - y, x_goal - x)
    # Calculate error between desired and current angles
    # error_angle = math.fmod(desired_angle - current_angle, 2 * math.pi)
    error_angle = desired_angle - current_angle
    if error_angle > math.pi:
        error_angle -= 2 * math.pi
    elif error_angle < -math.pi:
        error_angle += 2 * math.pi
    return error_angle
