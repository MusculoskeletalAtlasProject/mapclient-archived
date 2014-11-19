# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/loginformation.ui'
#
# Created: Wed Nov 19 14:28:27 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LogInformation(object):
    def setupUi(self, LogInformation):
        LogInformation.setObjectName("LogInformation")
        LogInformation.resize(729, 256)
        self.verticalLayout = QtGui.QVBoxLayout(LogInformation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.history = QtGui.QLabel(LogInformation)
        self.history.setObjectName("history")
        self.gridLayout.addWidget(self.history, 0, 0, 1, 1)
        self.error_table = QtGui.QTableWidget(LogInformation)
        self.error_table.setObjectName("error_table")
        self.error_table.setColumnCount(0)
        self.error_table.setRowCount(0)
        self.gridLayout.addWidget(self.error_table, 1, 0, 1, 1)
        self.verticalScrollBar = QtGui.QScrollBar(LogInformation)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.gridLayout.addWidget(self.verticalScrollBar, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(598, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exitWindowButton = QtGui.QPushButton(LogInformation)
        self.exitWindowButton.setObjectName("exitWindowButton")
        self.horizontalLayout.addWidget(self.exitWindowButton)
        spacerItem1 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LogInformation)
        QtCore.QMetaObject.connectSlotsByName(LogInformation)

    def retranslateUi(self, LogInformation):
        LogInformation.setWindowTitle(QtGui.QApplication.translate("LogInformation", "Log Information", None, QtGui.QApplication.UnicodeUTF8))
        self.history.setText(QtGui.QApplication.translate("LogInformation", "History:", None, QtGui.QApplication.UnicodeUTF8))
        self.exitWindowButton.setText(QtGui.QApplication.translate("LogInformation", "Exit", None, QtGui.QApplication.UnicodeUTF8))

