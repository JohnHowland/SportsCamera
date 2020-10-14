import BasicStartStop as GUI
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from picamera import PiCamera
from time import sleep


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GUI.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())