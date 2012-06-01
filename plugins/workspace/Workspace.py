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
from PyQt4.QtCore import QSettings
from settings import Info
from core import PluginFramework

def workspaceConfigurationExists(location):
    return os.path.exists(location + '/' + Info.WORKSPACE_NAME)

def getWorkspaceConfiguration(location):
    return QSettings(location + '/' + Info.WORKSPACE_NAME, QSettings.IniFormat)

class WorkspaceError(Exception):
    pass

'''
Plugins can inherit this mount point to add a workspace step.

 A plugin that registers this mount point must have attributes
 * description
 * icon
 
 A plugin that registers this mount point could have attributes
 * None
 
 It must implement
 * pass 

'''
WorkspaceStep = PluginFramework.MetaPluginMountPoint('WorkspaceStep', (object,), {})

class Direction(object):
    '''
    Pythonesque enum 
    '''
    IN = 0
    OUT = 1

class WorkspaceStepPort(object):
    '''
    Describes the location and properties of a port for a workspace step.
    '''
    location = None
    properties = {}
    direction = None

    def __init__(self, location, direction):
        self.location = location
        self.direction = direction

class Workspace(object):
    '''
    Holds information relating to a workspace.
    '''

    location = None
    version = None

    def __init__(self, location, version):
        self.location = location
        self.version = version

class Manager(object):
    '''
    This class managers the workspace.
    '''
    location = None

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













