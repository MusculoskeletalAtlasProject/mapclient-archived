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
from mountpoints.workflowstep import WorkflowStepMountPoint

class SegmentationStep(WorkflowStepMountPoint):
    '''
    A step that acts like the step plugin duck
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(SegmentationStep, self).__init__()
        self._name = 'Segmentation'
        self._identifier = ''
        self._icon = QtGui.QImage(':/segmentation/icons/seg.gif')
        self.addPort(('pho#workflow#port', 'uses', 'images'))
        self.addPort(('pho#workflow#port', 'provides', 'pointcloud'))

    def configure(self):
        self._configured = True
        if self._configured and self._configuredObserver != None:
            self._configuredObserver()

    def getIdentifier(self):
        return self._identifier
    
    def setIdentifier(self, identifier):
        self._identifier = identifier
        
    def serialize(self, location):
        pass #QtCore.QSettings(location + '/' + info.WORKFLOW_NAME, QtCore.QSettings.IniFormat)
        
    def deserialize(self, location):
        pass
    
