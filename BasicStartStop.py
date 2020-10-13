# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BasicStartStop.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(697, 381)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
		
		#Snapshot button
        self.snapShotPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.snapShotPushButton.setGeometry(QtCore.QRect(10, 240, 171, 101))
        self.snapShotPushButton.setObjectName("snapShotPushButton")
		
		#Start button
        self.startPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startPushButton.setGeometry(QtCore.QRect(10, 20, 171, 101))
        self.startPushButton.setObjectName("startPushButton")
		
		#Stop button
        self.stopPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopPushButton.setGeometry(QtCore.QRect(10, 130, 171, 101))
        self.stopPushButton.setObjectName("stopPushButton")
		
		#Text browser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(200, 20, 481, 321))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		#Connected the buttons to their callbacks
        self.startPushButton.clicked.connect(self.start_callback)
        self.stopPushButton.clicked.connect(self.stop_callback)
        self.snapShotPushButton.clicked.connect(self.snap_callback)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.snapShotPushButton.setText(_translate("MainWindow", "Snapshot"))
        self.startPushButton.setText(_translate("MainWindow", "Start"))
        self.stopPushButton.setText(_translate("MainWindow", "stop"))

    def start_callback(self):
        #print("You are in the start callback function");
        self.PutMsg("You are in the start callback function")

    def stop_callback(self):
        self.PutMsg("You are in the stop callback function");

    def snap_callback(self):
        self.PutMsg("You are in the snap callback function");

    def PutMsg(self, msg):
        self.textBrowser.append(msg)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
