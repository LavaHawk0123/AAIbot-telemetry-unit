#!/usr/bin/env python3

import socket
import time
import rospy
import threading
from data_packet import dataPacket,PacketFunctions
import json

class Connect_Socket:

    def __init__(self):
        # Variable Declerations
        self.IP_add_c1 = "127.0.0.1"
        self.port3 = 9058
        self.imu_roll = 0.0
        self.imu_pitch = 0.0
        self.imu_yaw = 0.0
        self.packets_sent = 0
        self.packets_recv = 0
        self.ping = 0.00
        self.signal_strength = 0.0
        self.imu_quat_x = 0.0000
        self.imu_quat_y = 0.0000
        self.imu_quat_z = 0.0000
        self.imu_quat_w = 0.0000
        self.gps_latitude = 0.000000
        self.gps_longitude = 0.000000
        self.msg = ''
        self.msg_to_send = ''
        self.data_packet_msg = ''

        # Socket Declerations
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Thread declerations
        self.th_Testbench = threading.Thread(target=self.Testbench)
        self.th_send_params = threading.Thread(target=self.send_params)
    
    def Testbench(self):
        while not rospy.is_shutdown():
            time.sleep(1)
            self.imu_roll = rospy.get_param("/IMU/Roll")
            self.imu_pitch = rospy.get_param("/IMU/Pitch")
            self.imu_yaw = rospy.get_param("/IMU/Yaw")
            self.packets_sent = rospy.get_param("/Packets/Sent")
            self.packets_recv = rospy.get_param("/Packets/Recieved")
            self.ping = rospy.get_param("/ping")
            self.signal_strength = rospy.get_param("/signalStrength")
            self.imu_quat_x = rospy.get_param("/IMU/Quat/x")
            self.imu_quat_y = rospy.get_param("/IMU/Quat/y")
            self.imu_quat_z = rospy.get_param("/IMU/Quat/z")
            self.imu_quat_w = rospy.get_param("/IMU/Quat/w")
            self.gps_latitude = rospy.get_param("/GPS/latitude")
            self.gps_longitude = rospy.get_param("/GPS/longitude")
            self.msg = str(self.imu_roll) + ","+str(self.imu_pitch)+","+str(self.imu_yaw)+","+str(self.packets_sent)+","+str(self.packets_recv)+","+str(self.ping)+","+str(self.signal_strength)+","+str(self.imu_quat_x)+","+str(self.imu_quat_y)+","+str(self.imu_quat_z)+","+str(self.imu_quat_w)+","+str(self.gps_latitude)+","+str(self.gps_longitude)
            rospy.set_param('gui_msg',self.msg)
            print("Updated Message")
            time.sleep(5)

    def createDataPacket(self,data,seq_num):
        packet = dataPacket(self.IP_add_c1,self.port3)
        packet.assignData(data)
        packet.assignSeqNum(seq_num)
        packet.initCheckSum()
        return packet

    
    def send_params(self):

        # binding port and host
        self.s1.bind((self.IP_add_c1, self.port3))
        print("Waiting for client to connect")

        # waiting for a client to connect
        self.s1.listen(5)
        c, addr = self.s1.accept() 
        seq_num = 0
        while True:
            self.msg_to_send = rospy.get_param('gui_msg')
            seq_num+=1
            self.data_packet = self.createDataPacket(self.msg_to_send,seq_num)
            # sending data type should be string and encode before sending
            print("sent msg : {}".format(self.data_packet.getParams()))
            self.data_packet_msg = self.data_packet.getParams()
            self.data_packet_msg = json.dumps(self.data_packet_msg)
            c.send(self.data_packet_msg.encode())
            time.sleep(5)


    def driver(self):
        self.th_Testbench.start()
        time.sleep(3)
        self.th_send_params.start()

if __name__ == '__main__':
    rospy.init_node('test_sender')
    sock_obj = Connect_Socket()
    sock_obj.driver()
