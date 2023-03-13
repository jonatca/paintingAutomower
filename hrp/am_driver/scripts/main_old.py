#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tf

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

go_to_x_pos = 1
go_to_y_pos = 2.33
update_freq = 10
duration_s = 1
reached_goal = False
first_pos = True
twist = Twist()
x_start = 0
y_start = 0
z_start = 0
w_start = 0
start_angle = 0
pid = None
pid = go_to_xy_PID4.PID(
    x_start,
    y_start,
    go_to_x_pos + x_start,
    go_to_y_pos + y_start,
    update_freq,
)


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


def calc_angle(z_dir, w_dir):
    t3 = +2.0 * (w_dir * z_dir)
    t4 = +1.0 - 2.0 * (z_dir * z_dir)
    current_angle = np.arctan2(t3, t4)
    return current_angle


def pose_callback(pose):
    global reached_goal, duration, first_pos, x_start, y_start, z_start, w_start, pid, start_angle
    if not reached_goal:
        x_map = pose.pose.position.x
        y_map = pose.pose.position.y
        z_map = pose.pose.orientation.z
        w_map = pose.pose.orientation.w

        if first_pos:
            listener = tf.TransformListener()
            listener.waitForTransform(
                "base_link", "map", rospy.Time(), rospy.Duration(4.0)
            )
            point_in_base_link, rot_in_base_link = listener.lookupTransform(
                "base_link", "map", rospy.Time(0)
            )
            x_start = point_in_base_link[0]
            y_start = point_in_base_link[1]
            first_pos = False

        listener = tf.TransformListener()
        listener.waitForTransform("base_link", "map", rospy.Time(), rospy.Duration(4.0))
        point_in_base_link, rot_in_base_link = listener.lookupTransform(
            "base_link", "map", rospy.Time(0)
        )
        x_base = x_map - point_in_base_link[0]
        y_base = y_map - point_in_base_link[1]
        theta_base = tf.transformations.euler_from_quaternion(rot_in_base_link)[2]

        current_angle = calc_angle(z_map, w_map)  # - start_angle
        current_angle = (current_angle + np.pi) % (2 * np.pi) - np.pi
        print("x: ", round(x_base, 2), "y: ", round(y_base, 2))
        lin_vel, ang_vel = pid.calc_vel(current_angle, x_base, y_base)
        # lin_vel, ang_vel = calc_k_vel(current_angle, x_base, y_base)
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
