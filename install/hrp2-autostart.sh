#!/bin/bash
#enable can
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 txqueuelen 5000
#activate
source /opt/ros/galactic/setup.bash
source /home/GMEO/paintingAutomower/install/local_setup.bash

ros2 launch hrp_pkg hrp_keepalive.launch.py
#ros2 launch hrp_pkg hrp.launch.py
