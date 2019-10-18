# -*- coding: utf-8 -*-
"""
第一個介面建立
區網連線(used with ModbusTCP)建立
使用COM PORT建立
Created on Wed Jul 31 21:24:40 2019
@author: hj823
"""

from PyQt5 import QtWidgets, uic, QtGui
import os
from pyModbusTCP.client import ModbusClient
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from secondForm import SecondUi   # 讀入設計的Second Window
import com_catch as com


'''
    由 main.py 引入此 __init__.py檔案: 使用的 path 路徑也在 main.py 底下
    os.sep 為 python的'\'引入
    由 uic 進行 UI(XML格式) 與 python 之間的引入轉換
'''
path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile_main = path + os.sep + "ui" + os.sep + "Main_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)
c1 = ModbusClient() #define modbus server host, port

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        #繼承QT介面基本設定
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.line_ip.setText("192.168.1.1")
        self.line_port.setText("502")
        self.setWindowIcon(QtGui.QIcon(path + os.sep + 'Me.jpg'))
        
        '''
            測試功能表是否可以建立
            由com_catch的library測試及抓取正在連接的 COM PORT
            COM PORT預設建立10個(編號0~9)
            setShortcut: 建立快捷鍵
            如果COM PORT的預設量超過使用量，會進入except區
            setCOM函式用於抓取選取COM的資料
        '''
        try:
            mainMenu = self.menuBar()
            fileMenu = mainMenu.addMenu('File')
            exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
            exitButton.setShortcut('Ctrl+Q')
            exitButton.setStatusTip('Exit application')
            exitButton.triggered.connect(self.close)
            fileMenu.addAction(exitButton)
            
            enterButton = QAction('Enter', self)
            enterButton.setShortcut('Ctrl+E')
            enterButton.setStatusTip('Enter application')
            enterButton.triggered.connect(self.turn_interface)
            fileMenu.addAction(enterButton)
        
            editMenu = mainMenu.addMenu('Edit')
            COMMenu = editMenu.addMenu('COM')
            self.action0 = COMMenu.addAction(str(com.serial_ports()[0]))
            self.action0.setStatusTip('COM application')
            self.action0.triggered.connect(self.setCom0)
            COMMenu.addAction(self.action0)
            
            self.action1 = COMMenu.addAction(str(com.serial_ports()[1]))
            self.action1.setStatusTip('COM application')
            self.action1.triggered.connect(self.setCom1)
            COMMenu.addAction(self.action1)
            
            self.action2 = COMMenu.addAction(str(com.serial_ports()[2]))
            self.action2.setStatusTip('COM application')
            self.action2.triggered.connect(self.setCom2)
            COMMenu.addAction(self.action2)
            
            self.action3 = COMMenu.addAction(str(com.serial_ports()[3]))
            self.action3.setStatusTip('COM application')
            self.action3.triggered.connect(self.setCom3)
            COMMenu.addAction(self.action3)
            
            self.action4 = COMMenu.addAction(str(com.serial_ports()[4]))
            self.action4.setStatusTip('COM application')
            self.action4.triggered.connect(self.setCom4)
            COMMenu.addAction(self.action4)
            
            self.action5 = COMMenu.addAction(str(com.serial_ports()[5]))
            self.action5.setStatusTip('COM application')
            self.action5.triggered.connect(self.setCom5)
            COMMenu.addAction(self.action5)
            
            self.action6 = COMMenu.addAction(str(com.serial_ports()[6]))
            self.action6.setStatusTip('COM application')
            self.action6.triggered.connect(self.setCom6)
            COMMenu.addAction(self.action6)
            
            self.action7 = COMMenu.addAction(str(com.serial_ports()[7]))
            self.action7.setStatusTip('COM application')
            self.action7.triggered.connect(self.setCom7)
            COMMenu.addAction(self.action7)
            
            self.action8 = COMMenu.addAction(str(com.serial_ports()[8]))
            self.action8.setStatusTip('COM application')
            self.action8.triggered.connect(self.setCom8)
            COMMenu.addAction(self.action8)
            
            self.action9 = COMMenu.addAction(str(com.serial_ports()[9]))
            self.action9.setStatusTip('COM application')
            self.action9.triggered.connect(self.setCom9)
            COMMenu.addAction(self.action9)
        except:
            pass
# =============================================================================
#         for i in range(len(com.serial_ports())):
#             self.action = QAction(str(com.serial_ports()[i]),self)
#             self.action.setStatusTip('COM application')
#             self.action.triggered.connect(self.setCom)
#             COMMenu.addAction(self.action)
# =============================================================================
    
        self.button_enter.clicked.connect(self.turn_interface)
        print('b_window')
# =============================================================================
#     def setCom(self):
#         self.COM = self.action.text()
#         print(self.COM)
# =============================================================================
        
    def setCom0(self):
        self.COM = self.action0.text()
        print(self.COM)
    def setCom1(self):
        self.COM = self.action1.text()
        print(self.COM)
    def setCom2(self):
        self.COM = self.action2.text()
        print(self.COM)
    def setCom3(self):
        self.COM = self.action3.text()
        print(self.COM)
    def setCom4(self):
        self.COM = self.action4.text()
        print(self.COM)
    def setCom5(self):
        self.COM = self.action5.text()
        print(self.COM)
    def setCom6(self):
        self.COM = self.action6.text()
        print(self.COM)
    def setCom7(self):
        self.COM = self.action7.text()
        print(self.COM)
    def setCom8(self):
        self.COM = self.action8.text()
        print(self.COM)
    def setCom9(self):
        self.COM = self.action9.text()
        print(self.COM)
        
        
        
    def closeEvent(self, event):#關閉介面事件: 關閉介面時會觸發
        print("closed!!")
        
        
    '''
        介面轉換判斷
        顯示錯誤事件於最下方的label_error
    '''
    def turn_interface(self):
        ip = self.line_ip.text()
        port = int(self.line_port.text())
        c1.host(ip)
        c1.port(port)
        c1.unit_id(1) #set UID to 1
        c1.timeout(1.5)
        c1.auto_open(True)
        c1.auto_close(True)
        # uncomment this line to see debug message
        c1.debug(True)
        self.Str = ""
        try:
            Com = self.COM
        except:
            try:
                Com = str(com.serial_ports()[0]) or False
            except:
                Com = False
        if not c1.is_open():
            if not c1.open():
                self.Str = "unable to connect to "+ip+":"+str(port)
            else:
                print("connected !!")
        if ip == "" or port == "":
            self.Str = self.Str + "\n" + "&" + "keyin the ip or port"
        elif Com == False:
            self.Str = self.Str + "\n" + "&" + "pls set com port number"
        elif c1.open():
            self.label_error.setText("")
            print(Com)
            #Com = 'COM4'
            self.b_window = SecondUi(c1,Com) #建立第二介面物件
            self.b_window.show()
        print(self.Str)
        self.label_error.setText(self.Str)
        
        
        
