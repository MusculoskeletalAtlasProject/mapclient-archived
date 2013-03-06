# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/workflowwidget.ui'
#
# Created: Wed Mar  6 13:36:49 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_WorkflowWidget(object):
    def setupUi(self, WorkflowWidget):
        WorkflowWidget.setObjectName(_fromUtf8("WorkflowWidget"))
        WorkflowWidget.resize(400, 300)
        WorkflowWidget.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(WorkflowWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(WorkflowWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.stepTree = StepTree(self.splitter)
        self.stepTree.setObjectName(_fromUtf8("stepTree"))
        self.graphicsView = WorkflowGraphicsView(self.splitter)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(WorkflowWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkflowWidget)

    def retranslateUi(self, WorkflowWidget):
        pass

from widgets.steptree import StepTree
from widgets.workflowgraphicsview import WorkflowGraphicsView
