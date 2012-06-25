# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/RegisterDialog.ui'
#
# Created: Mon Jun 25 14:22:41 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PMRRegistrationTool(object):
    def setupUi(self, PMRRegistrationTool):
        PMRRegistrationTool.setObjectName(_fromUtf8("PMRRegistrationTool"))
        PMRRegistrationTool.resize(616, 645)
        self.verticalLayout = QtGui.QVBoxLayout(PMRRegistrationTool)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(PMRRegistrationTool)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.webView = QtWebKit.QWebView(self.frame_2)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout_2.addWidget(self.webView, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(PMRRegistrationTool)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Close = QtGui.QPushButton(self.frame)
        self.pushButton_Close.setObjectName(_fromUtf8("pushButton_Close"))
        self.horizontalLayout.addWidget(self.pushButton_Close)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(PMRRegistrationTool)
        QtCore.QObject.connect(self.pushButton_Close, QtCore.SIGNAL(_fromUtf8("clicked()")), PMRRegistrationTool.close)
        QtCore.QMetaObject.connectSlotsByName(PMRRegistrationTool)

    def retranslateUi(self, PMRRegistrationTool):
        PMRRegistrationTool.setWindowTitle(QtGui.QApplication.translate("PMRRegistrationTool", "PMR Registration Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Close.setText(QtGui.QApplication.translate("PMRRegistrationTool", "&Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
