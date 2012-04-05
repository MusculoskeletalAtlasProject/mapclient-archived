# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AboutDialog.ui'
#
# Created: Thu Apr  5 11:35:28 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AboutDialog.resize(518, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(AboutDialog)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(AboutDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/mapclient/images/AboutLogo.png")))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.frame)
        self.label.setStyleSheet(_fromUtf8("QLabel { background-color : white }"))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(AboutDialog)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btn_Credits = QtGui.QPushButton(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Credits.sizePolicy().hasHeightForWidth())
        self.btn_Credits.setSizePolicy(sizePolicy)
        self.btn_Credits.setObjectName(_fromUtf8("btn_Credits"))
        self.horizontalLayout_2.addWidget(self.btn_Credits)
        self.btn_License = QtGui.QPushButton(self.frame_3)
        self.btn_License.setObjectName(_fromUtf8("btn_License"))
        self.horizontalLayout_2.addWidget(self.btn_License)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_Close = QtGui.QPushButton(self.frame_3)
        self.btn_Close.setObjectName(_fromUtf8("btn_Close"))
        self.horizontalLayout_2.addWidget(self.btn_Close)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.btn_Close, QtCore.SIGNAL(_fromUtf8("clicked()")), AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About MAP Client", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AboutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">MAP Client</span></p><p align=\"center\">MAP Client, a program to generate detailed musculoskeletal models for OpenSim.</p><p align=\"center\">Copyright (C) 2012 University of Auckland</p><p align=\"justify\">MAP Client is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p><p align=\"justify\">MAP Client is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</p><p align=\"justify\">You should have received a copy of the GNU General Public License along with MAP Client. If not, see &lt;http://www.gnu.org/licenses/&gt;.</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Credits.setText(QtGui.QApplication.translate("AboutDialog", "C&redits", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_License.setText(QtGui.QApplication.translate("AboutDialog", "&License", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Close.setText(QtGui.QApplication.translate("AboutDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

import widgets.Resources_rc
