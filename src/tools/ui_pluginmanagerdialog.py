# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pluginmanagerdialog.ui'
#
# Created: Sun Mar 24 19:54:46 2013
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

class Ui_PluginManagerDialog(object):
    def setupUi(self, PluginManagerDialog):
        PluginManagerDialog.setObjectName(_fromUtf8("PluginManagerDialog"))
        PluginManagerDialog.resize(567, 496)
        self.verticalLayout = QtGui.QVBoxLayout(PluginManagerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(PluginManagerDialog)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.directoryListing = QtGui.QListWidget(self.groupBox)
        self.directoryListing.setObjectName(_fromUtf8("directoryListing"))
        self.verticalLayout_3.addWidget(self.directoryListing)
        self.defaultPluginCheckBox = QtGui.QCheckBox(self.groupBox)
        self.defaultPluginCheckBox.setChecked(True)
        self.defaultPluginCheckBox.setObjectName(_fromUtf8("defaultPluginCheckBox"))
        self.verticalLayout_3.addWidget(self.defaultPluginCheckBox)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.addButton = QtGui.QPushButton(self.groupBox)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(self.groupBox)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout_2.addWidget(self.removeButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(PluginManagerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PluginManagerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PluginManagerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PluginManagerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginManagerDialog)

    def retranslateUi(self, PluginManagerDialog):
        PluginManagerDialog.setWindowTitle(_translate("PluginManagerDialog", "Plugin Manager", None))
        self.groupBox.setTitle(_translate("PluginManagerDialog", "Plugin Manager", None))
        self.label.setText(_translate("PluginManagerDialog", "Plugin directories:", None))
        self.defaultPluginCheckBox.setText(_translate("PluginManagerDialog", "Use default plugin directory", None))
        self.addButton.setText(_translate("PluginManagerDialog", "Add Directory", None))
        self.removeButton.setText(_translate("PluginManagerDialog", "Remove Directory", None))

