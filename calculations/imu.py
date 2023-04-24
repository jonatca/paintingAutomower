from __future__ import print_function
import qwiic_icm20948
import time
import sys
import math

def runExample():

    print ("SparkFun 9DoF ICM-20948 Sensor  Example 1")
    IMU = qwiic_icm20948.QwiicIcm20948()

    if IMU.connected == False:
        print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    IMU.begin()

    while True:
        if IMU.dataReady():
            IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
            
            # Raw sensor readings
            ax = IMU.axRaw
            ay = IMU.ayRaw
            az = IMU.azRaw
            mx = IMU.mxRaw
            my = IMU.myRaw
            mz = IMU.mzRaw
            
            # Apply a correction to the magnetometer readings
            mag_declination = 0.0  # Magnetic declination for your location
            mag_offset_x = 0.0  # Hard iron offset in X direction
            mag_offset_y = 0.0  # Hard iron offset in Y direction
            mag_scale_x = 1.0  # Soft iron scale in X direction
            mag_scale_y = 1.0  # Soft iron scale in Y direction
            
            mx_corr = mag_scale_x * (mx - mag_offset_x)
            my_corr = mag_scale_y * (my - mag_offset_y)
            mz_corr = mz
            
            # Calculate yaw angle
            heading = math.atan2(my_corr, mx_corr)
            heading += mag_declination
            if heading < 0:
                heading += 2 * math.pi
            yaw = -math.degrees(heading)
            
            # Calculate pitch angle
            pitch = math.atan2(ax, math.sqrt(ay**2 + az**2))
            pitch = math.degrees(pitch)
            
            # Calculate roll angle
            roll = math.atan2(ay, az)
            roll = math.degrees(roll)
            
            # Print the yaw, pitch, and roll angles
            print("Yaw: {:.2f}  Pitch: {:.2f}  Roll: {:.2f}".format(yaw, pitch, roll))
            
            time.sleep(0.03)
        else:
            print('Waiting for data')
            time.sleep(0.5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print('\nEnding Example 1')
        sys.exit(0)