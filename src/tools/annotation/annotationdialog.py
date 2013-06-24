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
from PySide import QtGui

from tools.annotation.ui_annotationdialog import Ui_AnnotationDialog
from tools.annotation.annotationtool import AnnotationTool

_DEFAULT_ANNOTATION_FILENAME = 'annotation.rdf'

class AnnotationDialog(QtGui.QDialog):
    '''
    Dialog for annotating a directory.
    '''


    def __init__(self, location, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_AnnotationDialog()
        self._ui.setupUi(self)
        
        self._ui.locationLineEdit.setText(location)
        self._tool = AnnotationTool()
        self._ui.subjectComboBox.addItems(self._tool.getTerms())
        self._ui.predicateComboBox.addItems(self._tool.getTerms())
        self._ui.objectComboBox.addItems(self._tool.getTerms())
        
#        self._ui
