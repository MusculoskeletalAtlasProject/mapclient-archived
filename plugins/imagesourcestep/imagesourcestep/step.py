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

from PySide import QtGui, QtCore

from mountpoints.workflowstep import WorkflowStepMountPoint
from imagesourcestep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState

from core.threadcommandmanager import ThreadCommandManager, CommandCopyDirectory, CommandCloneWorkspace
from tools.pmr.pmrtool import PMRTool
from tools.pmr.pmrhglogindialog import PMRHgLoginDialog

STEP_SERIALISATION_FILENAME = 'step.conf'

class ImageSourceData(object):
    def __init__(self, identifier, location, imageType):
        self._identifier = identifier
        self._location = location
        self._imageType = imageType
        
    def identifier(self):
        return self._identifier
    
    def location(self):
        return self._location
    
    def imageType(self):
        return self._imageType
    

class ImageSourceStep(WorkflowStepMountPoint):
    '''
    A step that satisfies the step plugin duck.
    
    It describes the location of an image/a set of images.
    It can be used as an image source.
    '''
    def __init__(self, location):
        '''
        Constructor
        '''
        super(ImageSourceStep, self).__init__('Image source', location)
#        self._location = location
#        self._name = 'Image source'
        self._icon = QtGui.QImage(':/imagesource/icons/landscapeimages.png')
        self.addPort(('pho#workflow#port', 'provides', 'images'))
        self._configured = False
        self._state = ConfigureDialogState()
        self._threadCommandManager = ThreadCommandManager()
        self._threadCommandManager.registerFinishedCallback(self._threadCommandsFinished)

    def configure(self):
        delay = False
        d = ConfigureDialog(self._state)
        d.setModal(True)
        if d.exec_():
            self.serialize(self._location)
            step_location = os.path.join(self._location, self._state.identifier())
            if d.copyToWorkflow():
                src_location = d.localLocation()
                if src_location != step_location:
                    delay = True
                    c = CommandCopyDirectory(src_location, step_location)
                    self._threadCommandManager.addCommand(c)
            if d.addToPMR():
                pmr_tool = PMRTool()
                # Get login details:
                dlg = PMRHgLoginDialog()
                if dlg.exec_():
                    repourl = pmr_tool.addWorkspace('Image Source Step: ' + self._state.identifier(), None)
                    c = CommandCloneWorkspace(repourl, step_location, dlg.username(), dlg.password())
                    self._threadCommandManager.addCommand(c)
                    delay= True
            
            self._state = d.getState()
        
        self._configured = d.validate()

        if self._configured and delay:
            self._threadCommandManager.execute()
        elif self._configured and self._configuredObserver != None:
            self._configuredObserver()
            
    def _threadCommandsFinished(self):
        self._state._localLocation = os.path.join(self._location, self._state.identifier())
        if self._configured and self._configuredObserver != None:
            self._configuredObserver()
            
    def getIdentifier(self):
        return self._state.identifier()
    
    def setIdentifier(self, identifier):
        self._state.setIdentifier(identifier)
        
    def serialize(self, location):
        step_location = os.path.join(location, self._state.identifier())
        if not os.path.exists(step_location):
            os.mkdir(step_location)
            
        s = QtCore.QSettings(os.path.join(step_location, STEP_SERIALISATION_FILENAME), QtCore.QSettings.IniFormat)
        self._state.save(s)
        
    def deserialize(self, location):
        step_location = os.path.join(location, self._state.identifier())
        s = QtCore.QSettings(os.path.join(step_location, STEP_SERIALISATION_FILENAME), QtCore.QSettings.IniFormat)
        self._state.load(s)
        d = ConfigureDialog(self._state)
        self._configured = d.validate()
        
    def portOutput(self):
        return ImageSourceData(self._state.identifier(), self._state.location(), self._state.imageType())
