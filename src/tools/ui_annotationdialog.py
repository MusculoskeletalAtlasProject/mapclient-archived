# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/annotationdialog.ui'
#
# Created: Fri Jun 14 11:26:47 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AnnotationDialog(object):
    def setupUi(self, AnnotationDialog):
        AnnotationDialog.setObjectName("AnnotationDialog")
        AnnotationDialog.resize(454, 513)
        self.verticalLayout = QtGui.QVBoxLayout(AnnotationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(AnnotationDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(400, 400))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/sad_face.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(AnnotationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AnnotationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AnnotationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AnnotationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnnotationDialog)

    def retranslateUi(self, AnnotationDialog):
        AnnotationDialog.setWindowTitle(QtGui.QApplication.translate("AnnotationDialog", "Annotation Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("AnnotationDialog", "Annotation", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
