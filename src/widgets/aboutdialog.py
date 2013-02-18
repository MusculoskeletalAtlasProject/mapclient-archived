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
from PyQt4.QtGui import QDialog
from widgets.AboutDialogUi import Ui_AboutDialog
class AboutDialog(QDialog):
    '''
    About dialog to display program about information.
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.makeConnections()
        
    def makeConnections(self):
        self.ui.btn_Credits.clicked.connect(self.showCreditsDialog)
        self.ui.btn_License.clicked.connect(self.showLicenseDialog)
        
    def showCreditsDialog(self):
        from widgets.CreditsDialog import CreditsDialog
        dlg = CreditsDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def showLicenseDialog(self):
        from widgets.LicenseDialog import LicenseDialog
        dlg = LicenseDialog(self)
        dlg.setModal(True)
        dlg.exec_()

