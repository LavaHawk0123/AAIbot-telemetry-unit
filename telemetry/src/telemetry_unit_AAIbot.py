#!/usr/bin/env python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
import socket
import time
from signal import signal, SIGPIPE, SIG_DFL
import threading
import sys
import cv2
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
import datetime
import pickle
import random
import numpy as np
import struct 
import zlib
import numpy as np
import json
from data_packet import PacketFunctions,dataPacket,telemetryDataStructure

class Ui_MainWindow(object):

    def declare_vars(self):
        self.L = []
        self.msg = {}
        # Variable Declerations
        host = socket.gethostname()
        self.IP = socket.gethostbyname(host)
        self.IP_add = "127.0.0.1"
        self.IP_add_c2 = "172.20.10.4"
        self.IP_add_c1 = "192.168.1.101"
        self.port1 = 9928
        self.port2 = 9047
        self.port3 = 9058
        self.port4 = 12345
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
        self.msg_dict = {}

        self.arrow_img = cv2.imread("/home/neo/AAIBot_ws/src/telemetry/images/arrow_ss.png")
        self.map_img = cv2.imread("/home/neo/AAIBot_ws/src/telemetry/images/Map_Screenshot.png")


        # Socket Declerations
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Thread declerations
        self.th_setCameraImageLabel = threading.Thread(target=self.getCameraUDP)
        self.th_setLabelValues = threading.Thread(target=self.getDataFromSocket)
        self.set_values_th = threading.Thread(target=self.set_values)
        self.addCoordinateThread = threading.Thread(target = self.addItemToList)
        self.signalStrengthThread = threading.Thread(target = self.setSignalLabels)


    def createGuiElements(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1568, 863)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pitchDia_label = QtWidgets.QLabel(self.centralwidget)
        self.pitchDia_label.setGeometry(QtCore.QRect(120, 100, 141, 71))
        self.pitchDia_label.setAutoFillBackground(True)
        self.pitchDia_label.setObjectName("pitchDia_label")

        self.rollDia_label = QtWidgets.QLabel(self.centralwidget)
        self.rollDia_label.setGeometry(QtCore.QRect(280, 100, 141, 71))
        self.rollDia_label.setAutoFillBackground(True)
        self.rollDia_label.setObjectName("rollDia_label")

        self.yawDia_label = QtWidgets.QLabel(self.centralwidget)
        self.yawDia_label.setGeometry(QtCore.QRect(440, 100, 141, 71))
        self.yawDia_label.setAutoFillBackground(True)
        self.yawDia_label.setObjectName("yawDia_label")

        self.pitch_label = QtWidgets.QLabel(self.centralwidget)
        self.pitch_label.setGeometry(QtCore.QRect(110, 190, 151, 17))
        self.pitch_label.setAutoFillBackground(True)
        self.pitch_label.setObjectName("pitch_label")

        self.roll_label = QtWidgets.QLabel(self.centralwidget)
        self.roll_label.setGeometry(QtCore.QRect(280, 190, 141, 17))
        self.roll_label.setAutoFillBackground(True)
        self.roll_label.setObjectName("roll_label")

        self.yaw_label = QtWidgets.QLabel(self.centralwidget)
        self.yaw_label.setGeometry(QtCore.QRect(440, 190, 141, 20))
        self.yaw_label.setAutoFillBackground(True)
        self.yaw_label.setObjectName("yaw_label")

        self.trans_lbl4 = QtWidgets.QLabel(self.centralwidget)
        self.trans_lbl4.setGeometry(QtCore.QRect(610, 100, 41, 17))
        self.trans_lbl4.setAutoFillBackground(True)
        self.trans_lbl4.setObjectName("trans_lbl4")

        self.trans_lbl3 = QtWidgets.QLabel(self.centralwidget)
        self.trans_lbl3.setGeometry(QtCore.QRect(610, 120, 41, 17))
        self.trans_lbl3.setAutoFillBackground(True)
        self.trans_lbl3.setObjectName("trans_lbl3")

        self.trans_lbl2 = QtWidgets.QLabel(self.centralwidget)
        self.trans_lbl2.setGeometry(QtCore.QRect(610, 140, 41, 17))
        self.trans_lbl2.setAutoFillBackground(True)
        self.trans_lbl2.setObjectName("trans_lbl2")

        self.trans_lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.trans_lbl1.setGeometry(QtCore.QRect(610, 160, 41, 17))
        self.trans_lbl1.setAutoFillBackground(True)
        self.trans_lbl1.setObjectName("trans_lbl1")

        self.recv_lbl2 = QtWidgets.QLabel(self.centralwidget)
        self.recv_lbl2.setGeometry(QtCore.QRect(670, 140, 41, 17))
        self.recv_lbl2.setAutoFillBackground(True)
        self.recv_lbl2.setObjectName("recv_lbl2")

        self.recv_lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.recv_lbl1.setGeometry(QtCore.QRect(670, 160, 41, 17))
        self.recv_lbl1.setAutoFillBackground(True)
        self.recv_lbl1.setObjectName("recv_lbl1")

        self.recv_lbl3 = QtWidgets.QLabel(self.centralwidget)
        self.recv_lbl3.setGeometry(QtCore.QRect(670, 120, 41, 17))
        self.recv_lbl3.setAutoFillBackground(True)
        self.recv_lbl3.setObjectName("recv_lbl3")

        self.recv_lbl4 = QtWidgets.QLabel(self.centralwidget)
        self.recv_lbl4.setGeometry(QtCore.QRect(670, 100, 41, 17))
        self.recv_lbl4.setAutoFillBackground(True)
        self.recv_lbl4.setObjectName("recv_lbl4")

        self.transmit_label = QtWidgets.QLabel(self.centralwidget)
        self.transmit_label.setGeometry(QtCore.QRect(590, 190, 71, 20))
        self.transmit_label.setAutoFillBackground(True)
        self.transmit_label.setObjectName("transmit_label")

        self.recv_label = QtWidgets.QLabel(self.centralwidget)
        self.recv_label.setGeometry(QtCore.QRect(660, 190, 71, 20))
        self.recv_label.setAutoFillBackground(True)
        self.recv_label.setObjectName("recv_label")

        self.packetSent_heading = QtWidgets.QLabel(self.centralwidget)
        self.packetSent_heading.setGeometry(QtCore.QRect(730, 100, 111, 17))
        self.packetSent_heading.setAutoFillBackground(True)
        self.packetSent_heading.setObjectName("packetSent_heading")

        self.packetsRecvd_heading = QtWidgets.QLabel(self.centralwidget)
        self.packetsRecvd_heading.setGeometry(QtCore.QRect(730, 130, 101, 17))
        self.packetsRecvd_heading.setAutoFillBackground(True)
        self.packetsRecvd_heading.setObjectName("packetsRecvd_heading")

        self.ping_heading = QtWidgets.QLabel(self.centralwidget)
        self.ping_heading.setGeometry(QtCore.QRect(730, 160, 67, 17))
        self.ping_heading.setAutoFillBackground(True)
        self.ping_heading.setObjectName("ping_heading")

        self.ss_heading = QtWidgets.QLabel(self.centralwidget)
        self.ss_heading.setGeometry(QtCore.QRect(730, 190, 111, 17))
        self.ss_heading.setAutoFillBackground(True)
        self.ss_heading.setObjectName("ss_heading")

        self.ping_val = QtWidgets.QLabel(self.centralwidget)
        self.ping_val.setGeometry(QtCore.QRect(850, 160, 111, 17))
        self.ping_val.setAutoFillBackground(True)
        self.ping_val.setObjectName("ping_val")

        self.sent_val = QtWidgets.QLabel(self.centralwidget)
        self.sent_val.setGeometry(QtCore.QRect(850, 100, 111, 17))
        self.sent_val.setAutoFillBackground(True)
        self.sent_val.setObjectName("sent_val")

        self.ss_val = QtWidgets.QLabel(self.centralwidget)
        self.ss_val.setGeometry(QtCore.QRect(850, 190, 111, 17))
        self.ss_val.setAutoFillBackground(True)
        self.ss_val.setObjectName("ss_val")

        self.recv_val = QtWidgets.QLabel(self.centralwidget)
        self.recv_val.setGeometry(QtCore.QRect(850, 130, 111, 17))
        self.recv_val.setAutoFillBackground(True)
        self.recv_val.setObjectName("recv_val")

        self.map_label = QtWidgets.QLabel(self.centralwidget)
        self.map_label.setGeometry(QtCore.QRect(940, 430, 601, 301))
        self.map_label.setAutoFillBackground(True)
        self.map_label.setObjectName("map_label")

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(20, 250, 901, 501))
        self.image_label.setAutoFillBackground(True)
        self.image_label.setObjectName("image_label")

        self.menu_heading = QtWidgets.QLabel(self.centralwidget)
        self.menu_heading.setGeometry(QtCore.QRect(36, 100, 71, 20))
        self.menu_heading.setAutoFillBackground(True)
        self.menu_heading.setObjectName("menu_heading")

        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(10, 130, 89, 25))
        self.connect_btn.setAutoFillBackground(True)
        self.connect_btn.setObjectName("connect_btn")

        self.showImage_btn = QtWidgets.QPushButton(self.centralwidget)
        self.showImage_btn.setGeometry(QtCore.QRect(10, 170, 89, 25))
        self.showImage_btn.setAutoFillBackground(True)
        self.showImage_btn.setObjectName("showImage_btn")

        self.showMap_btn = QtWidgets.QPushButton(self.centralwidget)
        self.showMap_btn.setGeometry(QtCore.QRect(10, 210, 89, 25))
        self.showMap_btn.setAutoFillBackground(True)
        self.showMap_btn.setObjectName("showMap_btn")

        self.imu_heading = QtWidgets.QLabel(self.centralwidget)
        self.imu_heading.setGeometry(QtCore.QRect(940, 231, 271, 20))
        self.imu_heading.setAutoFillBackground(True)
        self.imu_heading.setObjectName("imu_heading")

        self.imuOrientation_x = QtWidgets.QLabel(self.centralwidget)
        self.imuOrientation_x.setGeometry(QtCore.QRect(940, 270, 271, 21))
        self.imuOrientation_x.setAutoFillBackground(True)
        self.imuOrientation_x.setObjectName("imuOrientation_x")

        self.imuOrientation_y = QtWidgets.QLabel(self.centralwidget)
        self.imuOrientation_y.setGeometry(QtCore.QRect(940, 310, 271, 21))
        self.imuOrientation_y.setAutoFillBackground(True)
        self.imuOrientation_y.setObjectName("imuOrientation_y")

        self.imuOrientation_z = QtWidgets.QLabel(self.centralwidget)
        self.imuOrientation_z.setGeometry(QtCore.QRect(940, 350, 271, 21))
        self.imuOrientation_z.setAutoFillBackground(True)
        self.imuOrientation_z.setObjectName("imuOrientation_z")

        self.imuOrientation_w = QtWidgets.QLabel(self.centralwidget)
        self.imuOrientation_w.setGeometry(QtCore.QRect(940, 390, 271, 21))
        self.imuOrientation_w.setAutoFillBackground(True)
        self.imuOrientation_w.setObjectName("imuOrientation_w")

        self.gps_heading = QtWidgets.QLabel(self.centralwidget)
        self.gps_heading.setGeometry(QtCore.QRect(1230, 240, 271, 21))
        self.gps_heading.setAutoFillBackground(True)
        self.gps_heading.setObjectName("gps_heading")

        self.gpsLat_val = QtWidgets.QLabel(self.centralwidget)
        self.gpsLat_val.setGeometry(QtCore.QRect(1230, 280, 271, 21))
        self.gpsLat_val.setAutoFillBackground(True)
        self.gpsLat_val.setObjectName("gpsLat_val")

        self.gpsLong_value = QtWidgets.QLabel(self.centralwidget)
        self.gpsLong_value.setGeometry(QtCore.QRect(1230, 320, 271, 21))
        self.gpsLong_value.setAutoFillBackground(True)
        self.gpsLong_value.setObjectName("gpsLong_value")

        self.saveCoordinate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.saveCoordinate_btn.setGeometry(QtCore.QRect(1230, 360, 141, 25))
        self.saveCoordinate_btn.setObjectName("saveCoordinate_btn")

        self.plot_btn = QtWidgets.QPushButton(self.centralwidget)
        self.plot_btn.setGeometry(QtCore.QRect(1380, 360, 131, 25))
        self.plot_btn.setObjectName("plot_btn")

        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_label.setGeometry(QtCore.QRect(30, 10, 91, 71))
        self.logo_label.setAutoFillBackground(True)
        self.logo_label.setObjectName("logo_label")

        self.heading_label = QtWidgets.QLabel(self.centralwidget)
        self.heading_label.setGeometry(QtCore.QRect(140, 30, 581, 51))
        font = QtGui.QFont()
        font.setFamily("Uroob")
        font.setPointSize(34)
        self.heading_label.setFont(font)
        self.heading_label.setAutoFillBackground(True)
        self.heading_label.setObjectName("heading_label")

        self.tmr_label = QtWidgets.QLabel(self.centralwidget)
        self.tmr_label.setGeometry(QtCore.QRect(980, 90, 231, 17))
        self.tmr_label.setAutoFillBackground(True)
        self.tmr_label.setObjectName("tmr_label")

        self.tmr_val = QtWidgets.QLabel(self.centralwidget)
        self.tmr_val.setGeometry(QtCore.QRect(1010, 120, 171, 41))
        self.tmr_val.setAutoFillBackground(True)
        self.tmr_val.setObjectName("tmr_val")

        self.tmrStart_btn = QtWidgets.QPushButton(self.centralwidget)
        self.tmrStart_btn.setGeometry(QtCore.QRect(990, 180, 89, 25))
        self.tmrStart_btn.setObjectName("tmrStart_btn")

        self.tmrReset_btn = QtWidgets.QPushButton(self.centralwidget)
        self.tmrReset_btn.setGeometry(QtCore.QRect(1090, 180, 89, 25))
        self.tmrReset_btn.setObjectName("tmrReset_btn")

        self.waypoints_list = QtWidgets.QListWidget(self.centralwidget)
        self.waypoints_list.setGeometry(QtCore.QRect(1200, 111, 351, 111))
        self.listItem = "latitude" +"\t\t"+ "longitude"
        self.waypoints_list.addItem(self.listItem)
        self.waypoints_list.setObjectName("waypoints_list")

        self.watpoints_heading = QtWidgets.QLabel(self.centralwidget)
        self.watpoints_heading.setGeometry(QtCore.QRect(1340, 80, 81, 17))
        self.watpoints_heading.setObjectName("watpoints_heading")

        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setGeometry(QtCore.QRect(1458, 760, 101, 25))
        self.close_btn.setObjectName("close_btn")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1568, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
            self.declare_vars()
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.pitchDia_label.setText(_translate("MainWindow", "Pitch"))
            self.rollDia_label.setText(_translate("MainWindow", "Roll"))
            self.yawDia_label.setText(_translate("MainWindow", "Yaw"))
            self.pitch_label.setText(_translate("MainWindow", "Pitch Angle"))
            self.roll_label.setText(_translate("MainWindow", "Roll Angle"))
            self.yaw_label.setText(_translate("MainWindow", "Yaw Angle"))
            self.trans_lbl4.setText(_translate("MainWindow", "lv4"))
            self.trans_lbl3.setText(_translate("MainWindow", "lv3"))
            self.trans_lbl2.setText(_translate("MainWindow", "lv2"))
            self.trans_lbl1.setText(_translate("MainWindow", "lv1"))
            self.recv_lbl2.setText(_translate("MainWindow", "lv2"))
            self.recv_lbl1.setText(_translate("MainWindow", "lv1"))
            self.recv_lbl3.setText(_translate("MainWindow", "lv3"))
            self.recv_lbl4.setText(_translate("MainWindow", "lv4"))
            self.transmit_label.setText(_translate("MainWindow", "Transmit"))
            self.recv_label.setText(_translate("MainWindow", "Recieve"))
            self.packetSent_heading.setText(_translate("MainWindow", "Packets Sent : "))
            self.packetsRecvd_heading.setText( _translate("MainWindow", "Recieved: "))
            self.ping_heading.setText(_translate("MainWindow", "Ping"))
            self.ss_heading.setText(_translate("MainWindow", "Signal Strength:"))
            self.ping_val.setText(_translate("MainWindow", "Ping(ms)"))
            self.sent_val.setText(_translate("MainWindow", "sent"))
            self.ss_val.setText(_translate("MainWindow", "mbps"))
            self.recv_val.setText(_translate("MainWindow", "Recieved: "))
            self.map_label.setText(_translate("MainWindow", "Map "))
            self.image_label.setText(_translate("MainWindow", "Image"))
            self.menu_heading.setText(_translate("MainWindow", "MENU"))
            self.connect_btn.setText(_translate("MainWindow", "Connect"))
            self.showImage_btn.setText(_translate("MainWindow", "Show Image"))
            self.showMap_btn.setText(_translate("MainWindow", "Show Map"))
            self.imu_heading.setText(_translate("MainWindow", "IMU Values : "))
            self.imuOrientation_x.setText(_translate("MainWindow", "Orientation_x"))
            self.imuOrientation_y.setText(_translate("MainWindow", "Orientation_y"))
            self.imuOrientation_z.setText(_translate("MainWindow", "Orientation_z"))
            self.imuOrientation_w.setText(_translate("MainWindow", "Orientation_w"))
            self.gps_heading.setText(_translate("MainWindow", "GPS Values : "))
            self.gpsLat_val.setText(_translate("MainWindow", "Latitude : "))
            self.gpsLong_value.setText(_translate("MainWindow", "Longitude:"))
            self.saveCoordinate_btn.setText(_translate("MainWindow", "Save Coordinate"))
            self.plot_btn.setText(_translate("MainWindow", "Plot Point"))
            self.logo_label.setText(_translate("MainWindow", "Logo"))
            self.heading_label.setText(_translate("MainWindow", "AAIBot Telemetry Unit"))
            self.tmr_label.setText(_translate("MainWindow", "Timer"))
            self.tmr_val.setText(_translate("MainWindow", "00 Hrs 00 Mins"))
            self.tmrStart_btn.setText(_translate("MainWindow", "Start"))
            self.tmrReset_btn.setText(_translate("MainWindow", "Reset"))
            self.watpoints_heading.setText(_translate("MainWindow", "Waypoints"))
            self.close_btn.setText(_translate("MainWindow", "Close"))
            self.gui_buttonevents()
    
    def setupUi(self, MainWindow):
        self.createGuiElements(MainWindow)


    # Convert from an opencv image to QPixmap
    def convert_cv_qt(self, cv_img, width, hieght):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, hieght, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    
    def gui_buttonevents(self):
        self.close_btn.clicked.connect(self.exit_gui)
        self.showImage_btn.clicked.connect(self.Display_Image)
        self.connect_btn.clicked.connect(self.getDataFromPipeline)
        self.showMap_btn.clicked.connect(self.getDataFromPipeline)
        self.saveCoordinate_btn.clicked.connect(self.startListThread)
    
    def Display_Image(self):
        self.th_setCameraImageLabel.start()

    def setLabelValues(self):
        self.set_values_th.start()

    def addItemToList(self):
        self.listItem = str(self.gps_latitude) +"\t\t"+ str(self.gps_longitude)
        self.waypoints_list.addItem(self.listItem)

    def startListThread(self):
        self.addItemToList()


    def getDataFromPipeline(self):
        self.th_setLabelValues.start()
        self.set_values_th.start()
        self.setAngleLabels()
        self.signalStrengthThread.start()
    
    def getDataFromSocket(self):
        self.s1.connect((self.IP_add, self.port3))
        while True:
            time.sleep(2)
            self.msg = self.s1.recv(1024).decode()
            print("\nRecieved Message"+ self.msg)
            self.msg_dict = json.loads(self.msg)
            self.L = self.msg_dict['data'].split(",")
            telemData = telemetryDataStructure()
            telemData.assignValuefromList(self.L)
            telemData.printDataLog()
            self.assignClassVariableValues()


    def printIncomingData(self):
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


    def getCameraImage(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, self.cv_img = cap.read()
            self.qt_img = self.convert_cv_qt(self.cv_img, 791, 571)
            self.image_label.setPixmap(self.qt_img)

    def getCameraUDP(self):
        max_length = 65540
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.IP_add, self.port1))
        frame_info = None
        buffer = None
        frame = None
        print("-> waiting for connection")
        while True:
            data, address = sock.recvfrom(max_length)
            if len(data) < 100:
                frame_info = pickle.loads(data)

                if frame_info:
                    nums_of_packs = frame_info["packs"]

                    for i in range(nums_of_packs):
                        data, address = sock.recvfrom(max_length)

                        if i == 0:
                            buffer = data
                        else:
                            buffer += data

                    frame = np.frombuffer(buffer, dtype=np.uint8)
                    frame = frame.reshape(frame.shape[0], 1)

                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    frame = cv2.flip(frame, 1)

                    if frame is not None and type(frame) == np.ndarray:
                        self.cv_img = frame
                        self.qt_img = self.convert_cv_qt(self.cv_img, 791, 571)
                        self.image_label.setPixmap(self.qt_img)
    
    def setAngleLabels(self):
        self.qt_img_map = self.convert_cv_qt(self.map_img, 601, 301)
        self.map_label.setPixmap(self.qt_img_map)
    
    def setMapLabel(self):
        self.qt_img_map = self.convert_cv_qt(self.map_img, 601, 301)
        self.map_label.setPixmap(self.qt_img_map)

    def setSignalLabels(self):
        transLabelList = [self.trans_lbl1,self.trans_lbl2,self.trans_lbl3,self.trans_lbl4]
        recvLabelList = [self.trans_lbl1,self.trans_lbl2,self.trans_lbl3,self.trans_lbl4]
        while True:
            n_send = random.randint(0,5)
            n_recv = random.randint(0,5)
            for i in range(1,n_send):
                n_send = random.randint(0,5)

                transLabelList[i].setText("")
                transLabelList[i].setStyleSheet("background-color: green")
            for i in range(1,n_recv):
                n_recv = random.randint(0,5)
                recvLabelList[i].setText("")
                recvLabelList[i].setStyleSheet("background-color: green")


    def exit_gui(self):
        self.th_setCameraImageLabel.join()
        self.th_setLabelValues.join()
        self.set_values_th.join()
        print("Cleaning Up and Exiting...")
        time.sleep(3)
        sys.exit(0)

    def set_values(self):
        while True:
            _translate = QtCore.QCoreApplication.translate
            self.pitch_label.setText(_translate("MainWindow", str(self.imu_pitch)))
            self.roll_label.setText(_translate("MainWindow", str(self.imu_roll)))
            self.yaw_label.setText(_translate("MainWindow", str(self.imu_yaw)))
            self.sent_val.setText(_translate("MainWindow", str(self.packets_sent)))
            self.recv_val.setText(_translate("MainWindow", str(self.packets_recv)))
            self.ping_val.setText(_translate("MainWindow", str(self.ping)))
            self.ss_val.setText(_translate("MainWindow", str(self.signal_strength)))
            self.imuOrientation_x.setText(_translate("MainWindow", str(self.imu_quat_x)))
            self.imuOrientation_y.setText(_translate("MainWindow", str(self.imu_quat_y)))
            self.imuOrientation_z.setText(_translate("MainWindow", str(self.imu_quat_z)))
            self.imuOrientation_w.setText(_translate("MainWindow", str(self.imu_quat_w)))
            self.gpsLong_value.setText(_translate("MainWindow", str(self.gps_latitude)))
            self.gpsLat_val.setText(_translate("MainWindow", str(self.gps_longitude)))    

def create_GUI():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        create_GUI()
    except KeyboardInterrupt:
        print("Shutting Down Program")
        sys.exit(0)
