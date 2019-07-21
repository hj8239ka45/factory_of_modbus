from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import os,sys,shutil
from secondForm import SecondUi   # 讀入我們設計的Main Window
from pyModbusTCP.client import ModbusClient

path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile = path + os.sep + "ui" + os.sep + "Main_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.line_ip.setText("192.168.1.1")
        self.line_port.setText("502")
        
        
    def turn_interface(self,app):
        print(app)
        ip = self.line_ip.text()
        port = self.line_port.text()
        print("ip",ip)
        print("port",port)
        
        c1 = ModbusClient() # define modbus server host, port
        c1.host(ip)
        c1.port(port)
        c1.unit_id(1) #set UID to 1
        if not c1.is_open():
            if not c1.open():
                print("unable to connect to "+ip+":"+str(port))
            else:
                print("connected !!")
        if ip=="" or port=="":
            print("keyin the ip or port")
        else:
            b_window = SecondUi()
            b_window.show()
            sys.exit(app.exec_())