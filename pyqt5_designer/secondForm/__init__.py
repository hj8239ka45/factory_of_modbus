from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber
from PyQt5 import QtCore, QtGui
import os
from pyModbusTCP.client import ModbusClient


path = os.getcwd()
# 設計好的ui檔案路徑
qtCreatorFile = path + os.sep + "ui" + os.sep + "Second_Window.ui"
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class SecondUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.lcd_volt.setDigitCount(4)
        self.lcd_volt.setMode(QLCDNumber.Dec)
        self.lcd_volt.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.read_volt()
        self.display_volt()
    def read_volt(self):
        self.regs = read_holding_registers(0x6E, 1)
        print('regs:\n',self.regs)
    def display_volt(self):
        volt = str(self.reg)
        print(volt)
        self.lcd.display(volt)