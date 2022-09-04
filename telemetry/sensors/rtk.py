#!/usr/bin/env python3
import serial
from sensor_msgs.msg import NavSatFix
from ublox_gps import UbloxGps
import rospy

rospy.init_node('GPS', anonymous=True)
port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=0.1)
gps = UbloxGps(port)


def run():

    try:
        print("Listening for UBX Messages")
        rtk = NavSatFix()
        while not rospy.is_shutdown():
            try:
                geo = gps.geo_coords()
                print(geo.lat,geo.lon)
                rtk.longitude = geo.lon
                rtk.latitude = geo.lat
                print("current lat : "+str(rtk.latitude)+" current long : "+str(rtk.longitude))
                rospy.set_param("/GPS/latitude",rtk.latitude)
                rospy.set_param("/GPS/longitude",rtk.longitude)
            except rospy.ROSInterruptException():
                break

    except:
        pass
        


if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass


