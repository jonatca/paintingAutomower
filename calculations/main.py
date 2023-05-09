#!/usr/bin/env python
import rclpy
import threading
import sys
import tty
import termios
import matplotlib.pyplot as plt
import signal
import json

from rclpy.node import Node
from hqv_public_interface.msg import RemoteDriverDriveCommand
from hqv_public_interface.msg import MowerImu
from hqv_public_interface.msg import MowerGnssRtkRelativePositionENU

import numpy as np
from calc_velocities_550 import CalcVelocities
from paint import get_paint_order
#from plot_data2 import plot_data
from change_goal_550 import change_goal
from coord_sys_trans import *
import datetime



class DriveTo(Node):

    def __init__(self):
        super().__init__('drive_to')
        self.drive_publisher = self.create_publisher(RemoteDriverDriveCommand, '/hqv_mower/remote_driver/drive', 100)
        self.rtk_subscriber = self.create_subscription(MowerGnssRtkRelativePositionENU, '/hqv_mower/gnss_rtk/rel_enu', self.rtk_callback, 10)
        self.imu_subscriber = self.create_subscription(MowerImu, '/hqv_mower/imu0/orientation', self.imu_callback, 10)

        self.msg = RemoteDriverDriveCommand()
        self.update_freq = 10.0
        self.store_data = True
        self.data = {
            "x": [],
            "y": [],
            "x_goal": [],
            "y_goal": [],
            "x_start": [],
            "y_start": [],
            "angle_north": [],
            "angle_north_init": [],
            "angle": [],
        }
        self.x = None 
        self.y = None
        self.current_ang = None
        self.x_start = None
        self.y_start = None
        self.init_angle = None
        self.radius = None
        self.drive_in_circle = False
        self.order = get_paint_order()
        self.calc_velocities = None  
        self.reached_goal = False
        self.angle_north = 0 

    def rtk_callback(self, rtk):
        if (self.x_start is None
            and self.y_start is None
            ):
                self.x_start= rtk.east
                self.y_start = rtk.north
                self.x_start_automower = rtk.east
                self.y_start_automower = rtk.north
                self.calc_velocities = CalcVelocities()
                change_goal(self)
                self.data["x_start"].append(self.x_start)
                self.data["y_start"].append(self.y_start)
                self.data["x_goal"].append(self.calc_velocities.x_goal)
                self.data["y_goal"].append(self.calc_velocities.y_goal)
            
        self.x = rtk.east
        self.y = rtk.north
        print('x,y:', self.x, self.y)
        lin_vel, ang_vel = self.calc_velocities.calc_vel(self.current_ang, self.x, self.y)
        self.msg.speed = lin_vel
        self.msg.steering = ang_vel
        self.data["y"].append(self.y)
        self.data["x"].append(self.x)
        if lin_vel == 0.0 and ang_vel == 0.0:
            change_goal(self)
            self.data["x_goal"].append(self.calc_velocities.x_goal)
            self.data["y_goal"].append(self.calc_velocities.y_goal)

    def imu_callback(self, imu):
        if  self.init_angle is None:
            self.init_angle = imu.yaw
        self.current_ang = imu.yaw

        #print('ang', self.current_ang)

    def move(self):
        signal.signal(signal.SIGINT, self.ctrlc_shutdown)

        self.thread = threading.Thread(target=rclpy.spin, args=(self,))
        self.thread.start()

        rate = self.create_rate(self.update_freq)
        while rclpy.ok() and not self.reached_goal:
            self.msg.header.stamp = self.get_clock().now().to_msg()
            print(self.msg)
            self.drive_publisher.publish(self.msg)
            rate.sleep()
        self.stop()
        
    def stop(self):
        self.msg.speed = 0.0
        self. msg.steering = 0.0
        self.drive_publisher.publish(self.msg)
        print('STOP!!!')
        plt.plot(self.data["x"], self.data["y"], "o-", label="Path", markersize=3)
        plt.plot(self.data["x_goal"], self.data["y_goal"], "rx", markersize=3, label="Goal")
        plt.xlabel("x ")
        plt.ylabel("y ")
        plt.show(block=True)
        # print(np.arctan2(np.mean(x_gps[0:70]) - y[0], np.mean(y_gps[0:70]) - x[0]), "angle_start3")
        #plt.xlabel("x ")
        #plt.ylabel("y ")
        #plt.title("Path and Goal")
        #plt.legend()
        #plt.axis("equal")
        print('x:',self.data["x"], 'y:',self.data["y"])
        
    def ctrlc_shutdown(self, sig, frame):
        self.stop()
        rclpy.shutdown()


if __name__ == '__main__':
    rclpy.init()
    drive_to = DriveTo()
    drive_to.move()
