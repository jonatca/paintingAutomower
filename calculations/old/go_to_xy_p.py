import math

tolerance_angle = 10 * math.pi / 180
y_goal = 0
x_goal = 0


def calc_k_vel(current_angle, x, y):
    # Calculate error between desired and current position and angle
    closest_point = 
    goal_angle = math.atan2(
        y_goal - closest_point[1], x_goal - closest_point[0]
    )
    error_angle = current_angle - goal_angle
    if error_angle > math.pi:
        error_angle -= 2 * math.pi
    elif error_angle < -math.pi:
        error_angle += 2 * math.pi

    # Calculate output of P controller
    pid_output_angle = kp_angle * error_angle

    # Limit output to maximum angular velocity
    if pid_output_angle > max_ang_vel:
        pid_output_angle = max_ang_vel
    elif pid_output_angle < -max_ang_vel:
        pid_output_angle = -max_ang_vel

    # Set linear velocity to zero and angular velocity to the P controller output
    lin_vel = 0
    if tolerance_angle < abs(error_angle):
        lin_vel = 0.2
    ang_vel = pid_output_angle

    return lin_vel, ang_vel * -1
