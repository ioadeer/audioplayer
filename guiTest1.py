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
        Dialog.resize(672, 368)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 641, 351))
        self.tabWidget.setObjectName("tabWidget")
        self.processTab = QtWidgets.QWidget()
        self.processTab.setObjectName("processTab")
        self.label = QtWidgets.QLabel(self.processTab)
        self.label.setGeometry(QtCore.QRect(10, 20, 41, 21))
        self.label.setObjectName("label")
        self.labelFileName = QtWidgets.QLabel(self.processTab)
        self.labelFileName.setGeometry(QtCore.QRect(50, 20, 431, 21))
        self.labelFileName.setObjectName("labelFileName")
        self.pushButtonLoadFile = QtWidgets.QPushButton(self.processTab)
        self.pushButtonLoadFile.setGeometry(QtCore.QRect(500, 20, 89, 25))
        self.pushButtonLoadFile.setObjectName("pushButtonLoadFile")
        self.listWidgetFeatures = QtWidgets.QListWidget(self.processTab)
        self.listWidgetFeatures.setGeometry(QtCore.QRect(10, 120, 261, 191))
        self.listWidgetFeatures.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetFeatures.setObjectName("listWidgetFeatures")
        self.comboBoxGrainSize = QtWidgets.QComboBox(self.processTab)
        self.comboBoxGrainSize.setGeometry(QtCore.QRect(90, 50, 111, 25))
        self.comboBoxGrainSize.setObjectName("comboBoxGrainSize")
        self.label_2 = QtWidgets.QLabel(self.processTab)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.processTab)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 81, 21))
        self.label_3.setObjectName("label_3")
        self.listWidgetSelectedFeatures = QtWidgets.QListWidget(self.processTab)
        self.listWidgetSelectedFeatures.setGeometry(QtCore.QRect(320, 120, 261, 101))
        self.listWidgetSelectedFeatures.setObjectName("listWidgetSelectedFeatures")
        self.label_4 = QtWidgets.QLabel(self.processTab)
        self.label_4.setGeometry(QtCore.QRect(320, 90, 211, 21))
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.processTab, "")
        self.playTab = QtWidgets.QWidget()
        self.playTab.setObjectName("playTab")
        self.readPoint = QtWidgets.QSlider(self.playTab)
        self.readPoint.setGeometry(QtCore.QRect(30, 240, 581, 61))
        self.readPoint.setOrientation(QtCore.Qt.Horizontal)
        self.readPoint.setObjectName("readPoint")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.playTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(530, 150, 71, 80))
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
        self.tabWidget.addTab(self.playTab, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "File :"))
        self.labelFileName.setText(_translate("Dialog", "TextLabel"))
        self.pushButtonLoadFile.setText(_translate("Dialog", "Load File"))
        self.label_2.setText(_translate("Dialog", "Grain Size:"))
        self.label_3.setText(_translate("Dialog", "Features"))
        self.label_4.setText(_translate("Dialog", "Selected Features"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.processTab), _translate("Dialog", "Process"))
        self.playButton.setText(_translate("Dialog", "play"))
        self.stopButton.setText(_translate("Dialog", "stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.playTab), _translate("Dialog", "Play"))


