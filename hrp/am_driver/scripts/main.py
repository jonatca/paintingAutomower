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

go_to_x_pos = 1
go_to_y_pos = 0
update_freq = 10
duration_s = 10
reached_goal = False
twist = Twist()


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
    global reached_goal, duration
    if not reached_goal:
        x = pose.pose.position.x  # get x position
        y = pose.pose.position.y  # get y position
        z_dir = pose.pose.orientation.z  # get z direction
        w_dir = pose.pose.orientation.w  # get w direction
        x_vel, z_vel = calc_vel(
            z_dir, w_dir, x, y, go_to_x_pos, go_to_y_pos, update_freq
        )
        twist.linear.x = x_vel
        twist.angular.z = z_vel
        if x_vel == 0 and z_vel == 0:
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
