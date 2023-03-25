#!/usr/bin/env python
import sys

sys.path.append("/home/kandidatarbete/450/src/calculations")
import rospy
import tf.transformations
import signal
import json
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import NavSatFix
# from gps_common.msg import NavSatFix
import numpy as np
from calc_velocities import CalcVelocities
from paint import get_paint_order
from plot_data import plot_data
from change_goal import change_goal
from coord_sys_trans import convert_to_xy
import datetime
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
            "x_gps": [],
            "y_gps": [],
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
        self.lat_start = None
        self.lon_start = None

        self.calc_velocities = CalcVelocities(self.update_freq)
        self.reached_goal = False
        rospy.init_node("move_forward")
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber("/pose", PoseStamped, self.pose_callback)
        self.gps_sub = rospy.Subscriber("/GPSfix", NavSatFix, self.gps_callback)
        self.rate = rospy.Rate(self.update_freq) 
        self.paint_order = get_paint_order()
    
    def drive(self):
        signal.signal(
            signal.SIGINT, self.ctrlc_shutdown
        )  # shuts down when ctrl+c is pressed
        while not rospy.is_shutdown() and not self.reached_goal:
            self.pub.publish(self.twist)
            self.rate.sleep()
        self.stop()

    def pose_callback(self, pose):
        z_dir = pose.pose.orientation.z
        w_dir = pose.pose.orientation.w
        current_ang = tf.transformations.euler_from_quaternion([0, 0, z_dir, w_dir])[2]
        if (self.reset_angle and self.x_start is None):
            self.init_angle = current_ang
            self.x_start = pose.pose.position.x
            self.y_start = pose.pose.position.y
            change_goal(self, simulation = False)  # sets initial goal
        lin_vel, ang_vel = self.calc_velocities.calc_vel(current_ang, self.x, self.y)
        if lin_vel == 0.0 and ang_vel == 0.0: #TODO check if this works
            change_goal(self, simulation = False)
            lin_vel, ang_vel = self.calc_velocities.calc_vel(current_ang, self.x, self.y)
        self.twist.linear.x = lin_vel
        self.twist.angular.z = ang_vel
        if self.store_data:
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
        # if close to goal, cahnge goal

    def gps_callback(self, fix): #TODO get gps unsertainty
        if self.lat_start is None and self.lon_start is None:
            self.lat_start = fix.latitude
            self.lon_start = fix.longitude
        x_gps, y_gps = convert_to_xy(fix.latitude, fix.longitude, self.lat_start, self.lon_start)
        self.data["x_gps"].append(x_gps)
        self.data["y_gps"].append(y_gps)
        print(fix.latitude, fix.longitude, "gps")
        print(x_gps, y_gps, "gps, converted to xy")

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        timestamp = int(timestamp.replace("-", ""))
        filename = "../data/{}.json".format(timestamp) #TODO check if this works
        # filename = f"../data/{timestamp}.json"
        if self.store_data:  #TODO check if this works
            with open(filename, "w") as json_file:
                json.dump(self.data, json_file)
            plot_data(filename)
        rospy.loginfo(
            "Automower has moved to position x=%s, y=%s",
            round(self.x, 2),
            round(self.y, 2),
        )

    def ctrlc_shutdown(self, sig, frame):
        self.stop()
        rospy.signal_shutdown("User interrupted by ctrl+c")

if __name__ == "__main__":
    drive_to = Drive_to()
    drive_to.drive()
