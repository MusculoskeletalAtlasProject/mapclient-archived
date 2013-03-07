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
from widgets.workflowwidget import WorkflowWidget

def workflowConfigurationExists(location):
    return os.path.exists(location + '/' + info.WORKFLOW_NAME)

def getWorkflowConfiguration(location):
    return QtCore.QSettings(location + '/' + info.WORKFLOW_NAME, QtCore.QSettings.IniFormat)

class WorkflowError(Exception):
    pass

class Workflow(object):
    '''
    Holds information relating to a workflow.
    '''

    location = None
    version = None

    def __init__(self, location, version):
        self.location = location
        self.version = version

class WorkflowManager():
    '''
    This class managers the workflow.
    '''

    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        self.name = 'workflowManager'
        self.widget = None
        self.widgetIndex = -1
        self.location = None
        self._previousLocation = None
        self.saveStateIndex = 0
        self.currentStateIndex = 0
        self.mainWindow = mainWindow

    def setWidgetIndex(self, index):
        self.widgetIndex = index

    def getWidget(self):
        if not self.widget:
            self.widget = WorkflowWidget(self.mainWindow)

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
        Create a new workflow at the given location.  The location is a directory, if it doesn't exist
        it will be created.  A file 'workflow.conf' is created in the directory at 'location' which holds
        information relating to the workflow.  
        '''

        if location is None:
            raise WorkflowError('No location given to create new workflow.')

        if not os.path.exists(location):
            os.mkdir(location)

        self.location = location
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + location)
        ws = getWorkflowConfiguration(location)
        ws.setValue('version', info.VERSION_STRING)



    def load(self, location):
        '''
        Open a workflow from the given location.
        :param location:
        '''
        if location is None:
            raise WorkflowError('No location given to open workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Location %s does not exist' % location)

        if not workflowConfigurationExists(location):
            raise WorkflowError('No workflow located at %s' % location)

        ws = getWorkflowConfiguration(location)
        if ws.value('version') != info.VERSION_STRING:
            raise WorkflowError('Version mismatch in workflow expected: %s got: %s' % (info.VERSION_STRING, ws.value('version')))

        self.location = location
        ws = getWorkflowConfiguration(location)
        self.widget.loadState(ws)
        self.saveStateIndex = self.currentStateIndex = 0
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + location)

    def save(self):
        ws = getWorkflowConfiguration(self.location)
        self.widget.saveState(ws)
        self.saveStateIndex = self.currentStateIndex
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME + ' - ' + self.location)

    def close(self):
        '''
        Close the current workflow
        '''
        self.location = None
        self.mainWindow.setWindowTitle(info.APPLICATION_NAME)

    def isWorkflowOpen(self):
        return not self.location == None

    def writeSettings(self, settings):
        settings.beginGroup(self.name)
        settings.setValue('_previousLocation', self.widget._previousLocation)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(self.name)
        self.widget._previousLocation = settings.value('_previousLocation', '')
        settings.endGroup()














