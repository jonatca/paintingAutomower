#!/usr/bin/env python

import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
import tf2_ros
import tf.transformations

from geometry_msgs.msg import Twist, PoseStamped
import go_to_xy_PID4

# Target position in the base_link frame
target_x = 2
target_y = 2.33

# PID controller parameters
kp_l = 0.5
kp_a = 0.5
update_freq = 10.0

# Initialize global variables
twist = Twist()
pid = go_to_xy_PID4.PID(0, 0, target_x, target_y, update_freq)
reached_goal = False


def main():
    global reached_goal
    rospy.init_node("move_forward")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/pose", PoseStamped, pose_callback)
    rate = rospy.Rate(update_freq)

    while not rospy.is_shutdown() and not reached_goal:
        pub.publish(twist)
        rate.sleep()

    twist.linear.x = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)

    rospy.loginfo("Automower has moved to position x=%s, y=%s", target_x, target_y)


def pose_callback(pose):
    global reached_goal, twist, pid
    x = pose.pose.position.x
    y = pose.pose.position.y
    z_dir = pose.pose.orientation.z
    w_dir = pose.pose.orientation.w
    current_angle = tf.transformations.euler_from_quaternion([0, 0, z_dir, w_dir])[2]
    lin_vel, ang_vel = pid.calc_vel(current_angle, x, y)
    print(
        "x",
        round(x, 2),
        "y",
        round(y, 2),
        "x_goal",
        round(target_x, 2),
        "y_goal",
        round(target_y, 2),
        "lin_vel",
        round(lin_vel, 2),
        "ang_vel",
        round(ang_vel, 2),
    )

    twist.linear.x = lin_vel
    twist.angular.z = ang_vel

    if lin_vel == 0.0 and ang_vel == 0.0:
        reached_goal = True


if __name__ == "__main__":
    main()
