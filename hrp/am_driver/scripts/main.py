#!/usr/bin/env python
import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
import tf.transformations
import signal
import json
from geometry_msgs.msg import Twist, PoseStamped  # , NavSatFix
import numpy as np
from calc_velocities import CalcVelocities
from paint import get_user_input


class Drive_to:
    def __init__(self, reset_angle=True):
        self.update_freq = 10.0  # Hz but doesn't work? stuck at 10 Hz
        self.store_data = True
        self.data = {
            "x": [],
            "y": [],
            "x_goal": [],
            "y_goal": [],
            "x_mid": [],
            "y_mid": [],
            "radius": [],
        }
        self.x = None 
        self.y = None
        self.x_start = None
        self.y_start = None
        self.init_angle = None
        self.radius = None
        self.drive_in_circle = False
        self.reset_angle = reset_angle
        self.twist = Twist()

        self.pid = None  
        self.reached_goal = False
        rospy.init_node("move_forward")
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber("/pose", PoseStamped, self.pose_callback)
        self.rate = rospy.Rate(self.update_freq) 
        self.paint_order = get_user_input()

    def change_coord_sys(
        self, x_goal_prim, y_goal_prim
    ):  # automowers relative coordinates => global coordinates
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
        return x_goal, y_goal  # automowers global coordinates

    def drive(self):
        signal.signal(
            signal.SIGINT, self.ctrlc_shutdown
        )  # shuts down when ctrl+c is pressed
        while not rospy.is_shutdown() and not self.reached_goal:
            self.pub.publish(self.twist)
            self.rate.sleep()
        self.stop()

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        if self.store_data:  
            with open("data.json", "w") as json_file:
                json.dump(self.data, json_file)

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
            self.pid = CalcVelocities(self.update_freq)
            self.change_goal()  # sets initial goal/

        self.x = pose.pose.position.x
        self.y = pose.pose.position.y
        lin_vel, ang_vel = self.pid.calc_vel(current_ang, self.x, self.y)
        self.twist.linear.x = lin_vel
        self.twist.angular.z = ang_vel
        if self.store_data:
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
        # if close to goal, cahnge goal
        if lin_vel == 0.0 and ang_vel == 0.0:
            self.change_goal()

    def change_goal(self):
        if len(self.paint_order) > 0:
            if "start" in self.paint_order[0]:
                x_goal_prim, y_goal_prim = self.paint_order[0]["start"]
                self.paint_order[0].pop("start")
            elif "end" in self.paint_order[0]:
                print("end")
                self.drive_in_circle = False
                if self.paint_order[0]["type"] == "circle":  # start to go in circle
                    print("start to go in circle")
                    self.radius = self.paint_order[0]["radius"]
                    x_mid_prim, y_mid_prim = self.paint_order[0]["center"]
                    self.x_mid, self.y_mid = self.change_coord_sys(
                        x_mid_prim, y_mid_prim
                    )
                    self.drive_in_circle = True
                    self.pid.set_circle_params(self.radius, self.x_mid, self.y_mid)
                x_goal_prim, y_goal_prim = self.paint_order[0]["end"]
                self.paint_order[0].pop("end")  # unnecessary
                self.paint_order.pop(0)  # removes the line from the list
            else:
                self.reached_goal = True
                raise ValueError("Invalid line")
            x_goal, y_goal = self.change_coord_sys(x_goal_prim, y_goal_prim)
            self.data["x_goal"].append(x_goal)
            self.data["y_goal"].append(y_goal)
            if self.drive_in_circle: 
                self.data["radius"].append(self.radius)
                self.data["x_mid"].append(self.x_mid)
                self.data["y_mid"].append(self.y_mid)
            print("changed goal to", x_goal, y_goal)
            print(x_goal, y_goal, "x_goal", "y_goal")
            self.pid.set_goal_coords(x_goal, y_goal)
        else:
            self.reached_goal = True

    def ctrlc_shutdown(self, sig, frame):
        self.stop()
        rospy.signal_shutdown("User interrupted by ctrl+c")


if __name__ == "__main__":
    drive_to = Drive_to()
    drive_to.drive()
