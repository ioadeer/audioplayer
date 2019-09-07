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
        Dialog.resize(653, 368)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(540, 90, 71, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.playButton.setObjectName("playButton")
        self.verticalLayout.addWidget(self.playButton)
        self.stopButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout.addWidget(self.stopButton)
        self.readPoint = QtWidgets.QSlider(Dialog)
        self.readPoint.setGeometry(QtCore.QRect(30, 160, 581, 61))
        self.readPoint.setOrientation(QtCore.Qt.Horizontal)
        self.readPoint.setObjectName("readPoint")
        self.pushButtonLoadFile = QtWidgets.QPushButton(Dialog)
        self.pushButtonLoadFile.setGeometry(QtCore.QRect(520, 50, 89, 25))
        self.pushButtonLoadFile.setObjectName("pushButtonLoadFile")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 50, 41, 21))
        self.label.setObjectName("label")
        self.labelFileName = QtWidgets.QLabel(Dialog)
        self.labelFileName.setGeometry(QtCore.QRect(70, 50, 431, 21))
        self.labelFileName.setObjectName("labelFileName")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.playButton.setText(_translate("Dialog", "play"))
        self.stopButton.setText(_translate("Dialog", "stop"))
        self.pushButtonLoadFile.setText(_translate("Dialog", "Load File"))
        self.label.setText(_translate("Dialog", "File :"))
        self.labelFileName.setText(_translate("Dialog", "TextLabel"))


