# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/CreditsDialog.ui'
#
# Created: Thu Apr  5 11:32:49 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CreditsDialog(object):
    def setupUi(self, CreditsDialog):
        CreditsDialog.setObjectName(_fromUtf8("CreditsDialog"))
        CreditsDialog.resize(475, 356)
        self.verticalLayout = QtGui.QVBoxLayout(CreditsDialog)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_CreditsTab = QtGui.QFrame(CreditsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_CreditsTab.sizePolicy().hasHeightForWidth())
        self.frame_CreditsTab.setSizePolicy(sizePolicy)
        self.frame_CreditsTab.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_CreditsTab.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_CreditsTab.setObjectName(_fromUtf8("frame_CreditsTab"))
        self.verticalLayout.addWidget(self.frame_CreditsTab)
        self.frame = QtGui.QFrame(CreditsDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_Close = QtGui.QPushButton(self.frame)
        self.btn_Close.setObjectName(_fromUtf8("btn_Close"))
        self.horizontalLayout.addWidget(self.btn_Close)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(CreditsDialog)
        QtCore.QObject.connect(self.btn_Close, QtCore.SIGNAL(_fromUtf8("clicked()")), CreditsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(CreditsDialog)

    def retranslateUi(self, CreditsDialog):
        CreditsDialog.setWindowTitle(QtGui.QApplication.translate("CreditsDialog", "MAP Client Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Close.setText(QtGui.QApplication.translate("CreditsDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

