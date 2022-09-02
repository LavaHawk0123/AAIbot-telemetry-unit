import json
import sys
from datetime import datetime

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
