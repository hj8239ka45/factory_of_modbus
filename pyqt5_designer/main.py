from PyQt5 import QtWidgets
from mainForm import MainUi   # 讀入我們設計的Main Window
import sys
    
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        print(app)
        a_window = MainUi()
        a_window.show()
        a_window.button_enter.clicked.connect(a_window.turn_interface(app))
        sys.exit(app.exec_())
    run_app()
