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

go_to_x_pos = 6
go_to_y_pos = 0
update_freq = 10
duration_s = 40
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
    global reached_goal, duration, first_pos, x_start, y_start, z_start, w_start
    if not reached_goal:
        x = pose.pose.position.x
        y = pose.pose.position.y
        z_dir = pose.pose.orientation.z  # a angle
        w_dir = pose.pose.orientation.w  # another angle, strange coordinate system
        if first_pos:
            x_start = x
            y_start = y
            z_start = z_dir
            w_start = w_dir
            first_pos = False
        x = x - x_start
        y = y - y_start
        z_dir = z_dir - z_start
        w_dir = w_dir - w_start
        print("x: ", x, "y: ", y)
        lin_vel, ang_vel = calc_vel(
            z_dir, w_dir, x, y, go_to_x_pos, go_to_y_pos, update_freq
        )
        twist.linear.x = lin_vel
        twist.angular.z = ang_vel
        if lin_vel == 0 and ang_vel == 0:
            twist.linear.x = 0
            twist.angular.z = 0
            rospy.is_shutdown()
            rospy.loginfo("Automower has reached position x=%s, y=%s", x, y)
            duration = elapsed_time
            reached_goal = True
    else:
        print("Goal reached")


if __name__ == "__main__":
    main()
