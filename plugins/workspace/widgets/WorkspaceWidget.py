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
from workspace.widgets.WorkspaceWidgetUi import Ui_WorkspaceWidget
from workspace.MountPoint import WorkspaceStepMountPoint

class WorkspaceWidget(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self)
        self.ui = Ui_WorkspaceWidget()
        self.ui.setupUi(self)
        self.workspaceStepPlugins = WorkspaceStepMountPoint.getPlugins()
        self.stepTree = self.findChild(QtGui.QWidget, "stepTree")
        for step in self.workspaceStepPlugins:
            if step.name != 'empty':
                self.stepTree.addStep(step)

