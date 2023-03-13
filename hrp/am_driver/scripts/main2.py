#!/usr/bin/env python
import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
import tf.transformations
import signal
from geometry_msgs.msg import Twist, PoseStamped
import numpy as np
import go_to_xy_P


class Drive_to:
    def __init__(self, x_goal_prim, y_goal_prim, reset_angle=True):
        self.update_freq = 10.0  # Hz but doesn't work? stuck at 10 Hz
        self.x_goal_prim = x_goal_prim
        self.y_goal_prim = y_goal_prim
        self.x = None
        self.y = None
        self.x_start = None
        self.y_start = None
        self.init_angle = None
        self.reset_angle = reset_angle
        self.twist = Twist()

        self.pid = None  # go_to_xy_P.P(self.x_goal, self.y_goal, self.update_freq)
        self.reached_goal = False
        rospy.init_node("move_forward")
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber("/pose", PoseStamped, self.pose_callback)
        self.rate = rospy.Rate(self.update_freq)

    def goal_coords(self):  # prim coordinates => automowers relative coordinates
        x_goal = (
            self.x_start
            + self.x_goal_prim * np.cos(self.init_angle)
            - self.y_goal_prim * np.sin(self.init_angle)
        )
        y_goal = (
            self.y_start
            + self.x_goal_prim * np.sin(self.init_angle)
            + self.y_goal_prim * np.cos(self.init_angle)
        )
        return x_goal, y_goal  # given in automowers global coordinates

    def drive(self):
        signal.signal(
            signal.SIGINT, self.ctrlc_shutdown
        )  # shuts down when ctrl+c is pressed
        while not rospy.is_shutdown() and not self.reached_goal:
            self.pub.publish(self.twist)
            self.rate.sleep()
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        rospy.loginfo(
            "Automower has moved to position x=%s, y=%s",
            round(self.x, 2),
            round(self.y, 2),
        )

    def pose_callback(self, pose):
        z_dir = pose.pose.orientation.z
        w_dir = pose.pose.orientation.w
        current_ang = tf.transformations.euler_from_quaternion([0, 0, z_dir, w_dir])[2]
        if (
            self.reset_angle
            and self.init_angle is None
            and self.x_start is None
            and self.y_start is None
        ):
            self.init_angle = current_ang
            self.x_start = pose.pose.position.x
            self.y_start = pose.pose.position.y
            x_goal, y_goal = self.goal_coords()
            self.pid = go_to_xy_P.P(x_goal, y_goal, self.update_freq)
        self.x = pose.pose.position.x
        self.y = pose.pose.position.y
        lin_vel, ang_vel = self.pid.calc_vel(current_ang, self.x, self.y)
        self.twist.linear.x = lin_vel
        self.twist.angular.z = ang_vel
        if lin_vel == 0.0 and ang_vel == 0.0:
            self.reached_goal = True

    def ctrlc_shutdown(self, sig, frame):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        rospy.signal_shutdown("User interrupted by ctrl+c")


if __name__ == "__main__":
    x_goal = 1  # positive x = forward
    y_goal = 0  # positive y = left
    drive_to = Drive_to(x_goal, y_goal)
    drive_to.drive()
