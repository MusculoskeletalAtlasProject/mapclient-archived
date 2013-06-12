# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/mainwindow.ui'
#
# Created: Wed Mar 20 09:34:07 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/mapclient/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName(_fromUtf8("menu_Edit"))
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName(_fromUtf8("menu_Tools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.actionPluginManager = QtGui.QAction(MainWindow)
        self.actionPluginManager.setObjectName(_fromUtf8("actionPluginManager"))
        self.actionPMR = QtGui.QAction(MainWindow)
        self.actionPMR.setObjectName(_fromUtf8("actionPMR"))
        self.actionAnnotation = QtGui.QAction(MainWindow)
        self.actionAnnotation.setObjectName(_fromUtf8("actionAnnotation"))
        self.menu_Help.addAction(self.action_About)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Tools.addAction(self.actionPluginManager)
        self.menu_Tools.addAction(self.actionPMR)
        self.menu_Tools.addAction(self.actionAnnotation)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MAP Client", None))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help", None))
        self.menu_File.setTitle(_translate("MainWindow", "&File", None))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit", None))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools", None))
        self.action_About.setText(_translate("MainWindow", "&About", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))
        self.action_Quit.setStatusTip(_translate("MainWindow", "Quit the application", None))
        self.action_Quit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionPluginManager.setText(_translate("MainWindow", "Plugin &Manager", None))
        self.actionPMR.setText(_translate("MainWindow", "&PMR", None))
        self.actionAnnotation.setText(_translate("MainWindow", "&Annotation", None))

import widgets.resources_rc
