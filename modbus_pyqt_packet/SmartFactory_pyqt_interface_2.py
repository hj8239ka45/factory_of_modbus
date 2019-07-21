##interface 2:send msg.
##four type to send or get msg.
##  @smart manufactory 2019
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class SecondWindow(object):
    #初始設定
    def setupUi(self):
        self.setMinimumSize(575,200)
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()  # 初始化執行B視窗類下的 setupUi 函式
