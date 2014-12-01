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
import sys

from PySide.QtGui import QDialog, QTableWidgetItem

from mapclient.widgets.ui_logdetails import Ui_LogDetails

class LogDetails(QDialog):
    '''
    Load details dialog to present the user with more detailed information about an individual recorded log.
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''        
        QDialog.__init__(self, parent)
        self._ui = Ui_LogDetails()
        self._ui.setupUi(self)
        
    def fillTable(self, information, time, current_log_file, parent=None):
        log_file = open(current_log_file, 'r')
        log_data = log_file.read()
        log_file.close()        
        logs = log_data.split('\n')
        logs = logs[:-1]
        self._ui.detailedTable.setRowCount(5)
        self._ui.detailedTable.setColumnCount(1)
        
        selectedLog = logs[0].split(' - ')
        for log in logs:
            log = log.split(' - ')
            if log[1] == time and log[4] == information:
                selectedLog = log
                
        row_number = 0
        for information in selectedLog:
            self._ui.detailedTable.setItem(row_number, 0, QTableWidgetItem(selectedLog[row_number]))
            row_number += 1
