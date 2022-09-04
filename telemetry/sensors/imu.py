#!/usr/bin/env python3
import serial
import rospy
from sensor_msgs.msg import Imu
if __name__ == '__main__':
    rospy.init_node('imu_bno', anonymous=True)
    imu_msg = Imu()
    pub = rospy.Publisher('imu', Imu, queue_size=10)
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    roll=0
    pitch=0
    yaw=0
    while not rospy.is_shutdown():
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip().split(',')
                if(line.__str__() == ''):
                    continue
                elif(line[0]=='r'):
                    roll = float(line[1])
                    print("got roll : {}".format(roll))
                elif(line[0]=='p'):
                    print("got pitch : {}".format(pitch))
                    pitch = float(line[1])
                elif(line[0]=='y'):
                    print("got yaw : {}".format(yaw))
                    yaw = float(line[1])
                rospy.set_param("/IMU/Roll",roll)
                rospy.set_param("/IMU/Pitch",pitch)
                rospy.set_param("/IMU/Yaw",yaw)
        except rospy.ROSInterruptException:
            break
