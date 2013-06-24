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
import unittest, sys

from PySide import QtGui

from settings import info

DISABLE_GUI_TESTS = True

app = QtGui.QApplication('testpmr')
app.setOrganizationDomain(info.ORGANISATION_DOMAIN)
app.setOrganizationName(info.ORGANISATION_NAME)
app.setApplicationName(info.APPLICATION_NAME)
app.setApplicationVersion(info.ABOUT['version'])

class PMRSearchDialogTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    if sys.version < '2.7.0':
        @unittest.skipIf(DISABLE_GUI_TESTS, 'GUI tests are disabled')
        def testPMRSearchDialog(self):        
            from tools.pmr.pmrsearchdialog import PMRSearchDialog
            dlg = PMRSearchDialog()
            dlg.setModal(True)
            if dlg.exec_():
                ws = dlg.getSelectedWorkspace()
                print('the winner has selected:')
                print(ws)
            
class PMRToolTestCase(unittest.TestCase):
    
    def setUp(self):
        from tools.pmr.pmrtool import PMRTool
        self._tool = PMRTool()

    def tearDown(self):
        pass
#        del self._app

    if sys.version < '2.7.0':
        @unittest.skip('No need to create workspaces all the time.')
        def testAddWorkspace(self):
            location = self._tool.addWorkspace('my title', 'my description')
            self.assertTrue(location.startswith('http://'))
    
    def testGetDashboard(self):
        from tools.pmr.pmrtool import PMRTool
        t = PMRTool()
        d = t.getDashboard()
        
        self.assertTrue('workspace-home' in d)
        self.assertTrue('workspace-add' in d)
        
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
