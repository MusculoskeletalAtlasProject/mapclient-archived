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

from PyQt4 import QtCore, QtGui
from core import PluginFramework
from workspace.Workspace import Manager, getWorkspaceManagerCreateIfNecessary

# Placed in reverse order so that when the menu options are inserted before any 
# other action the desired order is achieved.

class WorkspaceViewMenu(PluginFramework.MenuOption):
    '''
    '''
    parent = None
    menuLabel = '&Window'
    menuName = 'menu_Window'
    actionLabel = 'Workspace'
    statustip = 'Show the workspace window'

    def __init__(self):
        QtCore.QObject.__init__(self)

    def execute(self):
        pass
#        self.parent.setCentralWidget(WorkspaceWidget(self.parent))

class WorkspaceCloseMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    parent = None
    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = '&Close'
    shortcut = 'Ctrl+W'
    statustip = 'Close open workspace'

    def __init__(self):
        '''
        Constructor
        '''
        QtCore.QObject.__init__(self)

    def execute(self):
        m = Manager()
        m.close()


class WorkspaceSeparatorMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    parent = None
    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = ''

    def __init__(self):
        '''
        Constructor
        '''
        QtCore.QObject.__init__(self)

    def execute(self):
        pass


class WorkspaceOpenMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    parent = None
    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = '&Open'
    shortcut = 'Ctrl+O'
    statustip = 'Open a workspace'

    def __init__(self):
        '''
        Constructor
        '''
        QtCore.QObject.__init__(self)

    def execute(self):
        workspaceDir = QtGui.QFileDialog.getExistingDirectory(caption='Open Workspace', options=QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ReadOnly)
        if len(workspaceDir) > 0:
            m = getWorkspaceManagerCreateIfNecessary(self.parent)
            m.load(workspaceDir)


class WorkspaceNewWorkspaceMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    parent = None
    menuLabel = '&File'
    menuName = 'menu_File'
    subMenuLabel = '&New'
    subMenuName = 'menu_New'
    actionLabel = '&Workspace'
    shortcut = 'Ctrl+N'
    statustip = 'Create a new workspace'

    def __init__(self):
        '''
        Constructor
        '''
        QtCore.QObject.__init__(self)

    def execute(self):
        workspaceDir = QtGui.QFileDialog.getExistingDirectory(self.parent, caption='Select Workspace Directory')
        if len(workspaceDir) > 0:
            m = getWorkspaceManagerCreateIfNecessary(self.parent)
            m.new(workspaceDir)



