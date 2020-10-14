from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 200)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        self.control_bt_start = QtWidgets.QPushButton(Form)
        self.control_bt_start.setObjectName("control_bt_start")
        self.verticalLayout.addWidget(self.control_bt_start)

        self.control_bt_stop = QtWidgets.QPushButton(Form)
        self.control_bt_stop.setObjectName("control_bt_stop")
        self.verticalLayout.addWidget(self.control_bt_stop)

        self.capture = QtWidgets.QPushButton(Form)
        self.capture.setObjectName("capture")
        self.verticalLayout.addWidget(self.capture)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form",     "Cam view"))

        self.control_bt_start.setText(_translate("Form", "Start"))
        self.control_bt_stop.setText(_translate("Form", "Stop"))
        self.capture.setText(_translate("Form",    "Capture"))