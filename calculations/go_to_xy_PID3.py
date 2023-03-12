import numpy as np
import math


class PID:
    def __init__(self, x_start, y_start, x_goal, y_goal, update_freq):
        self.kp = 0.5
        self.ki = 0
        self.kd = 0
        self.kp_angle = 1
        self.ki_angle = 0
        self.kd_angle = 0
        self.x_start = x_start
        self.y_start = y_start
        self.x_goal = x_goal
        self.y_goal = y_goal
        self.tolerance_position = 0.1  # meters
        self.tolerance_angle = 10 * np.pi / 180
        self.min_lin_vel = 0.2
        self.max_lin_vel = 0.3
        self.max_ang_vel = 0.8
        self.start_slow_lin = 0.2 * self.max_lin_vel
        self.last_error_distance = 0
        self.sum_error_distance = 0
        self.last_error_angle = 0
        self.sum_error_angle = 0
        self.time_diff = 1.0 / update_freq

    def calc_vel(self, current_angle, x, y):
        # Calculate error between desired and current position and angle
        error_goal = np.linalg.norm([x - self.x_goal, y - self.y_goal])
        print("error_goal=", error_goal)
        if abs(error_goal) < self.tolerance_position:
            return 0, 0
        closest_point = self._calc_closest_point(x, y)
        error_distance = np.linalg.norm([x - closest_point[0], y - closest_point[1]])
        goal_angle = math.atan2(
            self.y_goal - closest_point[1], self.x_goal - closest_point[0]
        )
        error_angle = current_angle - goal_angle
        if error_angle > math.pi:
            error_angle -= 2 * math.pi
        elif error_angle < -math.pi:
            error_angle += 2 * math.pi
        print(
            "current_angle=",
            current_angle,
            "goal_angle=",
            goal_angle,
            "error_angle=",
            error_angle,
        )
        # Calculate derivative of error
        error_distance_diff = (
            error_distance - self.last_error_distance
        ) / self.time_diff
        self.last_error_distance = error_distance

        # Calculate integral of error
        self.sum_error_distance += error_distance * self.time_diff
        # sum_error_distance_abs = abs(self.sum_error_distance)
        # Calculate output of PID controller
        pid_output = (
            self.kp * error_distance
            + self.ki * self.sum_error_distance
            + self.kd * error_distance_diff
        )

        # Limit output to maximum velocity
        pid_output = np.clip(pid_output, -self.max_lin_vel, self.max_lin_vel)

        # Calculate derivative of angle error
        print(self.time_diff)
        error_angle_diff = (error_angle - self.last_error_angle) / self.time_diff
        self.last_error_angle = error_angle

        # Calculate integral of angle error
        self.sum_error_angle += error_angle * self.time_diff
        sum_error_angle_abs = abs(self.sum_error_angle)

        # Calculate output of angle PID controller
        pid_output_angle = (
            self.kp_angle * error_angle
            + self.ki_angle * self.sum_error_angle
            + self.kd_angle * error_angle_diff
        )

        # Limit output to maximum angular velocity
        if pid_output_angle > self.max_ang_vel:
            pid_output_angle = self.max_ang_vel
        elif pid_output_angle < -self.max_ang_vel:
            pid_output_angle = -self.max_ang_vel

        # Calculate linear and angular velocities based on PID output and error angle
        ang_vel = pid_output_angle
        if abs(error_angle) > self.tolerance_angle:
            lin_vel = 0
        else:
            lin_vel = pid_output
            lin_vel = min(abs(lin_vel), self.max_lin_vel)
            lin_vel = max(lin_vel, self.min_lin_vel)
        return lin_vel, ang_vel * -1

    def _calc_error_angle(self, z_dir, w_dir, x, y, closest_point):
        # Convert quaternion orientation into yaw angle using formula from https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
        t3 = +2.0 * (w_dir * z_dir)
        t4 = +1.0 - 2.0 * (z_dir * z_dir)
        current_angle = math.atan2(t3, t4)
        print("current_angle=", current_angle)
        # Calculate desired angle that points towards goal position using trigonometry
        goal_angle = math.atan2(self.y_goal - self.y_start, self.x_goal - self.x_start)
        print("goal_angle=", goal_angle)
        # Calculate error between desired and current angles
        error_angle = goal_angle - current_angle
        if error_angle > math.pi:
            error_angle -= 2 * math.pi
        elif error_angle < -math.pi:
            error_angle += 2 * math.pi
        return error_angle

    def _calc_closest_point(self, x, y):
        # Calculate the vector from the start position to the current position
        dx = x - self.x_start
        dy = y - self.y_start

        # Calculate the unit vector in the direction of the goal
        goal_vector = np.array([self.x_goal - self.x_start, self.y_goal - self.y_start])
        goal_unit_vector = goal_vector / np.linalg.norm(goal_vector)

        # Calculate the projection of the current position onto the goal vector
        projection = np.dot([dx, dy], goal_unit_vector)

        # Calculate the closest point on the line between start and goal
        closest_point = (
            np.array([self.x_start, self.y_start]) + projection * goal_unit_vector
        )

        return closest_point
