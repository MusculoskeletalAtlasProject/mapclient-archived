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
from PyQt4 import QtCore
from settings import info
from core import pluginframework
from widgets.workspacewidget import WorkspaceWidget

def workspaceConfigurationExists(location):
    return os.path.exists(location + '/' + info.WORKSPACE_NAME)

def getWorkspaceConfiguration(location):
    return QtCore.QSettings(location + '/' + info.WORKSPACE_NAME, QtCore.QSettings.IniFormat)

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


class Manager(pluginframework.StackedWidgetMountPoint):
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
        self.location = None
        self.previousLocation = None
        self.saveStateIndex = 0
        self.currentStateIndex = 0
        self.mainWindow = mainWindow

    def setWidgetIndex(self, index):
        self.widgetIndex = index

    def getWidget(self):
        if not self.widget:
            self.widget = WorkspaceWidget(self.mainWindow)

        return self.widget

    def undoStackIndexChanged(self, index):
        if self.saveStateIndex == index:
            self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + self.location)
        elif self.saveStateIndex == self.currentStateIndex:
            self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + self.location + ' *')

        self.currentStateIndex = index

    def isModified(self):
        return self.saveStateIndex == self.currentStateIndex

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
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + location)
        ws = getWorkspaceConfiguration(location)
        ws.setValue('version', info.VERSION_STRING)



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
        if ws.value('version') != info.VERSION_STRING:
            raise WorkspaceError('Version mismatch in workspace expected: %s got: %s' % (info.VERSION_STRING, ws.value('version')))

        self.location = location
        ws = getWorkspaceConfiguration(location)
        self.widget.loadState(ws)
        self.saveStateIndex = self.currentStateIndex = 0
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + location)

    def save(self):
        ws = getWorkspaceConfiguration(self.location)
        self.widget.saveState(ws)
        self.saveStateIndex = self.currentStateIndex
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + self.location)

    def close(self):
        '''
        Close the current workspace
        '''
        self.location = None
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME)

    def isWorkspaceOpen(self):
        return not self.location == None

    def writeSettings(self, settings):
        settings.beginGroup(self.name)
        settings.setValue('previousLocation', self.widget.previousLocation)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(self.name)
        self.widget.previousLocation = settings.value('previousLocation', '')
        settings.endGroup()














