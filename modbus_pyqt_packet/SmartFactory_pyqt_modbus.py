##interface 1:ip & port
##four type to send or get msg.
##  @smart manufactory 2019

import sys

from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget

from SmartFactory_pyqt_interface_1_layout import MainWindow #這個是main   主視窗
from SmartFactory_pyqt_interface_2 import SecondWindow #這個是widget 子視窗


if __name__ == "__main__":
    app = QApplication(sys.argv)
    A1 = MainWindow()
    B1 = SecondWindow()
    A1.button_send.clicked.connect(B1.show) #視窗1的開啟視窗按鈕
    
    A1.show()
    sys.exit(app.exec_())
