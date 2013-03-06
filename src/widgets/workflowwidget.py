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
from PyQt4 import QtGui
from widgets.ui_workflowwidget import Ui_WorkflowWidget
from mountpoints.workflowstep import WorkflowStepMountPoint

class WorkflowWidget(QtGui.QWidget):
    '''
    classdocs
    '''
    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self)
        self.mainWindow = mainWindow
        self._ui = Ui_WorkflowWidget()
        self._ui.setupUi(self)
        self._ui.graphicsView.undoStack.indexChanged.connect(self.undoStackIndexChanged)
        self._ui.graphicsView.mainWindow = mainWindow
        self.action_Close = None # Keep a handle to this for modifying the Ui.
        self._createMenuItems()
        self._previousLocation = ''

        self.workflowStepPlugins = WorkflowStepMountPoint.getPlugins()
        self.stepTree = self.findChild(QtGui.QWidget, "stepTree")
        for step in self.workflowStepPlugins:
            self.stepTree.addStep(step)

        self.updateUi()

    def updateUi(self):
        workflowOpen = self.mainWindow.workflowManager.isWorkflowOpen()
        self.action_Close.setEnabled(workflowOpen)
        self.setEnabled(workflowOpen)
        self.action_Save.setEnabled(not self.mainWindow.workflowManager.isModified())

    def undoStackIndexChanged(self, index):
        self.mainWindow.workflowManager.undoStackIndexChanged(index)
        self.updateUi()

    def setActive(self):
        self.mainWindow.setUndoStack(self._ui.graphicsView.undoStack)

    def _setActionProperties(self, action, name, slot, shortcut='', statustip=''):
        action.setObjectName(name)
        action.triggered.connect(slot)
        if len(shortcut) > 0:
            action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setStatusTip(statustip)


    def new(self):
        workflowDir = QtGui.QFileDialog.getExistingDirectory(self.mainWindow, caption='Select Workflow Directory', directory=self._previousLocation)
        if len(workflowDir) > 0:
            m = self.mainWindow.workflowManager
            m.new(workflowDir)
            self._previousLocation = workflowDir
            self.updateUi()

    def load(self):
        workflowDir = QtGui.QFileDialog.getExistingDirectory(self.mainWindow, caption='Open Workflow', directory=self._previousLocation, options=QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ReadOnly)
        if len(workflowDir) > 0:
            m = self.mainWindow.workflowManager
            m.load(workflowDir)
            self._previousLocation = workflowDir
            self.updateUi()

    def close(self):
        m = self.mainWindow.workflowManager
        m.close()
        self._ui.graphicsView.clear()
        self.updateUi()

    def save(self):
        m = self.mainWindow.workflowManager
        m.save()
        self.updateUi()

    def saveState(self, ws):
        self._ui.graphicsView.saveState(ws)
        self.updateUi()

    def loadState(self, ws):
        self._ui.graphicsView.loadState(ws)
        self.updateUi()

    def _createMenuItems(self):
        menu_File = self.mainWindow._ui.menubar.findChild(QtGui.QMenu, 'menu_File')
        lastFileMenuAction = menu_File.actions()[-1]
        menu_New = menu_File.findChild(QtGui.QMenu, name='&New')
        if not menu_New:
            menu_New = QtGui.QMenu('&New', menu_File)

        action_New = QtGui.QAction('Workflow', menu_New)
        self._setActionProperties(action_New, 'action_New', self.new, 'Ctrl+N', 'Create a new workflow')
        action_Open = QtGui.QAction('&Open', menu_File)
        self._setActionProperties(action_Open, 'action_Open', self.load, 'Ctrl+O', 'Open an existing workflow')
        self.action_Close = QtGui.QAction('&Close', menu_File)
        self._setActionProperties(self.action_Close, 'action_Close', self.close, 'Ctrl+W', 'Close open workflow')
        self.action_Save = QtGui.QAction('&Save', menu_File)
        self._setActionProperties(self.action_Save, 'action_Save', self.save, 'Ctrl+S', 'Save workflow')

        menu_New.insertAction(QtGui.QAction(self), action_New)
        menu_File.insertMenu(lastFileMenuAction, menu_New)
        menu_File.insertAction(lastFileMenuAction, action_Open)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Close)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Save)
        menu_File.insertSeparator(lastFileMenuAction)

