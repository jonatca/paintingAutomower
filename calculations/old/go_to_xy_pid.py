import numpy as np
import math

max_lin_vel = 0.3
max_ang_vel = 0.8
start_slow_lin = 15 * np.pi / 180  # starts to slow down when error less than this
start_slow_ang = 0.5
kp_linear = 0.5
ki_linear = 0.1
kd_linear = 0.1
kp_angular = 0.5
ki_angular = 0.1
kd_angular = 0.1
tolerance_position = 0.01  # meters
tolerance_angle = 5 * np.pi / 180

prev_error_lin = 0
integral_lin = 0
prev_error_ang = 0
integral_ang = 0


def calc_vel(z_dir, w_dir, x, y, x_goal, y_goal, update_freq):
    global prev_error_lin, integral_lin, prev_error_ang, integral_ang

    error_angle = _calc_error_angle(z_dir, w_dir, x, y, x_goal, y_goal)
    error_distance = math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
    print("error_distance=", error_distance, "error_angle=", error_angle)

    if error_distance > tolerance_position:
        # Calculate angular velocity using a PID controller
        ang_error = error_angle
        derivative_ang = (ang_error - prev_error_ang) * update_freq
        integral_ang += ang_error * update_freq
        ang_vel = (
            kp_angular * ang_error
            + ki_angular * integral_ang
            + kd_angular * derivative_ang
        )
        ang_vel = np.clip(ang_vel, -max_ang_vel, max_ang_vel)
        prev_error_ang = ang_error

        if abs(error_angle) > tolerance_angle:
            lin_vel = 0
        else:
            # Calculate linear velocity using a PID controller
            lin_error = error_distance
            derivative_lin = (lin_error - prev_error_lin) * update_freq
            integral_lin += lin_error * update_freq
            lin_vel = (
                kp_linear * lin_error
                + ki_linear * integral_lin
                + kd_linear * derivative_lin
            )
            lin_vel = np.clip(lin_vel, -max_lin_vel, max_lin_vel)
            prev_error_lin = lin_error

            if error_distance < start_slow_lin:
                lin_vel = kp_linear * max_lin_vel * error_distance / start_slow_lin

    else:
        lin_vel = 0
        ang_vel = 0

    print("lin_vel=", lin_vel, "ang_vel=", ang_vel)
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
