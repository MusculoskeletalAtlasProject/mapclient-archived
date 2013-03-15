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

from PyQt4 import QtGui, QtCore

from mountpoints.workflowstep import WorkflowStepMountPoint
from imagesourcestep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState

STEP_SERIALISATION_FILENAME = 'step.conf'

class ImageSourceStep(WorkflowStepMountPoint):
    '''
    A step satisfies the step plugin duck.
    
    It describes the location of an image/a set of images.
    It can be used as an image source.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(ImageSourceStep, self).__init__()
        self._name = 'Image source'
        self._icon = QtGui.QImage(':/imagesource/icons/landscapeimages.png')
        self.addPort(('pho#workflow#port', 'provides', 'images'))
        self._configured = False
        self._state = ConfigureDialogState()

    def configure(self, location):
        d = ConfigureDialog(self._state)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            step_location = os.path.join(location, self._state.identifier())
            if not os.path.exists(step_location):
                os.mkdir(step_location)
                
            self.serialize(step_location)
        
        self._configured = d.validate()
        
    def getIdentifier(self):
        return self._state.identifier()
    
    def setIdentifier(self, identifier):
        self._state.setIdentifier(identifier)
        
    def serialize(self, location):
        s = QtCore.QSettings(os.path.join(location, STEP_SERIALISATION_FILENAME), QtCore.QSettings.IniFormat)
        self._state.save(s)
        
    def deserialize(self, location):
        s = QtCore.QSettings(os.path.join(location, STEP_SERIALISATION_FILENAME), QtCore.QSettings.IniFormat)
        self._state.load(s)
        d = ConfigureDialog(self._state)
        self._configured = d.validate()
    
