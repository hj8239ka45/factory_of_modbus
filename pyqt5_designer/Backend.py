# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:24:40 2019

@author: hj823
"""
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime
import time
from requests import get

firebase_url="https://smartmanu-af015.firebaseio.com/.json"
class BackendThread(QThread):
    # 通過類成員物件定義訊號
    update_station = pyqtSignal(str)
    # 處理業務邏輯
    def run(self):
        flag = 0
        while True:
            station = get(firebase_url).json()['AgvStation']
            self.update_station.emit( str(station) )
            time.sleep(0.1)
            if flag == 1:
                print('flag',flag)
                break

            