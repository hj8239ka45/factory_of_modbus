##interface_1_layout :label & edit....
##four type to send or get msg.
##  @smart manufactory 2019

##interface_1_layout :label & edit....
##four type to send or get msg.
##  @smart manufactory 2019

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class MainWindow(object):
    #設定UI內容
    def setupUi(self):
        self.setWindowTitle("Modbus @smart_manufactory_2019")
        self.main_set()
        self.setMinimumSize(575,200)
    #文字標籤
    def setup_label(self):
        self.label_title = QLabel("Modbus_TCP :")
        
        self.label_ip = QLabel("IP :")
        self.label_ip.setFixedWidth(160)
        self.label_ip.setFixedHeight(20)
        
        self.label_port = QLabel("PORT :")
        self.label_port.setFixedWidth(160)
        self.label_port.setFixedHeight(20)
    #文字編輯
    def setup_edit(self):
        self.line_ip = QLineEdit()
        self.line_port = QLineEdit()
    #建立按鈕
    def setup_button(self):
        self.button_send = QPushButton("Send")
    #排版版型&工具
    def setup_layout(self):
        #排版版型
        form_layout = QFormLayout()
        form_layout.addRow(self.label_ip, self.line_ip)
        form_layout.addRow(self.label_port, self.line_port)
        #排版工具
        h_layout = QVBoxLayout()
        h_layout.addWidget(self.label_title)
        h_layout.addLayout(form_layout)
        h_layout.addWidget(self.button_send)
        self.setLayout(h_layout)
    #設定包
    def main_set(self):
        self.setup_label()
        self.setup_edit()
        self.setup_button()
        self.setup_layout()
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()  # 初始化執行A視窗類下的 setupUi 函式
