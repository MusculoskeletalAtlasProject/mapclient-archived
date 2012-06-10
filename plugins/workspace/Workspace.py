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
from workspace.widgets.WorkspaceWidget import WorkspaceWidget

def workspaceConfigurationExists(location):
    return os.path.exists(location + '/' + Info.WORKSPACE_NAME)

def getWorkspaceConfiguration(location):
    return QtCore.QSettings(location + '/' + Info.WORKSPACE_NAME, QtCore.QSettings.IniFormat)

class WorkspaceError(Exception):
    pass

class WorkspaceStepPort(object):
    '''
    Describes the location and properties of a port for a workspace step.
    '''
    def __init__(self):
        self.subj = {}
        self.pred = {}
        self.obj = {}

    def addProperty(self, rdftriple):
        self.subj[rdftriple[0]] = rdftriple
        self.pred[rdftriple[1]] = rdftriple
        self.obj[rdftriple[2]] = rdftriple

    def canConnect(self, other):
        if 'pho#workspace#port' in self.subj and 'pho#workspace#port' in other.subj:
            this = self.subj['pho#workspace#port']
            that = other.subj['pho#workspace#port']
            if this[1] == 'provides' and that[1] == 'uses':
                if this[2] == that[2]:
                    return True

        return False


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
    if not hasattr(mainWindow, 'workspaceManager'):
        setattr(mainWindow, 'workspaceManager', Manager())
        stackedWidget = mainWindow.centralWidget().findChild(QtGui.QStackedWidget, 'stackedWidget')
        index = stackedWidget.addWidget(WorkspaceWidget(stackedWidget))
        mainWindow.workspaceManager.widgetIndex = index

    return mainWindow.workspaceManager

class Manager(object):
    '''
    This class managers the workspace.
    '''
    location = None
    widgetIndex = -1

    def __init__(self):
        '''
        Constructor
        '''
        pass


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













