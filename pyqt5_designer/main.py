# -*- coding: utf-8 -*-
"""
程式運行主函式
介面跳轉參考: https://blog.csdn.net/pursuit_zhangyu/article/details/82916224
介面設計參考: http://elmer-storage.blogspot.com/2018/04/pyqt.html
Created on Wed Jul 31 21:24:40 2019
@author: hj823
"""



from PyQt5 import QtWidgets
from PyQt5 import QtCore
from mainForm import MainUi   # 讀入設計的Main Window
import sys

if __name__ == "__main__":
    def run_app():
        app = QtCore.QCoreApplication.instance() #先行抓取QT是否建立成功(開啟介面比較不會有問題)
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        a_window = MainUi() #建立第一個介面的物件
        a_window.show() #第一介面物件顯示
        sys.exit(app.exec_()) #先行抓取QT是否建立成功(開啟介面比較不會有問題)
    run_app()
