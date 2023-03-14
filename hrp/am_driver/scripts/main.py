#!/usr/bin/env python
import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
import tf.transformations
import signal
from geometry_msgs.msg import Twist, PoseStamped
import numpy as np
import go_to_xy_P
from paint import get_user_input


class Drive_to:
    def __init__(self, reset_angle=True):
        self.update_freq = 10.0  # Hz but doesn't work? stuck at 10 Hz
        self.x = None
        self.y = None
        self.x_start = None
        self.y_start = None
        self.init_angle = None
        self.reset_angle = reset_angle
        self.twist = Twist()
        self.hasMoved = False

        self.pid = None  # go_to_xy_P.P(self.x_goal, self.y_goal, self.update_freq)
        self.reached_goal = False
        rospy.init_node("move_forward")
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber("/pose", PoseStamped, self.pose_callback)
        self.rate = rospy.Rate(self.update_freq)
        self.paint_order = get_user_input()

    def change_coord_sys(
        self, x_goal_prim, y_goal_prim
    ):  # prim coordinates => automowers relative coordinates
        x_goal = (
            self.x_start
            + x_goal_prim * np.cos(self.init_angle)
            - y_goal_prim * np.sin(self.init_angle)
        )
        y_goal = (
            self.y_start
            + x_goal_prim * np.sin(self.init_angle)
            + y_goal_prim * np.cos(self.init_angle)
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
            self.pid = go_to_xy_P.P(self.update_freq)
            self.change_goal()  # sets initial goal
        self.x = pose.pose.position.x
        self.y = pose.pose.position.y
        lin_vel, ang_vel = self.pid.calc_vel(current_ang, self.x, self.y)
        self.twist.linear.x = lin_vel
        self.twist.angular.z = ang_vel
        if lin_vel == 0.0 and ang_vel == 0.0:  # and self.hasMoved:
            self.change_goal()
        # if not (ang_vel == 0.0 and lin_vel == 0.0):
        #     self.hasMoved = True

    def change_goal(self):
        if len(self.paint_order) > 0:
            if "start" in self.paint_order[0]:
                x_goal_prim, y_goal_prim = self.paint_order[0]["start"]
                self.paint_order[0].pop("start")
            elif "end" in self.paint_order[0]:
                x_goal_prim, y_goal_prim = self.paint_order[0]["end"]
                self.paint_order[0].pop("end")  # unnecessary
                self.paint_order.pop(0)  # removes the line from the list
            else:
                print(self.current_line, "line")
                self.reached_goal = True
                raise ValueError("Invalid line")
            x_goal, y_goal = self.change_coord_sys(x_goal_prim, y_goal_prim)
            print("changed goal to", x_goal, y_goal)
            print(x_goal, y_goal, "x_goal", "y_goal", type(x_goal), type(y_goal))
            self.pid.set_goal_coords(x_goal, y_goal)
        else:
            self.reached_goal = True

    def ctrlc_shutdown(self, sig, frame):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        rospy.signal_shutdown("User interrupted by ctrl+c")


if __name__ == "__main__":
    x_goal = 0.4  # positive x = forward
    y_goal = 0  # positive y = left
    drive_to = Drive_to()
    drive_to.drive()
