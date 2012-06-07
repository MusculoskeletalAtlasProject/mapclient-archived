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
import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

import unittest
import os, tempfile
#from core.PluginFramework import loadPlugins

TEST_WORKSPACE_DIR_NAME = '/new_workspace_jihuuui'

class WorkspaceTestCase(unittest.TestCase):


    def setUp(self):
        pass
#        fileDir = os.path.dirname(__file__)
#        inbuiltPluginDir = os.path.realpath(fileDir + '/../../plugins')
#        
#        loadPlugins(inbuiltPluginDir)

    def tearDown(self):
        pass

    def testNew(self):
        from workspace.Workspace import Manager
        dirName = tempfile.mkdtemp(prefix='new_workspace_')
        try:
            ws = Manager()
            ws.new(dirName)
            assert(os.path.exists(dirName + '/workspace.conf'))
        finally:
            os.remove(dirName + '/workspace.conf')
            os.rmdir(dirName)

    def testNewWithNone(self):
        from workspace.Workspace import Manager, WorkspaceError
        ws = Manager()
        try:
            ws.new(None)
        except WorkspaceError:
            pass

    def testNewWithNonexistentDir(self):
        from workspace.Workspace import Manager
        tempDir = tempfile.gettempdir() + TEST_WORKSPACE_DIR_NAME
        ws = Manager()
        ws.new(tempDir)
        assert(os.path.exists(tempDir + '/workspace.conf'))

        # Get rid of test  output
        os.remove(tempDir + '/workspace.conf')
        os.rmdir(tempDir)

    def testOpen(self):
        from workspace.Workspace import Manager
        tempDir = tempfile.gettempdir() + TEST_WORKSPACE_DIR_NAME
        ws = Manager()
        ws.new(tempDir)
        ws.load(tempDir)

        # Get rid of test  output
        os.remove(tempDir + '/workspace.conf')
        os.rmdir(tempDir)

    def testDirection(self):
        from workspace.Workspace import Direction

        x = Direction.IN
        assert(x == Direction.IN)

    def testPort(self):
        from workspace.Workspace import WorkspaceStepPort, Direction
        port = WorkspaceStepPort(Direction.IN)
        assert(port.direction == Direction.IN)

    def testDummy(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()
