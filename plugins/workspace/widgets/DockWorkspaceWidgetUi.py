# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DockWorkspaceWidget.ui'
#
# Created: Thu Jun  7 11:35:07 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(883, 505)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.splitter = QtGui.QSplitter(self.dockWidgetContents)
        self.splitter.setGeometry(QtCore.QRect(60, 20, 0, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = StepTree(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "Workspace Manager", None, QtGui.QApplication.UnicodeUTF8))

from workspace.widgets.StepTree import StepTree
