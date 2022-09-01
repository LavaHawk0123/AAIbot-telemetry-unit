#!/usr/bin/env python3
import rospy
import time
import sys
rospy.init_node('load_param_testbench')
i= 1.123311
while True:
	try:
		rospy.set_param("/IMU/Roll",i) # dONE
		rospy.set_param("/IMU/Pitch",i) #dONE
		rospy.set_param("/IMU/Yaw",i) #Done
		rospy.set_param("/Packets/Sent",i) #Done
		rospy.set_param("/Packets/Recieved",i) #Done
		rospy.set_param("/ping",i) #Done
		rospy.set_param("/signalStrength",i) #DOne
		rospy.set_param("/IMU/Quat/x",i) 
		rospy.set_param("/IMU/Quat/y",i)
		rospy.set_param("/IMU/Quat/z",i)
		rospy.set_param("/IMU/Quat/w",i)
		rospy.set_param("/GPS/latitude",i)
		rospy.set_param("/GPS/longitude",i)
	except KeyboardInterrupt:
		sys.exit(0)
	time.sleep(0.1)
