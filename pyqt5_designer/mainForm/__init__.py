# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:24:40 2019

@author: hj823
"""

from PyQt5 import QtWidgets, uic
import os
from pyModbusTCP.client import ModbusClient
from secondForm import SecondUi   # 讀入我們設計的Main Window

path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile_main = path + os.sep + "ui" + os.sep + "Main_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)
c1 = ModbusClient() #define modbus server host, port

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.line_ip.setText("192.168.1.1")
        self.line_port.setText("502")
        self.b_window = SecondUi(c1)
        self.button_enter.clicked.connect(self.turn_interface)
        print('b_window')
        
    def turn_interface(self):
        ip = self.line_ip.text()
        port = int(self.line_port.text())
        c1.host(ip)
        c1.port(port)
        c1.unit_id(1) #set UID to 1
        c1.timeout(2)
        c1.auto_open(True)
        c1.auto_close(True)
        # uncomment this line to see debug message
        c1.debug(True)

        print(c1)
        if not c1.is_open():
            if not c1.open():
                print("unable to connect to "+ip+":"+str(port))
            else:
                print("connected !!")
        if ip=="" or port=="":
            print("keyin the ip or port")
        elif c1.open():
            self.b_window.show()
            