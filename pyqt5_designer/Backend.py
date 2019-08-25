# -*- coding: utf-8 -*-
"""
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
            self.update_station.emit( str(station) )
            if self.flag == 1:
                print('stop',self.flag)
                self.flag = 0
                break
    def stop(self): 
        self.flag = 1
        #print('stop')

class BackendThreadHart(QThread):
    # 處理業務邏輯
    def run(self):
        self.flag_hart = 0
        while True:
            self.c1=ModbusClient()
            self.c1.write_single_register(0xC8,1)
            time.sleep(1)
            self.c1.write_single_register(0xC8,0)
            print("hartbit!")
            if self.flag_hart == 1:
                print('stop!!!hartbit!!',self.flag_hart)
                self.flag_hart = 0
                break
    def stop(self): 
        self.flag_hart = 1
        #print('stop')
            