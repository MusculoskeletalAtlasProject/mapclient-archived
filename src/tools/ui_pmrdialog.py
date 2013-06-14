# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pmrdialog.ui'
#
# Created: Fri Jun 14 11:27:30 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PMRDialog(object):
    def setupUi(self, PMRDialog):
        PMRDialog.setObjectName("PMRDialog")
        PMRDialog.resize(456, 515)
        self.gridLayout_2 = QtGui.QGridLayout(PMRDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(PMRDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(400, 400))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/workmen.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(PMRDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(PMRDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PMRDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PMRDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PMRDialog)

    def retranslateUi(self, PMRDialog):
        PMRDialog.setWindowTitle(QtGui.QApplication.translate("PMRDialog", "Physiome Model Repository", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PMRDialog", "Physiome Model Repository", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
