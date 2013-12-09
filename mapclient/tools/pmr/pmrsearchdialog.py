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
import webbrowser

from PySide import QtGui, QtCore

from mapclient.settings import info
from mapclient.tools.annotation.annotationtool import AnnotationTool
from mapclient.tools.pmr.core import TokenHelper
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.pmrtool import PMRToolError
from mapclient.tools.pmr.oauthcheckdialog import OAuthCheckDialog
from mapclient.tools.pmr.ui_pmrsearchdialog import Ui_PMRSearchDialog

from mapclient.widgets.utils import set_wait_cursor


class PMRSearchDialog(QtGui.QDialog):
    '''
    Dialog for managing interaction with PMR.
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self._ui = Ui_PMRSearchDialog()
        self._ui.setupUi(self)
        
        self._pmrTool = PMRTool()
        self._annotationTool = AnnotationTool()
        
        self._makeConnections()
        
        self._updateUi()
        
    def _updateUi(self):
        if self._pmrTool.hasAccess():
            self._ui.loginStackedWidget.setCurrentIndex(1)
        else:
            self._ui.loginStackedWidget.setCurrentIndex(0)
            
    def _makeConnections(self):
        self._ui.searchButton.clicked.connect(self._searchClicked)
        self._ui.registerLabel.linkActivated.connect(self.register)
        self._ui.deregisterLabel.linkActivated.connect(self.deregister)
        
    def _searchClicked(self):
        # Set pmrlib to go
        self._ui.searchResultsListWidget.clear()
        
        # fix up known terms to be full blown uri
        search_text = self._ui.searchLineEdit.text()
        search_terms = search_text.split()
        for term in search_terms:
            rdfterm = self._annotationTool.rdfFormOfTerm(term)
            if rdfterm:
                search_text = search_text + ' ' + rdfterm[1:-1]

        results = []

        try:
            results = set_wait_cursor(self._pmrTool.search)(search_text)
        except PMRToolError as e:
            QtGui.QMessageBox.critical(self, e.title, e.description)

        for r in results:
            if 'title' in r and r['title']:
                item = QtGui.QListWidgetItem(r['title'], self._ui.searchResultsListWidget)
            else:
                item = QtGui.QListWidgetItem(r['target'], self._ui.searchResultsListWidget)
            item.setData(QtCore.Qt.UserRole, r)
        
    def getSelectedWorkspace(self):
        items = self._ui.searchResultsListWidget.selectedItems()
        for item in items:
            return item.data(QtCore.Qt.UserRole)
        
    def register(self, link):
        if link != 'mapclient.register':
            return

        dlg = OAuthCheckDialog(self)
        dlg.setModal(True)
        dlg.exec_()
                        
        self._updateUi()
        
    def deregister(self):
        pmr_info = info.PMRInfo()
        pmr_info.update_token(None, None)
        self._updateUi()
