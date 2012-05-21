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
from PyQt4.QtCore import QAbstractListModel, QModelIndex
from PyQt4.QtGui import QDialog, QListWidgetItem
from workspace.widgets.WorkstepsDialogUi import Ui_WorkstepsDialog
from workspace.Workspace import WorkspaceStep

class StepModel(QAbstractListModel):

    def __init__(self, steps, parent=None, *args, **kwargs):
        QAbstractListModel.__init__(self, parent, *args, **kwargs)
        self.steps = steps

    def rowCount(self, parent=QModelIndex()):
        return len(self.steps)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.steps[index.row()].icon
        else:
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
        self.makeConnections()
        self.workspaceStepPlugins = WorkspaceStep.getPlugins()
        self.ui.listView_Steps.setModel(StepModel(self.workspaceStepPlugins))
        for plugin in self.workspaceStepPlugins:
            print(plugin.icon, plugin.description)
            QListWidgetItem(plugin.icon, plugin.name, self.ui.listWidget_Steps)

    def makeConnections(self):
        self.ui.btn_Add.clicked.connect(self.addStep)

    def getAdd(self):
        return self.add

    def addStep(self):
        self.add = 'add this step'
        self.accept()

