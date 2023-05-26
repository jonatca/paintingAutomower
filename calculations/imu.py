from __future__ import print_function
#import qwiic_icm20948
import time
import sys
import math

def get_yaw_angle():
    IMU = qwiic_icm20948.QwiicIcm20948()

    if IMU.connected == False:
        print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    IMU.begin()
    
    while True:
        if IMU.dataReady():
            IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables

            mx = IMU.mxRaw
            my = IMU.myRaw
            ax = IMU.axRaw
            ay = IMU.ayRaw
            az = IMU.azRaw
            
           # Combine magnetometer and gyro readings for yaw angle
            yaw = math.atan2(my, mx)
            if yaw < 0:
                yaw += 2 * math.pi
            yaw = math.degrees(yaw)

            north_angle = 180 # Try and set it to where north is facing
            degrees_to_north = yaw - north_angle
            
            # Calculate pitch angle
            pitch = math.atan2(ax, math.sqrt(ay**2 + az**2))
            pitch = math.degrees(pitch)

            # Calculate roll angle
            roll = math.atan2(ay, az)
            roll = math.degrees(roll)

            # Print the yaw angle
            #print("Pitch: {:.2f} Roll:{:.2f}  ".format(pitch, roll))
            print("Yaw: {:.2f} ".format(yaw))
            #print("north: {:.2f} ".format(degrees_to_north))
            # return degrees_to_north*math.pi/180.
            
            time.sleep(0.03)
        else:
            print('Waiting for data')
            time.sleep(0.5)

if __name__ == '__main__':
    try:
        get_yaw_angle()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print('\nEnding Example 1')
        sys.exit(0)
