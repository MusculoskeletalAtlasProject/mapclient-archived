
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

from PyQt4.QtGui import QDialog, QDialogButtonBox

from imagesourcestep.widgets.ui_configuredialog import Ui_ConfigureDialog

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'

class ConfigureDialogState(object):
    
    def __init__(self, identifier='', localLocation='', copyTo=False, pmrLocation='', imageType=0):
        self._identifier = identifier
        self._localLocation = localLocation
        self._copyTo = copyTo
        self._pmrLocation = pmrLocation
        self._imageType = imageType
        
    def location(self):
        if self._localLocation:
            return self._localLocation
        
        return self._pmrLocation
    
    def identifier(self):
        return self._identifier
    
    def copyTo(self):
        return self._copyTo
    
    def imageType(self):
        return self._imageType
        
        
class ConfigureDialog(QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''


    def __init__(self, state, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
        self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)
        
        self.setState(state)
        self.validate()
        self._makeConnections()
        
    def _makeConnections(self):
        self._ui.identifierLineEdit.textChanged.connect(self.validate)
        self._ui.localLineEdit.textChanged.connect(self._localLocationEdited)
        self._ui.pmrLineEdit.textChanged.connect(self._pmrLocationEdited)
        
    def setState(self, state):
        self._ui.identifierLineEdit.setText(state._identifier)
        self._ui.localLineEdit.setText(state._localLocation)
        self._ui.copyToWorkspaceCheckBox.setChecked(state._copyTo)
        self._ui.pmrLineEdit.setText(state._pmrLocation)
        self._ui.imageSourceTypeComboBox.setCurrentIndex(state._imageType)
    
    def getState(self):
        state = ConfigureDialogState(
            self._ui.identifierLineEdit.text(),
            self._ui.localLineEdit.text(),
            self._ui.copyToWorkspaceCheckBox.isChecked(),
            self._ui.pmrLineEdit.text(),
            self._ui.imageSourceTypeComboBox.currentIndex())
        
        return state
    
    def _pmrLocationEdited(self):
        self._ui.localLineEdit.setText('')
        self.validate()
        
    def _localLocationEdited(self):
        self._ui.pmrLineEdit.setText('')
        self.validate()
        
    def validate(self):
        identifierValid = len(self._ui.identifierLineEdit.text()) > 0
        localValid = len(self._ui.localLineEdit.text()) > 0
        pmrValid = len(self._ui.pmrLineEdit.text()) > 0
        locationValid = localValid or pmrValid
        valid = identifierValid and locationValid
            
        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

        if identifierValid:
            self._ui.identifierLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        if localValid:
            self._ui.localLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.localLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)
            
        if pmrValid:
            self._ui.pmrLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.pmrLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)
            
        return valid
                
        
