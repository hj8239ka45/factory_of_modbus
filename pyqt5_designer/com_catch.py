# -*- coding: utf-8 -*-
"""
catch the COM port number

Created on Mon Sep  2 14:39:40 2019
@author: hj823
"""

import serial
def serial_ports():
    p = ['COM%s' % (i + 1) for i in range(256)]
    rlt = []
    for port in p:#測試0~255的COM是否使用，並回傳
        try:
            s = serial.Serial(port)
            s.close()
            rlt.append(port)
        except (OSError, serial.SerialException):
            pass
    return rlt