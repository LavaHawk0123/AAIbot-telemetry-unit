

"""
Maintainer - Aditya Arun Iyer
Last Modified - 02/09/2022 13:06 PM

The below driver code contains the class defenition for the data packet

Run Location : N/A

"""

import json
import sys
from datetime import datetime
import numpy as np

class telemetryDataStructure:
    def __init__(self):
        self.L = []
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

    def assignValuefromList(self,L):
        self.L = L
        self.assignClassVariableValues()

    def assignClassVariableValues(self):
        self.imu_roll = np.double(self.L[0])
        self.imu_pitch = np.double(self.L[1])
        self.imu_yaw = np.double(self.L[2])
        self.packets_sent = np.double(self.L[3])
        self.packets_recv = np.double(self.L[4])
        self.ping = np.double(self.L[5])
        self.signal_strength = np.double(self.L[6])
        self.imu_quat_x = "IMU Orientation_x: "+str(np.double(self.L[7]))
        self.imu_quat_y = "IMU Orientation_y: "+str(np.double(self.L[8]))
        self.imu_quat_z = "IMU Orientation_z: "+str(np.double(self.L[9]))
        self.imu_quat_w = "IMU Orientation_w: "+str(np.double(self.L[10]))
        self.gps_latitude = "Latitude: "+str(np.double(self.L[11]))
        self.gps_longitude = "Longitude: "+str(np.double(self.L[12]))
    
    def printDataLog(self):
        print("Telemetry Data Log : ")
        print("Roll : "+str(self.imu_roll))
        print("Pitch : "+str(self.imu_pitch))
        print("Yaw : "+str(self.imu_yaw))
        print("Packets Sent : "+str(self.packets_sent))
        print("Packets Recv : "+str(self.packets_recv))
        print("Ping : "+str(self.ping))
        print("Signal Strength : "+str(self.signal_strength))
        print("Quat X : "+str(self.imu_quat_x))
        print("Quat Y : "+str(self.imu_quat_y))
        print("Quat Z : "+str(self.imu_quat_z))
        print("Quat W : "+str(self.imu_quat_w))
        print("Latitude : "+str(self.gps_latitude))
        print("Longitude : "+str(self.gps_longitude))

class dataPacket:
    def __init__(self,sourceip,sourceport,destip,destport):
    
    # Data section of the Packet
        
        # {data} Contains the data to be sent to the base station
        self.data = ""
        self.data_dict = {}

    # Header of the data packet has been defined

        # {time} Contains the time of data packet creation to the header
        # Default - Contains the time the connection was initiated
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # {source_ip} - Contains the destination IP address to the header
        self.source_ip = sourceip

        # {source_port} - Contains the port the packet has to be sent to
        self.source_port = sourceport

        # {dest_ip} - Contains the destination IP address to the header
        self.dest_ip = destip

        # {dest_port} - Contains the port the packet has to be sent to
        self.dest_port = destport

        # {checksum} - Check value for data integrity check
        self.checksum = self.initCheckSum()

        # {size} - Contains the size of the data packet being sent
        self.packet_size = 0

        # {seq_num} - Specifies the sequence number of the current data packet
        # Note : must be defined externally and assigned
        self.seq_num = 0

        # Flag variables for the header
        self.ACK_FLAG = 1 # Indicates that acknowledgement number is valid.
        self.RST_FLAG = 0 # Resets the connection.
        self.URG_FLAG = 0 # Indicates that some urgent data has been placed.
        self.FIN_FLAG = 0 # It is used to terminate the connection

    # Driver Functions to enhance access and control

    # Function to configure details of the destination ip and port no
    def setDestDetails(self,ip,port):
        self.dest_ip = ip
        self.dest_port = port

    # Function to configure details of the source ip and port no
    def setSourceDetails(self,ip,port):
        self.source_ip = ip
        self.source_port = port

    # Function to return a str object of the class details
    def getParams(self):
        class_dict = self.__dict__
        return class_dict

    # Function to initialise checksum for the given dataPacket
    def initCheckSum(self):
        check = sys.getsizeof(self.data)
        return check

    # Function to assign sequence number to the data packet 
    def assignSeqNum(self,seq):
        self.seq_num = seq

    # Function to assign data to the data segment 
    def assignData(self,data):
        self.data = data

    # Function to assign packet size {In case it is variable}
    def assignPacketSize(self,packet):
        self.packet_size = sys.getsizeof(packet)
    
    def serializeDataSection(self,packet):
        self.data_dict = packet.data.__dict__


# Class to provide Client and Server side programs access and functionality to data packets
class PacketFunctions:
    # Function to validate data packets
    def validateCheckSum(self,packet):
        if(sys.getsizeof(packet.data)==packet.checksum):
            print("Packet {} validated. 0% packet loss".format(packet.seq_num))
            return 1   
        else:
            loss = sys.getsizeof(packet.data)-packet.checksum
            perc_loss = (loss/sys.getsizeof(packet.data))*100
            print("Packet {} validated. 0% packet loss".format(str(perc_loss)))
            return 0
        return "Unable to validate checksum"
