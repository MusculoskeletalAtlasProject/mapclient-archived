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
from core.workflowscene import WorkflowScene

def getWorkflowConfigurationAbsoluteFilename(location):
    return os.path.join(location, info.WORKFLOW_NAME)

def workflowConfigurationExists(location):
    return os.path.exists(getWorkflowConfigurationAbsoluteFilename(location))

def getWorkflowConfiguration(location):
    return QtCore.QSettings(getWorkflowConfigurationAbsoluteFilename(location), QtCore.QSettings.IniFormat)

class WorkflowError(Exception):
    pass

class Workflow(object):
    '''
    Holds information relating to a workflow.
    '''

    _location = None
    version = None

    def __init__(self, location, version):
        self._location = location
        self.version = version

class WorkflowManager():
    '''
    This class managers the workflow.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'workflowManager'
#        self.widget = None
#        self.widgetIndex = -1
        self._location = None
        self._previousLocation = None
        self._saveStateIndex = 0
        self._currentStateIndex = 0
        
        self._title = None
        
        self._scene = WorkflowScene(self)
#        self.mainWindow = mainWindow

#    def setWidgetIndex(self, index):
#        self.widgetIndex = index
#
#    def getWidget(self):
#        if not self.widget:
#            self.widget = WorkflowWidget(self.mainWindow)
#
#        return self.widget

    def title(self):
        self._title = info.APPLICATION_NAME
        if self._location:
            self._title = self._title + ' - ' + self._location
        if self._saveStateIndex != self._currentStateIndex:
            self._title = self._title + ' *'

        return self._title
    
    def setLocation(self, location):
        self._location = location
        
    def location(self):
        return self._location
    
    def setPreviousLocation(self, location):
        self._previousLocation = location
        
    def previousLocation(self):
        return self._previousLocation
    
    def scene(self):
        return self._scene
    
    def undoStackIndexChanged(self, index):
        self._currentStateIndex = index
        
    def execute(self):
        self._scene.execute()

    def isModified(self):
        return self._saveStateIndex == self._currentStateIndex

    def new(self, location):
        '''
        Create a new workflow at the given _location.  The _location is a directory, if it doesn't exist
        it will be created.  A file 'workflow.conf' is created in the directory at '_location' which holds
        information relating to the workflow.  
        '''

        if location is None:
            raise WorkflowError('No _location given to create new workflow.')

        if not os.path.exists(location):
            os.mkdir(location)

        self._location = location
        wf = getWorkflowConfiguration(location)
        wf.setValue('version', info.VERSION_STRING)
#        self._title = info.APPLICATION_NAME + ' - ' + location
        self._scene.clear()



    def load(self, location):
        '''
        Open a workflow from the given _location.
        :param _location:
        '''
        if location is None:
            raise WorkflowError('No _location given to open workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Location %s does not exist' % location)

        if not workflowConfigurationExists(location):
            raise WorkflowError('No workflow located at %s' % location)

        wf = getWorkflowConfiguration(location)
        if wf.value('version') != info.VERSION_STRING:
            raise WorkflowError('Version mismatch in workflow expected: %s got: %s' % (info.VERSION_STRING, wf.value('version')))

        self._location = location
        wf = getWorkflowConfiguration(location)
        self._scene.loadState(wf)
        self._saveStateIndex = self._currentStateIndex = 0
#        self._title = info.APPLICATION_NAME + ' - ' + location

    def save(self):
        wf = getWorkflowConfiguration(self._location)
        self._scene.saveState(wf)
        self._saveStateIndex = self._currentStateIndex
#        self._title = info.APPLICATION_NAME + ' - ' + self._location

    def close(self):
        '''
        Close the current workflow
        '''
        self._location = None
        self._saveStateIndex = self._currentStateIndex = 0
#        self._title = info.APPLICATION_NAME

    def isWorkflowOpen(self):
        return not self._location == None

    def writeSettings(self, settings):
        settings.beginGroup(self.name)
        settings.setValue('previousLocation', self._previousLocation)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(self.name)
        self._previousLocation = settings.value('previousLocation', '')
        settings.endGroup()














