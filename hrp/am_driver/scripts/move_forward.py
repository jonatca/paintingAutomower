#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

def pose_callback(pose):
    print("hej")
    x = pose.pose.position.x # get x position
    y = pose.pose.position.y # get y position
    z = pose.pose.position.z # get z position
    rospy.loginfo("Automower position: x=%s, y=%s, z=%s", x, y, z)

rospy.init_node('move_forward')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/pose', PoseStamped, pose_callback)
rate = rospy.Rate(3)

twist = Twist()
twist.linear.x = 0.1
twist.angular.z = 0.0

start_time = rospy.Time.now()
duration = rospy.Duration(10)

while not rospy.is_shutdown():
    current_time = rospy.Time.now()
    elapsed_time = current_time - start_time
    if elapsed_time < duration:
        pub.publish(twist)
    else:
        break
    rate.sleep()

twist.linear.x = 0.0
pub.publish(twist)

rospy.loginfo("Automower has moved two meters forward.")