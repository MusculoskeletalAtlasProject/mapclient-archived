# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/loginformation.ui'
#
# Created: Wed Nov 19 16:18:19 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LogInformation(object):
    def setupUi(self, LogInformation):
        LogInformation.setObjectName("LogInformation")
        LogInformation.resize(649, 309)
        LogInformation.setMinimumSize(QtCore.QSize(400, 200))
        LogInformation.setMaximumSize(QtCore.QSize(1000, 600))
        self.verticalLayout = QtGui.QVBoxLayout(LogInformation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.history = QtGui.QLabel(LogInformation)
        self.history.setObjectName("history")
        self.gridLayout.addWidget(self.history, 0, 0, 1, 1)
        self.error_table = QtGui.QTableWidget(LogInformation)
        self.error_table.setRowCount(10)
        self.error_table.setObjectName("error_table")
        self.error_table.setColumnCount(3)
        self.error_table.setRowCount(10)
        item = QtGui.QTableWidgetItem()
        self.error_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.error_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.error_table.setHorizontalHeaderItem(2, item)
        self.error_table.horizontalHeader().setCascadingSectionResizes(False)
        self.error_table.horizontalHeader().setDefaultSectionSize(100)
        self.error_table.horizontalHeader().setStretchLastSection(True)
        self.error_table.verticalHeader().setVisible(False)
        self.error_table.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.error_table, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(598, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeWindowButton = QtGui.QPushButton(LogInformation)
        self.closeWindowButton.setObjectName("closeWindowButton")
        self.horizontalLayout.addWidget(self.closeWindowButton)
        spacerItem1 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LogInformation)
        QtCore.QObject.connect(self.closeWindowButton, QtCore.SIGNAL("clicked()"), LogInformation.close)
        QtCore.QMetaObject.connectSlotsByName(LogInformation)

    def retranslateUi(self, LogInformation):
        LogInformation.setWindowTitle(QtGui.QApplication.translate("LogInformation", "Log Information", None, QtGui.QApplication.UnicodeUTF8))
        self.history.setText(QtGui.QApplication.translate("LogInformation", "History:", None, QtGui.QApplication.UnicodeUTF8))
        self.error_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("LogInformation", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.error_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("LogInformation", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.error_table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("LogInformation", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.closeWindowButton.setText(QtGui.QApplication.translate("LogInformation", "Close", None, QtGui.QApplication.UnicodeUTF8))

