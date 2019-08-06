# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:24:40 2019

@author: hj823
"""

# https://blog.csdn.net/pursuit_zhangyu/article/details/82916224
# http://elmer-storage.blogspot.com/2018/04/pyqt.html
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from mainForm import MainUi   # 讀入我們設計的Main Window
import sys
    
if __name__ == "__main__":
    def run_app():
        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
            print('app',app)
        a_window = MainUi()
        a_window.show()
        sys.exit(app.exec_())
    run_app()
