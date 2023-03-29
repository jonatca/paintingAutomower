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
            "lat": [],
            "lon": [],
            "lat_start": [],
            "lon_start": [],
            "angle_north": [],
            "angle_north_init": [],
            "covariance": [],
            "angle": [],
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
        self.covariance = None

        self.calc_velocities = None  
        self.reached_goal = False
        rospy.init_node("move_forward")
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        sub = rospy.Subscriber("/pose", PoseStamped, self.pose_callback)
        self.gps_sub = rospy.Subscriber("/GPSfix", NavSatFix, self.gps_callback)
        self.rate = rospy.Rate(self.update_freq) 
        self.order = get_paint_order()
    
    def gps_callback(self, fix):
        if self.lat_start is None and self.lon_start is None:
            self.lat_start = fix.latitude
            self.lon_start = fix.longitude
            self.data["lat_start"].append(self.lat_start)
            self.data["lon_start"].append(self.lon_start)
            self.data["angle_north_init"].append(0)
        x_gps, y_gps = self.convert_to_xy(fix.latitude, fix.longitude, self.lat_start, self.lon_start)
        self.data["x_gps"].append(x_gps)
        self.data["y_gps"].append(y_gps)
        self.data["lat"].append(fix.latitude)
        self.data["lon"].append(fix.longitude)
        self.data["angle_north"].append(0)
        self.data["covariance"].append(fix.position_covariance)
        print(fix.latitude, fix.longitude, "gps")
        print(x_gps, y_gps, "gps, converted to xy")

    def convert_to_xy(self, lat, lon, lat_start, lon_start):
        x = (lat - lat_start) * 111139
        y = (lon - lon_start) * 111139
        return x, y 

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
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        timestamp = int(timestamp.replace("-", ""))
        #make filename variable with python 2.7
        filename = "../data/{}.json".format(timestamp) #check if this works
        # filename = f"../data/{timestamp}.json"
        if self.store_data:  
            with open(filename, "w") as json_file:
                json.dump(self.data, json_file)
            plot_data(filename)
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
            self.calc_velocities = CalcVelocities(self.update_freq)
            change_goal(self)  # sets initial goal/

        self.x = pose.pose.position.x
        self.y = pose.pose.position.y
        lin_vel, ang_vel = self.calc_velocities.calc_vel(current_ang, self.x, self.y)
        self.twist.linear.x = lin_vel
        self.twist.angular.z = ang_vel
        if self.store_data:
            self.data["x"].append(self.x)
            self.data["y"].append(self.y)
            self.data["angle"].append(current_ang)
        # if close to goal, cahnge goal
        if lin_vel == 0.0 and ang_vel == 0.0:
            change_goal(self)

    def ctrlc_shutdown(self, sig, frame):
        self.stop()
        rospy.signal_shutdown("User interrupted by ctrl+c")


if __name__ == "__main__":
    drive_to = Drive_to()
    drive_to.drive()
