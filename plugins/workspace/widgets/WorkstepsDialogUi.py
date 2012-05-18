# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WorkstepsDialog.ui'
#
# Created: Fri May 18 15:52:02 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WorkstepsDialog(object):
    def setupUi(self, WorkstepsDialog):
        WorkstepsDialog.setObjectName(_fromUtf8("WorkstepsDialog"))
        WorkstepsDialog.resize(561, 426)
        self.gridLayout = QtGui.QGridLayout(WorkstepsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(WorkstepsDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listView_Steps = QtGui.QListView(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_Steps.sizePolicy().hasHeightForWidth())
        self.listView_Steps.setSizePolicy(sizePolicy)
        self.listView_Steps.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listView_Steps.setObjectName(_fromUtf8("listView_Steps"))
        self.verticalLayout.addWidget(self.listView_Steps)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(WorkstepsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.edit_Description = QtGui.QPlainTextEdit(self.groupBox_2)
        self.edit_Description.setReadOnly(True)
        self.edit_Description.setObjectName(_fromUtf8("edit_Description"))
        self.verticalLayout_2.addWidget(self.edit_Description)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 3)
        self.frame = QtGui.QFrame(WorkstepsDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_Add = QtGui.QPushButton(self.frame)
        self.btn_Add.setMinimumSize(QtCore.QSize(75, 0))
        self.btn_Add.setObjectName(_fromUtf8("btn_Add"))
        self.horizontalLayout.addWidget(self.btn_Add)
        self.btn_Cancel = QtGui.QPushButton(self.frame)
        self.btn_Cancel.setMinimumSize(QtCore.QSize(75, 0))
        self.btn_Cancel.setObjectName(_fromUtf8("btn_Cancel"))
        self.horizontalLayout.addWidget(self.btn_Cancel)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 4)

        self.retranslateUi(WorkstepsDialog)
        QtCore.QObject.connect(self.btn_Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), WorkstepsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(WorkstepsDialog)

    def retranslateUi(self, WorkstepsDialog):
        WorkstepsDialog.setWindowTitle(QtGui.QApplication.translate("WorkstepsDialog", "Worksteps", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("WorkstepsDialog", "Steps:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("WorkstepsDialog", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Add.setText(QtGui.QApplication.translate("WorkstepsDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Cancel.setText(QtGui.QApplication.translate("WorkstepsDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

