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
from pyModbusTCP.client import ModbusClient
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from firebase import firebase as fbs
import os
import time

import ReadWriteLib as RWM
import Backend as BK
import RoboticArmLib as RbArm

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
        self.rwm = RWM.ReadWriteMethod(c)
        self.COM = com
        QtWidgets.QMainWindow.__init__(self)
        Ui_SecondWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(path + os.sep + 'MeVb.png'))
        self.lcd_volt.setDigitCount(5)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        
        fileMenu = mainMenu.addMenu('Edit')
        autoButton = QAction('Auto_Mode', self)
        autoButton.setShortcut('Ctrl+A')
        autoButton.setStatusTip('Auto application')
        autoButton.triggered.connect(self.auto_mode)
        fileMenu.addAction(autoButton)        
        
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
        self.rwm.write_hartbit()
        volt = self.rwm.read_volt()
        self.set_volt(volt)
        if self.button_auto.text()=='自動模式':
            self.button_auto.setText('手動模式')
            self.thread_stop()
            self.rwm.write_AGVstop()
        else:
            self.button_auto.setText('自動模式')
            self.thread_set()
# =============================================================================            


# =============================================================================


                    
                    
    def charging(self):
        if self.button_charge.text()=='停止充電':
            self.button_charge.setText('開始充電')
            self.rwm.write_charge(0b01)
        else:
            self.button_charge.setText('停止充電')
            self.rwm.write_charge(0b10)
    def AGV_run(self):
        if self.button_run.text()=='AGV停止':
            self.button_run.setText('AGV啟動')
            self.rwm.write_AGVrun()
        else:
            self.button_run.setText('AGV停止')
            self.rwm.write_AGVstop()
            print('AGV RUN STATUS : *--',self.rwm.read_AGVrun())
# =============================================================================
#     DISPLAY  顯示
# =============================================================================
    def display(self):#讀取line_station寫得值並寫入AGV的PLC
        station = self.rwm.get_station_text()
        if station.isdigit():
            self.rwm.write_station(station)
        else:
            self.agv_act(station)
    def agv_act(self,station):
        station = self.get_station_text()
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
            
    def get_station_text(self):
        station = self.line_station.text()
        return station
    def set_volt(self,volt):
        volt = str(volt)
        print("volt",volt)
        self.lcd_volt.display(volt)
# =============================================================================
#     BACKEND THREAD Firebase       Firebase背景執行緒
# =============================================================================
    '''
        thread_set(): 背景執行緒物件建立
        stop_thread(): 背景執行緒物件關閉
        handle_firebase(): 背景執行緒物件訊號
    '''
    def thread_set(self):
        self.backend_firebase = BK.BackendThreadFirebase()# 建立執行緒
        self.backend_firebase.update_agv_signal.connect(self.handle_agv)# 連線訊號
        self.backend_firebase.update_arm_signal.connect(self.handle_arm)# 連線訊號
        self.backend_firebase.start()# 開始執行緒
    def thread_stop(self):
        self.backend_firebase.stop()
    def handle_agv(self, data):# agv
        print('agv_signal',data,type(data))
        if data=='0':#0b00
            self.toWEDM()
        elif data=='1':#0b01
            self.toHSM()
        elif data=='2':#0b10
            self.toLaser()
        elif data=='3':#0b11
            self.toCMM()

    def handle_arm(self, data):# arm
        print('arm_signal',data)
        #WEDM
        if data=='0':#0b0000
            self.WEDM_Arm_Pinch_AM_I()
        elif data=='1':#0b0001
            self.WEDM_Arm_Move_MA()
        elif data=='2':#0b0010
            self.WEDM_Arm_Move_AM_I()
        elif data=='3':#0b0011
            self.WEDM_Arm_Pinch_MA()
        
        #HSM    
        elif data=='4':#0b0100
            self.HSM_Arm_Pinch_AM_I()
        elif data=='5':#0b0101
            self.HSM_Arm_Move_MA()
        elif data=='6':#0b0110
            self.HSM_Arm_Move_AM_I
        elif data=='7':#0b0111
            self.HSM_Arm_Pinch_MA
            
        #Laser
        elif data=='8':#0b1000
            self.Laser_Arm_Pinch_AM_I()
        elif data=='9':#0b1001
            self.Laser_Arm_Move_MA()
        elif data=='10':#0b1010
            self.Laser_Arm_Move_AM_I()
        elif data=='11':#0b1011
            self.Laser_Arm_Pinch_MA()
        
        #CMM
        elif data=='12':#0b1100
            self.CMM_Arm_Pinch_AM_I()
        elif data=='13':#0b1101
            self.CMM_Arm_Move_MA()
        elif data=='14':#0b1110
            self.CMM_Arm_Move_AM_I()
        elif data=='15':#0b1111
            self.CMM_Arm_Pinch_MA()


        
# =============================================================================
#     Go to Station
# =============================================================================
    '''
        到各站機台
        判別到站後跳出迴圈
    '''
    #agv_signal 0b00
    def toWEDM(self):
        array = {'WEDM':0,'HSM':0,'Laser':0,'CMM':0}
        self.fdb.patch(self.url+"/AGV/",array)#離開站點
        self.rwm.write_station(1)
        self.rwm.write_AGVrun()
        agv_tag = self.rwm.read_tag()
        #print(agv_tag)
        while agv_tag!=[1]:
            #time.sleep(1)
            agv_tag = self.rwm.read_tag()    
            print('agv_tag',agv_tag)
            
            if agv_tag==[1]:
                print('arrive WEDM!')
                self.rwm.write_AGVstop()
                self.fdb.put(self.url+"/AGV/",'WEDM',1) #agv到站
                self.fdb.put(self.url+"/ARM/",'Enable',1) #手臂可動作
    #arm_signal 0b0000
    def WEDM_Arm_Pinch_AM_I(self): #WEDM底下遇到000010111手臂(夾放,AGV->機台,影處)
        self.RtArm.move_to_workpiece_table()
        self.RtArm.grip()
        self.RtArm.move_to_machine1()
        self.RtArm.ungrip()
        
    #arm_signal 0b0001
    def WEDM_Arm_Move_MA(self): #WEDM底下遇到00110011手臂(移動,機台->AGV)
        self.RtArm.back_from_machine1()
        
    #arm_signal 0b0010
    def WEDM_Arm_Move_AM_I(self): #WEDM底下遇到01110011手臂(移動,AGV->機台,影處)
        self.RtArm.move_to_machine1()
        
    #arm_signal 0b0011
    def WEDM_Arm_Pinch_MA(self): #WEDM底下遇到01000011手臂(夾放,機台->AGV)
        self.RtArm.grip()
        self.RtArm.back_from_machine1()
        self.RtArm.move_to_workpiece_table()
        self.RtArm.ungrip()
        self.RtArm.back_from_workpiece_table()    

        
    #agv_signal 0b01
    def toHSM (self):
        array = {'WEDM':0,'HSM':0,'Laser':0,'CMM':0}#離開站點
        self.fdb.patch(self.url+"/AGV/",array)
        self.rwm.write_station(8)
        self.rwm.write_AGVrun()
        agv_tag = self.rwm.read_tag()
        print(agv_tag)
        while agv_tag!=[8]:
            time.sleep(1)
            agv_tag = self.rwm.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[8]:
                print('arrive HSM!')
                self.rwm.write_AGVstop()
                self.fdb.put(self.url+"/AGV/",'HSM',1)#agv到站
                self.fdb.put(self.url+"/ARM/",'Enable',1) #手臂可動作
                
    #arm_signal 0b0100
    def HSM_Arm_Pinch_AM_I(self): #HSM底下遇到000010111手臂(夾放,AGV->機台,影處)
        self.RtArm.move_to_workpiece_table()
        self.RtArm.grip()
        self.RtArm.move_to_machine2()
        self.RtArm.ungrip()
        
    #arm_signal 0b0101
    def HSM_Arm_Move_MA(self): #HSM底下遇到00110011手臂(移動,機台->AGV)
        self.RtArm.back_from_machine2()
        
    #arm_signal 0b0110
    def HSM_Arm_Move_AM_I(self): #HSM底下遇到01110011手臂(移動,AGV->機台,影處)
        self.RtArm.move_to_machine2()
        
    #arm_signal 0b0111
    def HSM_Arm_Pinch_MA(self): #HSM底下遇到01000011手臂(夾放,機台->AGV)
        self.RtArm.grip()
        self.RtArm.back_from_machine2()
        self.RtArm.move_to_workpiece_table()
        self.RtArm.ungrip()
        self.RtArm.back_from_workpiece_table()            
                   
            
    #agv_signal 0b10
    def toLaser(self):
        array = {'WEDM':0,'HSM':0,'Laser':0,'CMM':0}#離開站點
        self.fdb.patch(self.url+"/AGV/",array)
        self.rwm.write_station(13)
        self.rwm.write_AGVrun()
        agv_tag = self.rwm.read_tag()
        print(agv_tag)
        while agv_tag!=[13]:
            time.sleep(1)
            agv_tag = self.rwm.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[13]:
                print('arrive Laser!')
                self.rwm.write_AGVstop()   
                self.fdb.put(self.url+"/AGV/",'Laser',1)#車子到站
                self.fdb.put(self.url+"/ARM/",'Enable',1) #手臂可動作
                
    #arm_signal 0b1000
    def Laser_Arm_Pinch_AM_I(self): #Laser底下遇到000010111手臂(夾放,AGV->機台,影處)
        self.RtArm.move_to_workpiece_table()
        self.RtArm.grip()
        self.RtArm.move_to_machine3()
        self.RtArm.ungrip()
        
    #arm_signal 0b1001
    def Laser_Arm_Move_MA(self): #Laser底下遇到00110011手臂(移動,機台->AGV)
        self.RtArm.back_from_machine3()
        
    #arm_signal 0b1010
    def Laser_Arm_Move_AM_I(self): #Laser底下遇到01110011手臂(移動,AGV->機台,影處)
        self.RtArm.move_to_machine3()
        
    #arm_signal 0b1011
    def Laser_Arm_Pinch_MA(self): #Laser底下遇到01000011手臂(夾放,機台->AGV)
        self.RtArm.grip()
        self.RtArm.back_from_machine3()
        self.RtArm.move_to_workpiece_table()
        self.RtArm.ungrip()
        self.RtArm.back_from_workpiece_table()  


    #agv_signal 0b11
    def toCMM(self):
        array = {'WEDM':0,'HSM':0,'Laser':0,'CMM':0}#離開站點
        self.fdb.patch(self.url+"/AGV/",array)
        self.rwm.write_station(12)
        self.rwm.write_AGVrun()
        agv_tag = self.rwm.read_tag()
        print(agv_tag)
        while agv_tag!=[12]:
            time.sleep(1)
            agv_tag = self.rwm.read_tag()    
            print('agv_tag',agv_tag)
            if agv_tag==[12]:
                print('arrive CMM!')
                self.rwm.write_AGVstop()
                self.fdb.put(self.url+"/AGV/",'CMM',1) #agv到站
                self.fdb.put(self.url+"/ARM/",'Enable',1) #手臂可動作
                
    #arm_signal 0b1100
    def CMM_Arm_Pinch_AM_I(self): #CMM底下遇到000010111手臂(夾放,AGV->機台,影處)
        self.RtArm.move_to_workpiece_table()
        self.RtArm.grip()
        self.RtArm.move_to_machine2()
        self.RtArm.ungrip()
        
    #arm_signal 0b1101
    def CMM_Arm_Move_MA(self): #CMM底下遇到00110011手臂(移動,機台->AGV)
        self.RtArm.back_from_machine2()
        
    #arm_signal 0b1110
    def CMM_Arm_Move_AM_I(self): #CMM底下遇到01110011手臂(移動,AGV->機台,影處)
        self.RtArm.move_to_machine2()
        
    #arm_signal 0b1111
    def CMM_Arm_Pinch_MA(self): #CMM底下遇到01000011手臂(夾放,機台->AGV)
        self.RtArm.grip()
        self.RtArm.back_from_machine2()
        self.RtArm.move_to_workpiece_table()
        self.RtArm.ungrip()
        self.RtArm.back_from_workpiece_table()  
    """        
    def ArmCMM(self):
        #            #沒門        
        self.fdb.put(self.url+"/CMM/",'Arm',0) #手臂下去，準備夾工件
    """ 
    '''    
    def AutoRound(self):
        while(1):
            AGV = self.fdb.get('/AGV',None)
            ARM = self.fdb.get('/ARM',None)
            MES = self.fdb.get('/MES',None)
            if AGV['WEDM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                WEDM = self.fdb.get('/WEDM',None)               
                if list(WEDM.values())==[0,0,0,0,0]:
                    self.fdb.put(self.url+"/ARM/",'Moving',1)
                    self.WEDM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                    self.fdb.put(self.url+"/ARM/",'Moving',0)
                    self.fdb.put(self.url+"/WEDM/",'ChuckEnable',1)
                elif list(WEDM.values())==[1,1,0,0,0]:
                    self.fdb.put(self.url+"/ARM/",'Moving',1)
                    self.WEDM_Arm_Move_MA() #手臂(移動,機台->AGV)
                    self.fdb.put(self.url+"/ARM/",'Moving',0)
                    self.fdb.put(self.url+"/ARM/",'Enable',0)
                elif list(WEDM.values())==[1,1,1,0,0]:
                    self.fdb.put(self.url+"/ARM/",'Moving',1)
                    self.WEDM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                    self.fdb.put(self.url+"/ARM/",'Moving',0)
                    self.fdb.put(self.url+"/WEDM/",'ChuckEnable',0)
                elif list(WEDM.values())==[0,0,1,0,0]:
                    self.fdb.put(self.url+"/WEDM/",'Done',0)
                    self.fdb.put(self.url+"/ARM/",'Moving',1)
                    self.WEDM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
                    self.fdb.put(self.url+"/ARM/",'Moving',0)
                    self.fdb.put(self.url+"/ARM/",'Enable',0)
            if AGV['HSM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                HSM = self.fdb.get('/HSM',None)               
                if list(HSM.values())==[0,0,0,0,0]:
                    self.HSM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                elif list(HSM.values())==[1,1,0,0,0]:
                    self.HSM_Arm_Move_MA() #手臂(移動,機台->AGV)
                elif list(HSM.values())==[1,1,1,0,0]:
                    self.HSM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                elif list(HSM.values())==[1,1,1,0,0]:
                    self.HSM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
            if AGV['Laser']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                Laser = self.fdb.get('/Laser',None)               
                if list(Laser.values())==[0,0,0,0,0]:
                    self.Laser_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                elif list(Laser.values())==[1,1,0,0,0]:
                    self.Laser_Arm_Move_MA() #手臂(移動,機台->AGV)
                elif list(Laser.values())==[1,1,1,0,0]:
                    self.Laser_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                elif list(Laser.values())==[1,1,1,0,0]:
                    self.Laser_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
            if AGV['CMM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                CMM = self.fdb.get('/CMM',None)               
                if list(CMM.values())==[0,0,0,0,0]:
                    self.CMM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                elif list(CMM.values())==[1,1,0,0,0]:
                    self.CMM_Arm_Move_MA() #手臂(移動,機台->AGV)
                elif list(CMM.values())==[1,1,1,0,0]:
                    self.CMM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                elif list(CMM.values())==[1,1,1,0,0]:
                    self.CMM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
            if list(AGV.values())!=[0,0,0,0] and list(ARM.values())==[0,0] and MES!=0:#AGV在WEDM並且手臂符合動作
                if MES==1:
                    self.toWEDM()
                elif MES==2:
                    self.toHSM()
                elif MES==3:
                    self.toLaser()
                elif MES==4:
                    self.toCMM()
       '''             
                
                
        
    
        
        
        
        
        