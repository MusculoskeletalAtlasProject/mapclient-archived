# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WorkspaceDockWidget.ui'
#
# Created: Thu Jun  7 20:57:54 2012
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
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.dockWidgetContents)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = StepTree(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout.addWidget(self.splitter)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "Workspace Manager", None, QtGui.QApplication.UnicodeUTF8))

from workspace.widgets.StepTree import StepTree
