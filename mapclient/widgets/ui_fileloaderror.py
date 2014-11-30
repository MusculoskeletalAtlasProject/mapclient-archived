# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/fileloaderror.ui'
#
# Created: Wed Nov 26 12:23:30 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FileLoadError(object):
    def setupUi(self, FileLoadError):
        FileLoadError.setObjectName("FileLoadError")
        FileLoadError.resize(261, 84)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileLoadError.sizePolicy().hasHeightForWidth())
        FileLoadError.setSizePolicy(sizePolicy)
        FileLoadError.setMinimumSize(QtCore.QSize(261, 84))
        FileLoadError.setMaximumSize(QtCore.QSize(261, 84))
        self.verticalLayout = QtGui.QVBoxLayout(FileLoadError)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(233, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(45, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_2 = QtGui.QLabel(FileLoadError)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(20, 20))
        self.label_2.setMaximumSize(QtCore.QSize(20, 20))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/mapclient/images/round_error_logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label = QtGui.QLabel(FileLoadError)
        self.label.setMinimumSize(QtCore.QSize(90, 20))
        self.label.setMaximumSize(QtCore.QSize(90, 20))
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
        self.pushButton = QtGui.QPushButton(FileLoadError)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FileLoadError)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), FileLoadError.close)
        QtCore.QMetaObject.connectSlotsByName(FileLoadError)

    def retranslateUi(self, FileLoadError):
        FileLoadError.setWindowTitle(QtGui.QApplication.translate("FileLoadError", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FileLoadError", "Failed to load file!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("FileLoadError", "OK", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
