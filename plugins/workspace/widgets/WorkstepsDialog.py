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

from PyQt4.Qt import Qt
from PyQt4.QtCore import QAbstractListModel, QModelIndex, QSize
from PyQt4.QtGui import QDialog, QAbstractItemView
from workspace.widgets.WorkstepsDialogUi import Ui_WorkstepsDialog
from workspace.MountPoint import WorkspaceStep
from PyQt4 import QtGui

class StepModel(QAbstractListModel):

    def __init__(self, steps, parent=None, *args, **kwargs):
        QAbstractListModel.__init__(self, parent, *args, **kwargs)
        self.steps = steps

    def rowCount(self, parent=QModelIndex()):
        return len(self.steps)

    def data(self, index, role):
        if index.isValid() and role == Qt.DecorationRole:
            return self.steps[index.row()].icon

        return None


    def stepAt(self, index):
        if 0 <= index.row() < len(self.steps):
            return self.steps[index.row()]

        return None


class WorkstepsDialog(QDialog):
    '''
    Dialog to select from a list of worksteps.
    '''

    add = None
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.ui = Ui_WorkstepsDialog()
        self.ui.setupUi(self)

        self.ui.listView_Steps.setViewMode(QtGui.QListView.IconMode)
        self.ui.listView_Steps.setIconSize(QSize(80, 80))
        self.ui.listView_Steps.setGridSize(QSize(94, 94))
        self.ui.listView_Steps.setSpacing(10)
        self.ui.listView_Steps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.workspaceStepPlugins = WorkspaceStep.getPlugins()
        stepModel = StepModel(self.workspaceStepPlugins)
        self.ui.listView_Steps.setModel(stepModel)
        if self.ui.listView_Steps.model().rowCount() > 0:
            self.ui.listView_Steps.setCurrentIndex(stepModel.index(0))
            self._updateUi()

        # Do this last after the selection model has been created
        self._makeConnections()

    def _makeConnections(self):
        self.ui.btn_Add.clicked.connect(self._addButtonClicked)
        self.ui.listView_Steps.clicked.connect(self._updateUi)
        selectionModel = self.ui.listView_Steps.selectionModel()
        selectionModel.selectionChanged.connect(self._updateUi)

    def addedStep(self):
        return self.add

    def _addButtonClicked(self):
        indexes = self.ui.listView_Steps.selectedIndexes()
        assert(len(indexes) == 1)
        self.add = self.ui.listView_Steps.model().stepAt(indexes[0])
        self.accept()

    def _updateUi(self):
        indexes = self.ui.listView_Steps.selectedIndexes()
        if len(indexes) > 0:
            self.ui.btn_Add.setEnabled(True)
            description = self.ui.listView_Steps.model().stepAt(indexes[0]).description
            self.ui.edit_Description.setPlainText(description)
        else:
            self.ui.btn_Add.setEnabled(False)
            self.ui.edit_Description.setPlainText('')


