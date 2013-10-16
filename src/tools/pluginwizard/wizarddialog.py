'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''

import os

from PySide import QtCore, QtGui

from widgets.utils import createDefaultImageIcon

from tools.pluginwizard.skeleton import SkeletonOptions
from tools.pluginwizard.ui_output import Ui_Output
from tools.pluginwizard.ui_name import Ui_Name
from tools.pluginwizard.ui_ports import Ui_Ports

# Registered field names:
OUTPUT_DIRECTORY_FIELD = 'output_directory'
NAME_FIELD = 'name'
IMAGE_FILE_FIELD = 'image_file'
PACKAGE_NAME_FIELD = 'package_name'
PORTS_FIELD = 'ports_table'

# Style sheets
REQUIRED_STYLE_SHEET = 'background-color: rgba(239, 16, 16, 20%)'
DEFAULT_STYLE_SHEET = ''

class WizardDialog(QtGui.QWizard):


    def __init__(self, parent=None):
        super(WizardDialog, self).__init__(parent)
        self.setWindowTitle('Workflow Step Wizard')

        # set pages
        self.addPage(createIntroPage())
        self.addPage(NameWizardPage())
        self.addPage(PortsWizardPage())
        self.addPage(OutputWizardPage())

        # set images banner, logo, watermark and background
        self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/wizard/images/logo.png'))
#         self.setPixmap(QtGui.QWizard.BannerPixmap, QtGui.QPixmap(':/wizard/images/banner.png'))
#         self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
#         self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))
        self._options = SkeletonOptions()

    def getOptions(self):
        return self._options

    def accept(self):
        self._options.setOutputDirectory(self.field(OUTPUT_DIRECTORY_FIELD))
        self._options.setImageFile(self.field(IMAGE_FILE_FIELD))
        self._options.setName(self.field(NAME_FIELD))
        self._options.setPackageName(self.field(PACKAGE_NAME_FIELD))
        # Registered field failed to return table, may need to set up
        # default property for this to work.  Currently using workaround
        # by directly getting desired widget
        ports_table = self.page(2)._ui.portTableWidget
        row_index = 0
        while row_index < ports_table.rowCount():
            self._options.addPort(ports_table.item(row_index, 0).text(), ports_table.item(row_index, 1).text())
            row_index += 1

        super(WizardDialog, self).accept()
#         QtGui.QDialog.accept()


def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle('Introduction')
    page.setSubTitle('Create skeleton Python code to get started creating a workflow step.')
    label = QtGui.QLabel('This wizard will help get you started creating your own plugin for the MAP Client.')
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    page.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
    page.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))

    return page


class NameWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(NameWizardPage, self).__init__(parent)

        self.setTitle('Identify Workflow Step')
        self.setSubTitle('Set the name and icon (optional) for the workflow step.')

        self._ui = Ui_Name()
        self._ui.setupUi(self)

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidLabel = QtGui.QLabel(self)
        self._invalidLabel.setStyleSheet('border: none; padding: 0px;')

        self._updateImage()

        self._makeConnections()
        self._defineFields()
        self._packageNameEdited = False

    def _defineFields(self):
        self.registerField(NAME_FIELD, self._ui.nameLineEdit)
        self.registerField(PACKAGE_NAME_FIELD, self._ui.packageNameLineEdit)
        self.registerField(IMAGE_FILE_FIELD, self._ui.iconLineEdit)

    def _makeConnections(self):
        self._ui.nameLineEdit.textChanged.connect(self._nameChanged)
        self._ui.nameLineEdit.textChanged.connect(self._updateImage)
        self._ui.packageNameLineEdit.textEdited.connect(self._packageNameChanged)
        self._ui.iconLineEdit.textChanged.connect(self._updateImage)
        self._ui.iconButton.clicked.connect(self._chooseImage)

    def _nameChanged(self):
        self.completeChanged.emit()
        if not self._packageNameEdited:
            package_name = self._ui.nameLineEdit.text().lower()
            package_name = package_name.replace(' ', '')
            self._ui.packageNameLineEdit.setText(package_name + 'step')

    def _packageNameChanged(self):
        self._packageNameEdited = True

    def _chooseImage(self):
        image, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose Image File', options=QtGui.QFileDialog.ReadOnly)
        if len(image) > 0:
            self._ui.iconLineEdit.setText(image)

    def _updateImage(self):

        image_file = self._ui.iconLineEdit.text()
        if image_file:
            image = QtGui.QPixmap(image_file)
            if image:
                self._ui.iconPictureLabel.setPixmap(image.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))
        else:
            image = createDefaultImageIcon(self._ui.nameLineEdit.text())
            self._ui.iconPictureLabel.setPixmap(QtGui.QPixmap.fromImage(image).scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))

    def resizeEvent(self, event):
        rect = self._ui.nameLineEdit.rect()
        pos = self._ui.nameLineEdit.pos()
        self._invalidLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidLabel.move(pos.x() - rect.height() / 2, pos.y() - rect.height() / 4)

    def isComplete(self):
        status = False
        if len(self._ui.nameLineEdit.text()) > 0:
            status = True

        self._invalidLabel.setVisible(not status)

        return status


class PortsWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(PortsWizardPage, self).__init__(parent)

        self.setTitle('Set Step Ports')
        self.setSubTitle('Set the ports for the workflow step.')

        self._ui = Ui_Ports()
        self._ui.setupUi(self)

        self._ui.portTableWidget.setColumnCount(2)
        self._ui.portTableWidget.setShowGrid(False)
        self._ui.portTableWidget.setHorizontalHeaderLabels(['Type', 'Object'])
        horizontal_header = self._ui.portTableWidget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)

        self._updateUi()
        self._defineFields()
        self._makeConnections()

    def _defineFields(self):
        self.registerField(PORTS_FIELD, self._ui.portTableWidget)

    def _updateUi(self):
        have_selected_rows = len(self._ui.portTableWidget.selectedIndexes()) > 0
        self._ui.removeButton.setEnabled(have_selected_rows)

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addPort)
        self._ui.removeButton.clicked.connect(self._removePort)
        self._ui.portTableWidget.itemSelectionChanged.connect(self._updateUi)



    def _addPort(self):

        def createPortTypeComboBox():
            cb = QtGui.QComboBox()
            cb.addItems(['provides', 'uses'])

            return cb

        next_row = self._ui.portTableWidget.rowCount()
        self._ui.portTableWidget.insertRow(next_row)
        self._ui.portTableWidget.setCellWidget(next_row, 0, createPortTypeComboBox())

    def _removePort(self):
        indexes = self._ui.portTableWidget.selectedIndexes()
        reversed_rows = indexes[::2]
        reversed_rows.reverse()
        for row in reversed_rows:
            self._ui.portTableWidget.removeRow(row.row())


class OutputWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(OutputWizardPage, self).__init__(parent)

        self.setTitle('Output Files')
        self.setSubTitle('Specify where you want the wizard to put the generated skeleton code.')

        self._ui = Ui_Output()
        self._ui.setupUi(self)

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidLabel = QtGui.QLabel(self)
        self._invalidLabel.setStyleSheet('border: none; padding: 0px;')

        self.registerField(OUTPUT_DIRECTORY_FIELD, self._ui.directoryLineEdit)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.directoryLineEdit.textChanged.connect(self.completeChanged)
        self._ui.directoryButton.clicked.connect(self._chooseDirectory)

    def _chooseDirectory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, caption='Select Output Directory', directory=self._ui.directoryLineEdit.text(), options=QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ReadOnly)
        if len(directory) > 0:
            self._ui.directoryLineEdit.setText(directory)

    def resizeEvent(self, event):
        rect = self._ui.directoryLineEdit.rect()
        pos = self._ui.directoryLineEdit.pos()
        self._invalidLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidLabel.move(pos.x() - rect.height() / 2, pos.y() - rect.height() / 4)

    def isComplete(self):
        status = False
        directory = self._ui.directoryLineEdit.text()
        if os.path.isdir(directory) and os.access(directory, os.W_OK | os.X_OK):
            status = True

        self._invalidLabel.setVisible(not status)

        return status

