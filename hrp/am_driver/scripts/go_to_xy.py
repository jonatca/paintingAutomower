import numpy as np
import math

max_lin_vel = 0.3
max_ang_vel = 0.8
start_slow_lin = 0.3  # starts to slow down when error less than this
start_slow_ang = 0.5
kp_linear = max_lin_vel / (2 * start_slow_lin)  # Proportional gain
kp_angular = max_ang_vel / (1.5 * start_slow_ang)
tolerance_position = 0.005  # meters
tolerance_angle = 15 * np.pi / 180


def calc_vel(z_dir, w_dir, x, y, x_goal, y_goal):
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
    error_distance = math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
    print("error_distance=", error_distance, "error_angle=", error_angle)
    if error_distance > tolerance_position:
        if abs(error_angle) > tolerance_angle:
            z_vel = kp_angular * error_angle
            if start_slow_lin < error_distance:  # when close rotate even slower
                z_vel *= kp_linear * error_distance
            # Limit angular velocity to maximum value
            if abs(z_vel) > max_ang_vel:
                z_vel = np.sign(z_vel) * max_ang_vel
            x_vel = 0
        else:
            # Move forward until close enough to goal position
            x_vel = kp_linear * error_distance
            x_vel = min(x_vel, max_lin_vel)
            z_vel = 0
    else:
        # Stop when close enough to goal position
        x_vel = 0
        z_vel = 0
    return x_vel, z_vel
