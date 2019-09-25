# -*- coding: utf-8 -*-
"""
背景執行緒建立參考: https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/433908/
Created on Wed Jul 31 21:24:40 2019
@author: hj823
"""
from PyQt5.QtCore import QThread ,  pyqtSignal
from requests import get
from pyModbusTCP.client import ModbusClient
import time 
firebase_url="https://smartmanu-af015.firebaseio.com/.json"
class BackendThreadFirebase(QThread):
    # 通過類成員物件定義訊號
    update_station = pyqtSignal(str)
    # 處理業務邏輯
    def run(self):
        self.flag = 0
        while True:
            station = get(firebase_url).json()['AgvStation']
            self.update_station.emit( str(station) )#發送訊號流訊號
            if self.flag == 1:
                print('stop',self.flag)
                self.flag = 0
                break
    def stop(self): 
        self.flag = 1

        
class BackendThread_HartBit(QThread):
    def __init__(self,c=ModbusClient()):
        QThread.__init__(self)
        self.c1 = c
    def run(self):
        self.flag = 0
        while True:
            time.sleep(1)
            self.c1.write_single_register(0xC8,1)
            time.sleep(1)
            self.c1.write_single_register(0xC8,0)
        
            if self.flag == 1:
                print('stop',self.flag)
                self.flag = 0
                break
    def stop(self): 
        self.flag = 1  

class BackendThread_Auto(QThread):
    # 通過類成員物件定義訊號
    update_arrive = pyqtSignal(str)
    # 處理業務邏輯
    def __init__(self,c=ModbusClient(),station=0):
        QThread.__init__(self)
        self.station = station
        self.c1 = c
    def run(self):
        self.flag = 0
        agv_tag = self.read_tag()
        while agv_tag!=self.station:
            time.sleep(1)
            agv_tag = self.read_tag()    
            print('agv_tag',agv_tag)
            print('station',self.station)
            if agv_tag==self.station:
                print('arrive !!!')
                self.update_arrive.emit( str(self.station) )#發送訊號流訊號
            if self.flag == 1:
                print('stop',self.flag)
                self.flag = 0
                break
    def read_tag(self):
        tag = self.c1.read_holding_registers(0x74, 1)
        return tag
    def stop(self): 
        self.flag = 1
        