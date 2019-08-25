# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:24:40 2019

@author: hj823
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLCDNumber , QHeaderView
import os
from pyModbusTCP.client import ModbusClient
from Backend import BackendThreadFirebase , BackendThreadHart
import RoboticArmLib as RbArm
import time

path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile_second = path + os.sep + "ui" + os.sep + "Second_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_SecondWindow, QtBaseClass_second = uic.loadUiType(qtCreatorFile_second)
class SecondUi(QtWidgets.QMainWindow, Ui_SecondWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self,c=ModbusClient()):
        self.c1 = c
        QtWidgets.QMainWindow.__init__(self)
        Ui_SecondWindow.__init__(self)
        self.setupUi(self)
        self.lcd_volt.setDigitCount(5)
        self.lcd_volt.setMode(QLCDNumber.Dec)
        self.lcd_volt.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.initUI()
    def closeEvent(self, event):#關閉執行
        if self.button_auto.text()=='自動模式':
            self.stop_hart()
        print("closed!!")
    def initUI(self):
        self.button_auto.clicked.connect(self.auto_mode)
        self.button_push.clicked.connect(self.display)
        self.button_charge.clicked.connect(self.charging)
        self.button_run.clicked.connect(self.AGV_run)
        #self.robot_set()
    def tableUI(self):
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch)
# =============================================================================
#     Robotic Arm   
# =============================================================================
    def robot_set(self):
        self.RobotArm = RbArm.RoboticArm()
# =============================================================================
#     Firebase Data  
# =============================================================================
    def FirebaseData(self):
        self.MyData = {
            Chuck_Robot: 1,
            Chuck_Workpiece: 1,
            Arm: 2,
            Running: 1,
            Error: 0
            }
        self.MyData_door = {
            Chuck_Robot: 1,
            Chuck_Workpiece: 1,
            Arm: 2,
            Running: 1,
            Door: 1,
            Error: 0
            }
        
        #db.ref("/chinese/Bob").update(myGrade)
# =============================================================================
#     MODE  模式
# =============================================================================
    def auto_mode(self):#used for 9/1
        volt = self.read_volt()
        self.write_volt(volt)
        if self.button_auto.text()=='自動模式':
            self.button_auto.setText('手動模式')
            self.stop_thread()
            self.write_AGVrun(0b10)
            self.c1.write_single_register(0xC8,1)
            self.c1.write_single_register(0xC8,0)
        else:
            self.button_auto.setText('自動模式')
            self.thread_set()
            self.write_AGVrun(0b01)
            self.c1.write_single_register(0xC8,1)
            self.c1.write_single_register(0xC8,0)
            self.toWEDM()
            self.write_AGVrun(0b00)
            self.write_AGVrun(0b01) 
            agv_tag = self.read_tag()
            print(agv_tag)
            while agv_tag!=[1]:
                time.sleep(0.5)
                agv_tag = self.read_tag()    
                print('agv_tag',agv_tag)
                if agv_tag==[1]:
                    print('arrive WEDM!')
            self.write_AGVrun(0b00)
            self.write_AGVrun(0b10)
#            手臂&firebase
# =============================================================================
#             self.toLaser()
#             agv_tag = self.read_tag()
#             print("agv_tag",agv_tag)
#             if agv_tag!=[13]:
#                 self.write_AGVrun(0b00)
#                 self.write_AGVrun(0b01)
#             while agv_tag!=[13]:
#                 time.sleep(0.8)
#                 agv_tag = self.read_tag()
#                 print("agv_tag",agv_tag)
#                 if agv_tag==[13]:
#                     print('arrive Laser!')
#             self.write_AGVrun(0b00)
#             self.write_AGVrun(0b10)
# #           手臂&firebase
# =============================================================================
# =============================================================================
#             self.toEDM()
#             agv_tag = self.read_tag()
#             print("agv_tag",agv_tag)
#             if agv_tag!=[8]:
#                 self.write_AGVrun(0b00)
#                 self.write_AGVrun(0b01)
#             while agv_tag!=[8]:
#                 time.sleep(0.5)
#                 agv_tag = self.read_tag()
#                 if agv_tag==[8]:
#                     print('arrive EDM!')
#                     self.write_AGVrun(0b00)
#                     self.write_AGVrun(0b10)
#             ##手臂&firebase
# =============================================================================
# =============================================================================
#             self.toCMM()
#             agv_tag = self.read_tag()
#             print("agv_tag",agv_tag)
#             if agv_tag!=[12]:
#                 self.write_AGVrun(0b00)
#                 self.write_AGVrun(0b01)
#             while agv_tag!=[12]:
#                 time.sleep(0.5)                
#                 agv_tag = self.read_tag()
#                 if agv_tag==[12]:
#                     print('arrive CMM!')
#                     self.write_AGVrun(0b00)
#                     self.write_AGVrun(0b10)
# =============================================================================


            ##手臂&firebase
                    
                    
# =============================================================================
#     def auto_mode(self):
#         if self.button_auto.text()=='自動模式':
#             self.button_auto.setText('手動模式')
#             self.stop_thread()
#         else:
#             self.button_auto.setText('自動模式')
#             self.thread_set()
# =============================================================================
    def charging(self):
        if self.button_charge.text()=='停止充電':
            self.button_charge.setText('開始充電')
            self.write_charge(0b01)
        else:
            self.button_charge.setText('停止充電')
            self.write_charge(0b10)
    def AGV_run(self):
        if self.button_run.text()=='AGV停止':
            self.button_run.setText('AGV啟動')
            self.write_AGVrun(0b00)
            self.write_AGVrun(0b01)
            self.read_AGVrun()
            self.c1.write_single_register(0xC8,1)
            self.c1.write_single_register(0xC8,0)
        else:
            self.button_run.setText('AGV停止')
            self.write_AGVrun(0b00)
            self.write_AGVrun(0b10)
            self.read_AGVrun()
            self.c1.write_single_register(0xC8,1)
            self.c1.write_single_register(0xC8,0)
# =============================================================================
#     DISPLAY  顯示
# =============================================================================
    def display(self):
        station = self.read_station()
        self.write_station(station)
# =============================================================================
#     WRITE&READ  寫入讀取  
# =============================================================================
    def read_station(self):
        station = self.line_station.text()
        return station
    def write_station(self,station):
        self.station = station
        self.c1.write_single_register(0xD6,int(self.station))
    def read_tag(self):
        tag = self.c1.read_holding_registers(0x74, 1)
        return tag
    def read_volt(self):
        volt = self.c1.read_holding_registers(0x6E, 1)
        return volt
        #print('regs:\n',self.regs)
    def write_volt(self,volt):
        volt = str(volt)
        print("volt",volt)
        self.lcd_volt.display(volt)
    def write_charge(self,data):
        self.c1.write_single_register(0xD1,data)
    def write_AGVrun(self,data):
        self.c1.write_single_register(0xD7,data)
        print('!\n')
    def read_AGVrun(self):
        reg = self.c1.read_holding_registers(0xC8, 30)
        print('regs:\n',reg)
# =============================================================================
#     BACKEND THREAD Firebase       Firebase背景執行緒
# =============================================================================
    def thread_set(self):
        #self.backend_firebase = BackendThreadFirebase()# 建立執行緒
        self.hart_set()
        #self.backend_firebase.update_station.connect(self.handle_firebase)# 連線訊號
        #self.backend_firebase.start()# 開始執行緒
    def stop_thread(self):
        #self.backend_firebase.stop()
        self.backend_hart.stop()
    def handle_firebase(self, data):# 將當前訊息輸出到文字框
        self.station = data
        self.line_station.setText(data)
#        data_err = c1.read_holding_registers(0xDC,75)
#        print('err:',data_err)
        print(data)
        self.write_station()
# =============================================================================
#     BACKEND THREAD Hart bit       Hart bit背景執行緒
# =============================================================================        
    def hart_set(self):
        self.backend_hart = BackendThreadHart()# 建立執行緒
        self.backend_hart.start()# 開始執行緒
    def stop_hart(self):
        self.backend_hart.stop()
        
        
# =============================================================================
#     Go to Station
# =============================================================================
    def toWEDM(self):
        self.write_station(1)
    def toEDM (self):
        self.write_station(8)
    def toLaser(self):    
        self.write_station(13)
    def toCMM(self):
        self.write_station(12)
        
        
        
        
        
        
        
        