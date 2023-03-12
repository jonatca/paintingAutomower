#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import numpy as np
from go_to_xy import (
    calc_vel,
)  # error? is go_to_xy.pyc in calculations folder? try chmod 777 go_to_xy.py and catkin_make
import go_to_xy_PID3
import go_to_xy_PID4

# from go_to_xy_p import calc_k_vel
import math

go_to_x_pos = 0.9
go_to_y_pos = 0
update_freq = 10
duration_s = 10
reached_goal = False
first_pos = True
twist = Twist()
x_start = 0
y_start = 0
z_start = 0
w_start = 0


def main():
    global elapsed_time
    rospy.init_node("move_forward")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/pose", PoseStamped, pose_callback)
    rate = rospy.Rate(update_freq)

    start_time = rospy.Time.now()
    duration = rospy.Duration(duration_s)

    while not rospy.is_shutdown() and not reached_goal:
        current_time = rospy.Time.now()
        elapsed_time = current_time - start_time
        if elapsed_time < duration:
            pub.publish(twist)
        else:
            twist.linear.x = 0
            twist.angular.z = 0
            pub.publish(twist)
            break
        rate.sleep()

    twist.linear.x = 0
    twist.angular.z = 0
    pub.publish(twist)
    rospy.is_shutdown()

    rospy.loginfo(
        "Automower has moved to position x=%s, y=%s", go_to_x_pos, go_to_y_pos
    )


def pose_callback(pose):
    global reached_goal, duration, first_pos, x_start, y_start, z_start, w_start, pid
    if not reached_goal:
        x = pose.pose.position.x
        y = pose.pose.position.y
        z_dir = pose.pose.orientation.z
        w_dir = pose.pose.orientation.w
        t3 = +2.0 * (w_dir * z_dir)
        t4 = +1.0 - 2.0 * (z_dir * z_dir)
        current_angle = math.atan2(t3, t4)
        if first_pos:
            x_start = x
            y_start = y
            z_start = z_dir
            w_start = w_dir
            pid = go_to_xy_PID4.PID(
                x_start,
                y_start,
                go_to_x_pos + x_start,
                go_to_y_pos + y_start,
                update_freq,
            )
            start_angle = current_angle  # angle is wrong
            first_pos = False

        print("x: ", x, "y: ", y)
        lin_vel, ang_vel = pid.calc_vel(current_angle, x, y)
        # lin_vel, ang_vel = calc_k_vel(current_angle, x, y)
        twist.linear.x = lin_vel
        twist.angular.z = ang_vel

        if lin_vel == 0 and ang_vel == 0:
            twist.linear.x = 0
            twist.angular.z = 0
            rospy.signal_shutdown("Automower has reached position goal position")
            duration = elapsed_time
            reached_goal = True
    else:
        print("Goal reached")


if __name__ == "__main__":
    main()
