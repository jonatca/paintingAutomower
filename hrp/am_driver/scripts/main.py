#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import numpy as np
from set_vel import calc_vel

go_to_x_pos = 0
go_to_y_pos = 0
num_callbacks = 0


def pose_callback(pose):
    if num_callbacks == 0:
        starting_x = pose.pose.position.x
        starting_y = pose.pose.position.y
        starting_z_dir = pose.pose.orientation.z
        starting_w_dir = pose.pose.orientation.w
        go_to_x_pos -= starting_x
        go_to_y_pos -= starting_y

    num_callbacks = 1
    x = pose.pose.position.x - starting_x  # get x position
    y = pose.pose.position.y - starting_y  # get y position
    z_dir = pose.pose.orientation.z - starting_z_dir  # get z direction
    w_dir = pose.pose.orientation.w - starting_w_dir  # get w direction
    x_vel, z_vel = calc_vel(z_dir, w_dir, x, y, go_to_x_pos, go_to_y_pos)
    twist.linear.x = x_vel
    twist.angular.z = z_vel


rospy.init_node("move_forward")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
sub = rospy.Subscriber("/pose", PoseStamped, pose_callback)
rate = rospy.Rate(10)

twist = Twist()
start_time = rospy.Time.now()
duration = rospy.Duration(15)

while not rospy.is_shutdown():
    current_time = rospy.Time.now()
    elapsed_time = current_time - start_time
    if elapsed_time < duration:
        pub.publish(twist)
    else:
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        pub.publish(twist)
        break
    rate.sleep()

twist.linear.x = 0.0
twist.angular.z = 0.0
pub.publish(twist)

rospy.loginfo("Automower has moved to position x=%s, y=%s", go_to_x_pos, go_to_y_pos)
