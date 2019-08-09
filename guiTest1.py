# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiForScript.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(646, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(420, 70, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playSound= QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.playSound.setObjectName("playSound")
        self.verticalLayout.addWidget(self.playSound)
        self.stopButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout.addWidget(self.stopButton)
        self.readPoint = QtWidgets.QSlider(Dialog)
        self.readPoint.setGeometry(QtCore.QRect(80, 190, 471, 61))
        self.readPoint.setOrientation(QtCore.Qt.Horizontal)
        self.readPoint.setObjectName("readPoint")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.playSound.setText(_translate("Dialog", "play"))
        self.stopButton.setText(_translate("Dialog", "stop"))


