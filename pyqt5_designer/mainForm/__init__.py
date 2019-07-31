from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QFileDialog
from PyQt5 import QtCore, QtGui
import os,sys,shutil
from pyModbusTCP.client import ModbusClient

path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile_main = path + os.sep + "ui" + os.sep + "Main_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)
c1 = ModbusClient() #define modbus server host, port

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.line_ip.setText("192.168.1.1")
        self.line_port.setText("502")
        self.b_window = SecondUi()
        self.button_enter.clicked.connect(self.turn_interface)
        print('b_window')
        
    def turn_interface(self):
        ip = self.line_ip.text()
        port = int(self.line_port.text())
        print("ip",type(ip))
        print("port",type(port))
        c1.host(ip)
        c1.port(port)
        c1.unit_id(1) #set UID to 1
        c1.auto_open(True)
        c1.auto_close(True)
        # uncomment this line to see debug message
        c1.debug(True)

        print(c1)
        if not c1.is_open():
            if not c1.open():
                print("unable to connect to "+ip+":"+str(port))
            else:
                print("connected !!")
        if ip=="" or port=="":
            print("keyin the ip or port")
        elif c1.open():
            regs = c1.read_holding_registers(0x6E, 1)
            print('regs:\n',regs)
            self.b_window.show()

# 設計好的ui檔案路徑
qtCreatorFile_second = path + os.sep + "ui" + os.sep + "Second_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_SecondWindow, QtBaseClass_second = uic.loadUiType(qtCreatorFile_second)

class SecondUi(QtWidgets.QMainWindow, Ui_SecondWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.lcd_volt.setDigitCount(5)
        self.lcd_volt.setMode(QLCDNumber.Dec)
        self.lcd_volt.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.button_send.clicked.connect(self.display)
    def display(self):
        self.read_volt()
        self.display_volt()
        self.get_station()
        self.write_station()
    def get_station(self):
        self.station = self.line_station.text()
        print('regs:\n',self.station,type(int(self.station)))
    def write_station(self):
        c1.write_single_register(0xD6,int(self.station))
    def read_volt(self):
        self.regs = c1.read_holding_registers(0x6E, 1)
        print('regs:\n',self.regs)
    def display_volt(self):
        volt = str(self.regs)
        print("volt",volt)
        self.lcd_volt.display(volt)

