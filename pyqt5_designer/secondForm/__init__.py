# -*- coding: utf-8 -*-
"""
第二個介面建立
手臂COM連線建立
AGV_PLC的modbus資料傳輸以及功能設計
AGV 各站程式建立
Created on Wed Jul 31 21:24:40 2019
@author: hj823
"""

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QLCDNumber , QTableWidgetItem
import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from pyModbusTCP.client import ModbusClient
from Backend import BackendThread_HartBit,BackendThread_Auto
import RoboticArmLib as RbArm
from firebase import firebase as fbs
import time

'''
    由 main.py 引入此 __init__.py檔案: 使用的 path 路徑也在 main.py 底下
    os.sep 為 python的'\'引入
    由 uic 進行 UI(XML格式) 與 python 之間的引入轉換
'''
path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile_second = path + os.sep + "ui" + os.sep + "Second_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_SecondWindow, QtBaseClass_second = uic.loadUiType(qtCreatorFile_second)
class SecondUi(QtWidgets.QMainWindow, Ui_SecondWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self,c=ModbusClient(),com = ""):
        self.c1 = c
        self.COM = com
        QtWidgets.QMainWindow.__init__(self)
        Ui_SecondWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(path + os.sep + 'MeVb.png'))
        self.lcd_volt.setDigitCount(5)
        
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip('Exit application')
        self.exitButton.triggered.connect(self.close)
        
        self.autoButton.setShortcut('Ctrl+A')
        self.autoButton.setStatusTip('Auto application')
        self.autoButton.triggered.connect(self.auto_mode)
        
        self.lcd_volt.setMode(QLCDNumber.Dec)
        self.lcd_volt.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.initUI()
    def closeEvent(self, event):#關閉執行，關閉機械手臂物件的serial連線
        self.RtArm.close()
        self.thread_stop()
        print("closed!!")
    def initUI(self):#初始按鈕連接的函式建立連線，以及各個功能初始物件建立
        self.button_auto.clicked.connect(self.auto_mode)
        self.button_push.clicked.connect(self.display)
        self.button_charge.clicked.connect(self.charging)
        self.button_run.clicked.connect(self.AGV_run)
        self.tableUI()
        self.Firebase_set()
        self.robot_set()
        
# =============================================================================
#     UTable
# =============================================================================
    def tableUI(self):#UI的資料表的初始物件設定
        self.table_firebase.resizeColumnsToContents()   #将列调整到跟内容大小相匹配
        self.table_firebase.resizeRowsToContents()      #将行大小调整到跟内容的大小相匹配
        data = []
        data.append((self.line_station.text(), 'QtableWidget'))
        data.append(('With data', 'In Python'))
        data.append(('Is easy', 'Job'))
        row=0
        for tup in data:
            col=0
            for item in tup:
                cellinfo=QTableWidgetItem(item)
                self.table_firebase.setItem(row, col, cellinfo)
                col+=1
            row += 1
# =============================================================================
#     Robotic Arm   
# =============================================================================
    def robot_set(self):#手臂初始物件設定
        self.RtArm = RbArm.RoboticArm(self.COM)
        self.RtArm.speed( spd=200, acl=400)
# =============================================================================
#     Firebase Data  
# =============================================================================
    def Firebase_set(self): #Firebase的初始物件設定
        self.url = "https://smartmanu-af015.firebaseio.com"
        self.fdb = fbs.FirebaseApplication(self.url, None)
# =============================================================================
#     MODE  模式
# =============================================================================
    def auto_mode(self):#used for 9/1
        volt = self.read_volt()
        self.write_volt(volt)
        if self.button_auto.text()=='自動模式':
            self.button_auto.setText('手動模式')
            self.write_AGVstop()
            self.thread_stop()           
        else:
            self.button_auto.setText('自動模式')
            self.thread_set()
            self.write_AGVrun()   
# =============================================================================            
#            self.toWEDM()
#            #手臂&firebase
#            self.ArmWEDM()
# =============================================================================
#            self.toHSM()
#            ##手臂&firebase
#            self.ArmHSM()
# =============================================================================
#            self.toLaser()
#            ##手臂&firebase
#            self.ArmLaser()
# =============================================================================
#            self.toCMM()
#            ##手臂&firebase
#            self.ArmCMM()
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
            self.write_AGVrun()
        else:
            self.button_run.setText('AGV停止')
            self.write_AGVstop()
            print('AGV RUN STATUS : *--',self.read_AGVrun())
# =============================================================================
#     DISPLAY  顯示
# =============================================================================
    def display(self):#讀取line_station寫得值並寫入AGV的PLC
        station = self.read_station()
        if station.isdigit():
            self.write_station(station)
        else:
            self.write_Act(station)
# =============================================================================
#     WRITE&READ  寫入讀取  
# =============================================================================
    def write_Act(self,station):
        station = self.read_station()
        if station == "WEDM":
            self.toWEDM()
            self.ArmWEDM()
        elif station == "HSM":
            self.toHSM()
            self.ArmHSM()
        elif station == "Laser":
            self.toLaser()
            self.ArmLaser()
        elif station == "CMM":
            self.toCMM()
            self.ArmCMM()
        else:
            print("error")
        
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
    def write_hartbit(self):
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
#     BACKEND THREAD Firebase       Firebase背景執行緒
# =============================================================================
    '''
        thread_set(): 背景執行緒物件建立
        stop_thread(): 背景執行緒物件關閉
        handle_firebase(): 背景執行緒物件訊號
    '''
    def thread_set(self):
        station = self.c1.read_holding_registers(0x72,1)
        #self.backend_hartbit = BackendThread_HartBit(self.c1)
        #self.backend_hartbit.start()# 開始執行緒
        self.backend_auto = BackendThread_Auto(self.c1,station)
        self.backend_auto.start()# 開始執行緒        
        self.backend_auto.update_arrive.connect(self.handle_arrive)# 連線訊號
    def handle_arrive(self,data):
        print('data',data)
        if data == str([1]):
            print('WEDM')
            #self.ArmWEDM()
        elif data == str([8]):
            print('HSM')
            #self.ArmHSM()
        elif data == str([13]):
            print('Laser')
            #self.ArmLaser()
        elif data == str([12]):
            print('CMM')
            #self.ArmCMM()
    def thread_stop(self):
        #self.backend_hartbit.stop()
        self.backend_auto.stop()
# =============================================================================
#         self.backend_firebase = BackendThreadFirebase()# 建立執行緒
#         self.backend_firebase.update_station.connect(self.handle_firebase)# 連線訊號
#         self.backend_firebase.start()# 開始執行緒
# =============================================================================
# =============================================================================
#     def handle_firebase(self, data):# 將當前訊息輸出到文字框
#         self.station = data
#         self.line_station.setText(data)
# #        data_err = c1.read_holding_registers(0xDC,75)
# #        print('err:',data_err)
#         print(data)
#         self.write_station()
# =============================================================================

        
        
# =============================================================================
#     Go to Station
# =============================================================================
    '''
        到各站機台
        判別到站後跳出迴圈
    '''
    def toWEDM(self):
        self.write_station(1)
        self.write_AGVrun()
        agv_tag = self.read_tag()
        print(agv_tag)
        while agv_tag!=[1]:
            time.sleep(1)
            agv_tag = self.read_tag()
            print('agv_tag',agv_tag)
            
            if agv_tag==[1]:
                print('arrive WEDM!')
                self.write_AGVstop()
    def ArmWEDM(self):
#            #沒門
        self.fdb.put(self.url+"/AGV/",'WEDM',1) #agv到站
        self.fdb.put(self.url+"/WEDM/",'Arm',0) #手臂下去，準備夾工件
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/WEDM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/WEDM/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine1()
        self.fdb.put(self.url+"/WEDM/",'Arm',1)#手臂停止(到夾置具上方)
        time.sleep(2)
        WEDM = self.fdb.get('/WEDM',None)
        while WEDM['Chuck_W']!=0:#工具機夾爪夾持
            time.sleep(0.5)
            WEDM = self.fdb.get('/WEDM',None)
            print(WEDM['Chuck_W'])
            print("wait for Chuck_workpiece")
        self.fdb.put(self.url+"/WEDM/",'Chuck_R',1)#手臂放
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂移開
        self.RtArm.back_from_machine1()
        self.fdb.put(self.url+"/WEDM/",'Arm',2)#手臂停(移回AGV)
        time.sleep(2)
        WEDM = self.fdb.get('/WEDM',None)
        while WEDM['Running']!=1:#工具機夾爪夾持
            time.sleep(0.5)
            WEDM = self.fdb.get('/WEDM',None)
            print("wait for Machine Stoped")
        time.sleep(2)
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine1()
        self.fdb.put(self.url+"/WEDM/",'Arm',1)#手臂停止(到夾置具上方)
        self.fdb.put(self.url+"/WEDM/",'Chuck_R',0)#手臂夾爪夾持
        self.RtArm.grip()
        time.sleep(2)
        WEDM = self.fdb.get('/WEDM',None)
        while WEDM['Chuck_W']!=1:#工具夾爪放
            time.sleep(0.5)
            WEDM = self.fdb.get('/WEDM',None)
            print("wait for Chuck_workpiece")
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂動(移回AGV)
        self.RtArm.back_from_machine1()
        self.fdb.put(self.url+"/WEDM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂下去
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/WEDM/",'Arm',2)#手臂放下工件
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/WEDM/",'Arm',0)#手臂上去
        self.fdb.put(self.url+"/WEDM/",'Arm',2)#手臂回到原位
        self.RtArm.back_from_workpiece_table()
        self.fdb.put(self.url+"/AGV/",'WEDM',0)#AGV 走
        
        
    def toHSM (self):
        self.write_station(8)
        self.write_AGVrun()
        agv_tag = self.read_tag()
        print(agv_tag)
        while agv_tag!=[8]:
            time.sleep(1)
            agv_tag = self.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[8]:
                print('arrive HSM!')
                self.write_AGVstop()
                
                
    def ArmHSM(self):
        #            #有門
        self.fdb.put(self.url+"/AGV/",'HSM',1)#agv到站
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂下去(準備夾工件)
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/HSM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/HSM/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine3()
        self.fdb.put(self.url+"/HSM/",'Arm',1)#手臂停止(到夾置具上方)
        time.sleep(2)
        HSM = self.fdb.get('/HSM',None)
        while HSM['Chuck_W']!=0: #工具機夾爪夾持
            time.sleep(0.5)
            HSM = self.fdb.get('/HSM',None)
            print("wait for CHUCK WORKPIECE")
        self.fdb.put(self.url+"/HSM/",'Chuck_R',1)#手臂放(順序改一下)
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂移開
        self.RtArm.back_from_machine3()
        self.fdb.put(self.url+"/HSM/",'Arm',2)#手臂停(移回AGV)
        time.sleep(2)
        HSM = self.fdb.get('/HSM/',None)
        while HSM['Door']!=1:#門關後Delay20秒
            time.sleep(0.5)
            HSM = self.fdb.get('/HSM',None)
            print("wait for DOOR OPENED")
        time.sleep(2)
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine3()
        self.fdb.put(self.url+"/HSM/",'Arm',1)#手臂停止(到夾置具上方)
        self.fdb.put(self.url+"/HSM/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        time.sleep(2)
        HSM = self.fdb.get('/HSM/',None)
        while HSM['Chuck_W']!=1:#工具放
            HSM = self.fdb.get('/HSM',None)
            time.sleep(0.5)
            print("wait for CHUCK WORKPIECE")
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂動(移回AGV)
        self.RtArm.back_from_machine3()
        self.fdb.put(self.url+"/HSM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂下去
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/HSM/",'Arm',2)
        self.fdb.put(self.url+"/HSM/",'Chuck_R',1)#手臂放下工件
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/HSM/",'Arm',0)#手臂上去
        self.fdb.put(self.url+"/HSM/",'Arm',2)#手臂回到原位
        self.RtArm.back_from_workpiece_table()
        self.fdb.put(self.url+"/AGV/",'HSM',0)#AGV 走

            
    def toLaser(self):
        self.write_station(13)
        self.write_AGVrun()
        agv_tag = self.read_tag()
        print(agv_tag)
        while agv_tag!=[13]:
            time.sleep(1)
            agv_tag = self.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[13]:
                print('arrive Laser!')
                self.write_AGVstop()        
                
    def ArmLaser(self):
        #            #有門
        self.fdb.put(self.url+"/AGV/",'Laser',1)#車子到站
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂下去(準備夾工件)
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/Laser/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/Laser/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine3()
        self.fdb.put(self.url+"/Laser/",'Arm',1)#手臂停止(到夾置具上方)
        time.sleep(2)
        Laser = self.fdb.get('/Laser',None)
        while Laser['Chuck_W']!=0: #工具機夾爪夾持
            time.sleep(0.5)
            Laser = self.fdb.get('/Laser',None)
            print("wait for CHUCK WORKPIECE")
        self.fdb.put(self.url+"/Laser/",'Chuck_R',1)#手臂放(順序改一下)
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂移開
        self.RtArm.back_from_machine3()
        self.fdb.put(self.url+"/Laser/",'Arm',2)#手臂停(移回AGV)
        time.sleep(2)
        Laser = self.fdb.get('/Laser',None)
        while Laser['Door']!=1:#門關後Delay20秒
            time.sleep(0.5)
            Laser = self.fdb.get('/Laser',None)
            print("wait for DOOR OPENED")
        time.sleep(2)
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine3()
        self.fdb.put(self.url+"/Laser/",'Arm',1)#手臂停止(到夾置具上方)
        self.fdb.put(self.url+"/Laser/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        time.sleep(2)
        Laser = self.fdb.get('/Laser',None)
        while Laser['Chuck_W']!=1:#工具放
            time.sleep(0.5)
            Laser = self.fdb.get('/Laser',None)
            print("wait for CHUCK WORKPIECE")
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂動(移回AGV)
        self.RtArm.back_from_machine3()
        self.fdb.put(self.url+"/Laser/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂下去
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/Laser/",'Arm',2)
        self.fdb.put(self.url+"/Laser/",'Chuck_R',1)#手臂放下工件
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/Laser/",'Arm',0)#手臂上去
        self.fdb.put(self.url+"/Laser/",'Arm',2)#手臂回到原位
        self.RtArm.back_from_workpiece_table()
        self.fdb.put(self.url+"/AGV/",'Laser',0)#AGV 走

    def toCMM(self):
        self.write_station(12)
        self.write_AGVrun()
        agv_tag = self.read_tag()
        print(agv_tag)
        while agv_tag!=[12]:
            time.sleep(1)
            agv_tag = self.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[12]:
                print('arrive CMM!')
                self.write_AGVstop()
        
    def ArmCMM(self):
        #            #沒門
        self.fdb.put(self.url+"/AGV/",'CMM',1) #agv到站
        self.fdb.put(self.url+"/CMM/",'Arm',0) #手臂下去，準備夾工件
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/CMM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/CMM/",'Chuck_R',0)#手臂夾
        self.RtArm.grip()
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine4()
        self.fdb.put(self.url+"/CMM/",'Arm',1)#手臂停止(到夾置具上方)
        time.sleep(2)
        CMM = self.fdb.get('/CMM',None)
        while CMM['Chuck_W']!=0:#工具機夾爪夾持
            time.sleep(0.5)
            CMM = self.fdb.get('/CMM',None)
            print("wait for Chuck_workpiece")
        self.fdb.put(self.url+"/CMM/",'Chuck_R',1)#手臂放
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂移開
        self.RtArm.back_from_machine4()
        self.fdb.put(self.url+"/CMM/",'Arm',2)#手臂停(移回AGV)
        time.sleep(2)
        CMM = self.fdb.get('/CMM',None)
        while CMM['Running']==1:#工具機夾爪夾持
            time.sleep(0.5)
            CMM = self.fdb.get('/CMM',None)
            print("wait for Running")
        time.sleep(2)
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂動(送進機臺)
        self.RtArm.move_to_machine4()
        self.fdb.put(self.url+"/CMM/",'Arm',1)#手臂停止(到夾置具上方)
        self.fdb.put(self.url+"/CMM/",'Chuck_R',0)#手臂夾爪夾持
        self.RtArm.grip()
        time.sleep(2)
        CMM = self.fdb.get('/CMM',None)
        while CMM['Chuck_W']!=1:#工具夾爪放
            time.sleep(0.5)
            CMM = self.fdb.get('/CMM',None)
            print("wait for Chuck_workpiece")
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂動(移回AGV)
        self.RtArm.back_from_machine4()
        self.fdb.put(self.url+"/CMM/",'Arm',2)#手臂停
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂下去
        self.RtArm.move_to_workpiece_table()
        self.fdb.put(self.url+"/CMM/",'Arm',2)#手臂放下工件
        self.RtArm.ungrip()
        self.fdb.put(self.url+"/CMM/",'Arm',0)#手臂上去
        self.fdb.put(self.url+"/CMM/",'Arm',2)#手臂回到原位
        self.RtArm.back_from_workpiece_table()
        self.fdb.put(self.url+"/AGV/",'CMM',0)#AGV 走
        
        
        
        