# -*- coding: utf-8 -*-
"""
背景執行緒建立參考: https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/433908/
Created on Wed Jul 31 21:24:40 2019
@author: hj823
"""
from PyQt5.QtCore import QThread ,  pyqtSignal

from firebase import firebase as fbs
import time
class BackendThreadFirebase(QThread):    
    # 通過類成員物件定義訊號
    update_arm_signal = pyqtSignal(str)
    # 通過類成員物件定義訊號
    update_agv_signal = pyqtSignal(str)
    
    def run(self):
        self.flag = 0
        url = "https://smartmanu-af015.firebaseio.com"
        fdb = fbs.FirebaseApplication(url, None)
        
        while True:
            time.sleep(0.5)
            print('auto')
            AGV = fdb.get('/AGV',None)
            print('AGV',AGV)
            ARM = fdb.get('/ARM',None)
            print('ARM',ARM)
            MES = fdb.get('/MES',None)
            print('MES',MES)
            if AGV['WEDM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                WEDM = fdb.get('/WEDM',None)               
                if list(WEDM.values())==[0,0,0,0,0]:
                    fdb.put(url+"/ARM/",'Moving',1)
                    #self.WEDM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)        
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0000
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                    fdb.put(url+"/ARM/",'Moving',0)
                    fdb.put(url+"/WEDM/",'ChuckEnable',1)
                elif list(WEDM.values())==[1,1,0,0,0]:
                    fdb.put(url+"/ARM/",'Moving',1)
                    #self.WEDM_Arm_Move_MA() #手臂(移動,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0001
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號
                    array = {'Moving':0,'Enable':0}#手臂停止
                    fdb.patch(url+"/ARM/",array)
                elif list(WEDM.values())==[1,1,1,0,0]:
                    fdb.put(url+"/ARM/",'Moving',1)
                    #self.WEDM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0010
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                    fdb.put(url+"/ARM/",'Moving',0)
                    fdb.put(url+"/WEDM/",'ChuckEnable',0)
                elif list(WEDM.values())==[0,0,1,0,0]:
                    fdb.put(url+"/WEDM/",'Done',0)
                    fdb.put(url+"/ARM/",'Moving',1)
                    #self.WEDM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0011
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號
                    array = {'Moving':0,'Enable':0}#手臂停止
                    fdb.patch(url+"/ARM/",array)
            if AGV['HSM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                HSM = fdb.get('/HSM',None)
                print('HSM',HSM)
                if list(HSM.values())==[0,0,0,0,0]:
                    #self.HSM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0100
                    pdate_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(HSM.values())==[1,1,0,0,0]:
                    #self.HSM_Arm_Move_MA() #手臂(移動,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0101
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(HSM.values())==[1,1,1,0,0]:
                    #self.HSM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0110
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(HSM.values())==[1,1,1,0,0]:
                    #self.HSM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b0111
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

            if AGV['Laser']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                Laser = fdb.get('/Laser',None)               
                if list(Laser.values())==[0,0,0,0,0]:
                    #self.Laser_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1000
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(Laser.values())==[1,1,0,0,0]:
                    #self.Laser_Arm_Move_MA() #手臂(移動,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1001
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(Laser.values())==[1,1,1,0,0]:
                    #self.Laser_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1010
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(Laser.values())==[1,1,1,0,0]:
                    #self.Laser_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1011
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

            if AGV['CMM']==1 and list(ARM.values())==[1,0]:#AGV在WEDM並且手臂符合動作
                CMM = fdb.get('/CMM',None)               
                if list(CMM.values())==[0,0,0,0,0]:
                    #self.CMM_Arm_Pinch_AM_I() #手臂(夾放,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1100
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(CMM.values())==[1,1,0,0,0]:
                    #self.CMM_Arm_Move_MA() #手臂(移動,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1101
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(CMM.values())==[1,1,1,0,0]:
                    #self.CMM_Arm_Move_AM_I() #手臂(移動,AGV->機台,影處)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1110
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號

                elif list(CMM.values())==[1,1,1,0,0]:
                    #self.CMM_Arm_Pinch_MA() #手臂(夾放,機台->AGV)
                    #前兩位元是機台 後兩位元是動作
                    Arm_signal = 0b1111
                    self.update_arm_signal.emit( str(Arm_signal) )#發送訊號流訊號
                    
            if list(AGV.values())!=[0,0,0,0] and list(ARM.values())==[0,0] and MES!=0:#AGV在WEDM並且手臂符合動作
                if MES==1:
                    #self.toWEDM()
                    #前兩位元是機台
                    Agv_signal = 0b00
                    self.update_agv_signal.emit( str(Agv_signal) )#發送訊號流訊號

                elif MES==2:
                    #self.toHSM()
                    #前兩位元是機台
                    Agv_signal = 0b01
                    self.update_agv_signal.emit( str(Agv_signal) )#發送訊號流訊號

                elif MES==3:
                    #self.toLaser()
                    #前兩位元是機台
                    Agv_signal = 0b10
                    self.update_agv_signal.emit( str(Agv_signal) )#發送訊號流訊號

                elif MES==4:
                    #self.toCMM()
                    #前兩位元是機台
                    Agv_signal = 0b11
                    self.update_agv_signal.emit( str(Agv_signal) )#發送訊號流訊號

            if self.flag == 1:
                print('stop',self.flag)
                self.flag = 0
                break
    def stop(self): 
        self.flag = 1
        
        
        

        