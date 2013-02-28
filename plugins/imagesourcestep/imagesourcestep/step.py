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

from PyQt4 import QtGui

from mountpoints.workspacestep import WorkspaceStepMountPoint
from imagesourcestep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState

class ImageSourceStep(WorkspaceStepMountPoint):
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
        self._pixmap = QtGui.QPixmap(':/imagesource/icons/landscapeimages.png')
        self.addPort(('pho#workspace#port', 'provides', 'images'))
        self._configured = False
        self._state = ConfigureDialogState()

    def configure(self, location):
        d = ConfigureDialog(self._state)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            step_location = os.path.join(location, self._state.identifier())
            if not step_location:
                os.mkdir(step_location)
        
        self._configured = d.validate()
