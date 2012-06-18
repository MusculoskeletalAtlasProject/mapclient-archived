# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WorkspaceWidget.ui'
#
# Created: Thu Jun  7 21:33:09 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WorkspaceWidget(object):
    def setupUi(self, WorkspaceWidget):
        WorkspaceWidget.setObjectName(_fromUtf8("WorkspaceWidget"))
        WorkspaceWidget.resize(400, 300)
        WorkspaceWidget.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(WorkspaceWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(WorkspaceWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = StepTree(self.splitter)
        self.widget.setObjectName(_fromUtf8("stepTree"))
        self.graphicsView = WorkspaceGraphicsView(self.splitter)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(WorkspaceWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkspaceWidget)

    def retranslateUi(self, WorkspaceWidget):
        pass

from workspace.widgets.StepTree import StepTree
from workspace.widgets.WorkspaceGraphicsView import WorkspaceGraphicsView
