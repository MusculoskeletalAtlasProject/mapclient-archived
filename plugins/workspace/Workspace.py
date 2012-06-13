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
from PyQt4 import QtCore, QtGui
from settings import Info
from core import PluginFramework
from workspace.widgets.WorkspaceWidget import WorkspaceWidget

def workspaceConfigurationExists(location):
    return os.path.exists(location + '/' + Info.WORKSPACE_NAME)

def getWorkspaceConfiguration(location):
    return QtCore.QSettings(location + '/' + Info.WORKSPACE_NAME, QtCore.QSettings.IniFormat)

class WorkspaceError(Exception):
    pass

class Workspace(object):
    '''
    Holds information relating to a workspace.
    '''

    location = None
    version = None

    def __init__(self, location, version):
        self.location = location
        self.version = version

def getWorkspaceManagerCreateIfNecessary(mainWindow):
#    if not hasattr(mainWindow, 'workspaceManager'):
#        setattr(mainWindow, 'workspaceManager', Manager(mainWindow))
#        stackedWidget = mainWindow.centralWidget().findChild(QtGui.QStackedWidget, 'stackedWidget')
#        index = stackedWidget.addWidget(WorkspaceWidget(stackedWidget))
#        mainWindow.workspaceManager.widgetIndex = index

    return mainWindow.workspaceManager


class UndoManager(object):
    '''
    This class is the undo redo manager for multiple undo stacks. It is a
    singleton class. 
    
    Don't inherit from this class.
    '''
    _instance = None
    undoAction = None
    redoAction = None
    stack = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UndoManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def createUndoAction(self, parent):
        self.undoAction = QtGui.QAction('Undo', parent)
        self.undoAction.triggered.connect(self.undo)
        if self.stack:
            self.undoAction.setEnabled(self.stack.canUndo())
        else:
            self.undoAction.setEnabled(False)

        return self.undoAction

    def createRedoAction(self, parent):
        self.redoAction = QtGui.QAction('Redo', parent)
        self.redoAction.triggered.connect(self.redo)
        if self.stack:
            self.redoAction.setEnabled(self.stack.canRedo())
        else:
            self.redoAction.setEnabled(False)

        return self.redoAction

    def setCurrentStack(self, stack):
        if self.stack:
            self.stack.canRedoChanged.disconnect(self._canRedoChanged)
            self.stack.canUndoChanged.disconnect(self._canUndoChanged)

        self.stack = stack
        self.redoAction.setEnabled(stack.canRedo())
        self.undoAction.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._canUndoChanged)
        stack.canRedoChanged.connect(self._canRedoChanged)

    def currentStack(self):
        return self.stack

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def _canRedoChanged(self, canRedo):
        self.redoAction.setEnabled(canRedo)

    def _canUndoChanged(self, canUndo):
        self.undoAction.setEnabled(canUndo)


class Manager(PluginFramework.StackedWidgetMountPoint):
    '''
    This class managers the workspace.
    '''

    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        self.name = 'workspaceManager'
        self.widget = None
        self.widgetIndex = -1
        self.mainWindow = mainWindow
        self.undoManager = UndoManager()

        undoAction = self.undoManager.createUndoAction(mainWindow)
        undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        redoAction = self.undoManager.createRedoAction(mainWindow)
        redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))

        editMenu = mainWindow.findChild(QtGui.QMenu, 'menu_Edit')
#        editMenu.addAction(undoAction)
#        editMenu.addAction(redoAction)


    def getWidget(self, parent):
        if not self.widget:
            self.widget = WorkspaceWidget(parent)

        return self.widget

    def new(self, location):
        '''
        Create a new workspace at the given location.  The location is a directory, if it doesn't exist
        it will be created.  A file 'workspace.conf' is created in the directory at 'location' which holds
        information relating to the workspace.  
        '''

        if location is None:
            raise WorkspaceError('No location given to create new workspace.')

        if not os.path.exists(location):
            os.mkdir(location)

        self.location = location
        ws = getWorkspaceConfiguration(location)
        ws.setValue('version', Info.VERSION_STRING)



    def load(self, location):
        '''
        Open a workspace from the given location.
        :param location:
        '''
        if location is None:
            raise WorkspaceError('No location given to open workspace.')

        if not os.path.exists(location):
            raise WorkspaceError('Location %s does not exist' % location)

        if not workspaceConfigurationExists(location):
            raise WorkspaceError('No workspace located at %s' % location)

        ws = getWorkspaceConfiguration(location)
        if ws.value('version') != Info.VERSION_STRING:
            raise WorkspaceError('Version mismatch in workspace expected: %s got: %s' % (Info.VERSION_STRING, ws.value('version')))

        self.location = location

    def close(self):
        '''
        Close the current workspace
        '''
        self.location = None













