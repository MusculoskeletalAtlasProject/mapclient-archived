# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/fileselectionerror.ui'
#
# Created: Wed Nov 26 10:46:12 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FileSelectionError(object):
    def setupUi(self, FileSelectionError):
        FileSelectionError.setObjectName("FileSelectionError")
        FileSelectionError.resize(261, 84)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileSelectionError.sizePolicy().hasHeightForWidth())
        FileSelectionError.setSizePolicy(sizePolicy)
        FileSelectionError.setMinimumSize(QtCore.QSize(261, 84))
        FileSelectionError.setMaximumSize(QtCore.QSize(261, 84))
        self.verticalLayout = QtGui.QVBoxLayout(FileSelectionError)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(233, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(48, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_2 = QtGui.QLabel(FileSelectionError)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(20, 20))
        self.label_2.setMaximumSize(QtCore.QSize(20, 20))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/workflow/images/yellow_black_exclamation.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label = QtGui.QLabel(FileSelectionError)
        self.label.setMinimumSize(QtCore.QSize(80, 20))
        self.label.setMaximumSize(QtCore.QSize(80, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(75, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtGui.QSpacerItem(158, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton = QtGui.QPushButton(FileSelectionError)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FileSelectionError)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), FileSelectionError.accept)
        QtCore.QMetaObject.connectSlotsByName(FileSelectionError)

    def retranslateUi(self, FileSelectionError):
        FileSelectionError.setWindowTitle(QtGui.QApplication.translate("FileSelectionError", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FileSelectionError", "No file selected!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("FileSelectionError", "OK", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
