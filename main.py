import BasicStartStop as GUI
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GUI.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())