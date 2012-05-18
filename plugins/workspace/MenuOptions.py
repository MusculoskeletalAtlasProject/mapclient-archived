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

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QFileDialog
from core import PluginFramework
from workspace.Workspace import Manager

# Placed in reverse order so that when the menu options are inserted before any 
# other action the desired order is achieved.
class WorkspaceCloseMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = '&Close'
    shortcut = 'Ctrl+W'
    statustip = 'Close open workspace'

    def __init__(self):
        '''
        Constructor
        '''
        QObject.__init__(self)

    def execute(self):
        m = Manager()
        m.close()


class WorkspaceSeparatorMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = ''

    def __init__(self):
        '''
        Constructor
        '''
        QObject.__init__(self)

    def execute(self):
        pass


class WorkspaceOpenMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    menuLabel = '&File'
    menuName = 'menu_File'
    actionLabel = '&Open'
    shortcut = 'Ctrl+O'
    statustip = 'Open a workspace'

    def __init__(self):
        '''
        Constructor
        '''
        QObject.__init__(self)

    def execute(self):
        workspaceDir = QFileDialog.getExistingDirectory(caption='Open Workspace', options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
        if len(workspaceDir) > 0:
            m = Manager()
            m.load(workspaceDir)


class WorkspaceNewWorkspaceMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

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
        QObject.__init__(self)

    def execute(self, parent=None):
        workspaceDir = QFileDialog.getExistingDirectory(caption='Select Workspace Directory')
        if len(workspaceDir) > 0:
            m = Manager()
            m.new(workspaceDir)

class WorkspaceNewWorkstepMenu(PluginFramework.MenuOption):
    '''
    classdocs
    '''

    menuLabel = '&File'
    menuName = 'menu_File'
    subMenuLabel = '&New'
    subMenuName = 'menu_New'
    actionLabel = '&Workstep'
    #shortcut = 'Ctrl+N'
    statustip = 'Create a new workstep'

    def __init__(self):
        '''
        Constructor
        '''
        QObject.__init__(self)

    def execute(self, parent=None):
        print('sonugfff')



