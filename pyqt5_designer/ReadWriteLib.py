# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:57:30 2019
# =============================================================================
#     WRITE&READ  寫入讀取  
# =============================================================================
@author: hj823
"""
from pyModbusTCP.client import ModbusClient
import time
'''
    __init__  : initial setting
    write_XXX : use to write the data of XXX to PLC
    read_XXX  : use to read the data of XXX in PLC
'''
class ReadWriteMethod:
    def __init__(self,c = ModbusClient()):
        self.c1 = c
    def write_station(self,station):
        #self.write_hartbit()
        self.station = station
        self.c1.write_single_register(0xD6,int(self.station))
    def read_tag(self):
        tag = self.c1.read_holding_registers(0x74, 1)
        return tag
    def read_volt(self):
        volt = self.c1.read_holding_registers(0x6E, 1)
        return volt
    def write_charge(self,data):
        self.c1.write_single_register(0xD1,data)
    def write_hartbit(self):
        print("hartbit")
        time.sleep(1)
        self.c1.write_single_register(0xC8,1)
        time.sleep(1)
        self.c1.write_single_register(0xC8,0)
        time.sleep(1)
    def write_AGVrun(self):
        self.write_hartbit()
        self.c1.write_single_register(0xD7,0b01)
        self.write_hartbit()
        print("Run!!!!!!!!!!!!")
    def write_AGVstop(self):
        self.write_hartbit()
        self.c1.write_single_register(0xC8,0b10)
        self.write_hartbit()
        print("Stop!!!!!!!!!!!!")
    def read_AGVrun(self):
        reg = self.c1.read_holding_registers(0xC8, 21)
        return reg

# =============================================================================
# # # # # # # Example # # # # # # 
# import ReadWriteLib as rwl
# from pyModbusTCP.client import ModbusClient
# import time
# rwm = rwl.ReadWriteMethod(c = ModbusClient())
# rwm.write_station()
# print('tag',rwm.read_tag())
# =============================================================================

