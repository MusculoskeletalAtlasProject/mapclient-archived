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

from PyQt4 import QtGui, QtCore
from pmr2register import RegisterDialogUi

class RegisterDialog(QtGui.QDialog):
    '''
    Some quality documentation
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        self.previousCursor = None
        super(RegisterDialog, self).__init__(parent)
        self.ui = RegisterDialogUi.Ui_PMRRegistrationTool()
        self.ui.setupUi(self)
        self.ui.webView.loadStarted.connect(self.onLoadStart)
        self.ui.webView.loadFinished.connect(self.onLoadFinish)
        self.ui.webView.page().networkAccessManager().sslErrors.connect(self.onSSLError)
        self.ui.webView.load(QtCore.QUrl("https://bioeng1033.bioeng.auckland.ac.nz/pmr/register"))

    def onSSLError(self, nr, errors):
        ignoreError = False
        for error in errors:
            if error.errorString() == 'The certificate is self-signed, and untrusted':
                ignoreError = True

        if ignoreError:
            nr.ignoreSslErrors()

    def onLoadStart(self):
        print('onLoadStart')
        self.previousCursor = self.ui.webView.cursor()
        self.ui.webView.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def onLoadFinish(self):
        print('onLoadFinish')
        self.ui.webView.setCursor(self.previousCursor)
