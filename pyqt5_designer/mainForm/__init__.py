# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:24:40 2019

@author: hj823
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLCDNumber
import os
from pyModbusTCP.client import ModbusClient
from Backend import BackendThread
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
        self.b_window = SecondUi()
        self.button_enter.clicked.connect(self.turn_interface)
        print('b_window')
        
    def turn_interface(self):
        ip = self.line_ip.text()
        port = int(self.line_port.text())
        print("ip",type(ip))
        print("port",type(port))
        c1.host(ip)
        c1.port(port)
        c1.unit_id(1) #set UID to 1
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
            regs = c1.read_holding_registers(0x6E, 1)
            print('regs:\n',regs)
            self.b_window.show()

# 設計好的ui檔案路徑
qtCreatorFile_second = path + os.sep + "ui" + os.sep + "Second_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_SecondWindow, QtBaseClass_second = uic.loadUiType(qtCreatorFile_second)
firebase_url="https://smartmanu-af015.firebaseio.com/.json"
class SecondUi(QtWidgets.QMainWindow, Ui_SecondWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.lcd_volt.setDigitCount(5)
        self.lcd_volt.setMode(QLCDNumber.Dec)
        self.lcd_volt.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.initUI()
    def initUI(self):
        self.button_thread.clicked.connect(self.display)
        self.button_auto.clicked.connect(self.auto_mode)
    def auto_mode(self):
        if self.button_auto.text()=='自動模式':
            self.auto_mode = False
            self.button_auto.setText('手動模式')
        else:
            self.auto_mode = True
            self.button_auto.setText('自動模式')
    def display(self):
        self.thread_set()
        self.read_volt()
        self.display_volt()
# =============================================================================
#         self.get_station()
#         self.write_station()
# =============================================================================
    def thread_set(self):
        self.backend = BackendThread()# 建立執行緒
        print(self.backend)
        self.backend.update_station.connect(self.handle_station)# 連線訊號
        self.backend.start()# 開始執行緒
    def stop_thread(self):
        backend.flag = 1
    def get_station(self):
        self.station = self.line_station.text()
        print('regs:\n',self.station,type(int(self.station)))
    def write_station(self):
        c1.write_single_register(0xD6,int(self.station))
    def read_volt(self):
        self.regs = c1.read_holding_registers(0x6E, 1)
        print('regs:\n',self.regs)
    def display_volt(self):
        volt = str(self.regs)
        print("volt",volt)
        self.lcd_volt.display(volt)
    def handle_station(self, data):# 將當前時間輸出到文字框
        self.station = data
        self.line_station.setText(data)
        print(data)
        self.write_station()