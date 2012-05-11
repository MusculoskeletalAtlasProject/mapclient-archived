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
import unittest
import os, tempfile
from workspace.Workspace import Manager, WorkspaceError

TEST_WORKSPACE_DIR_NAME = '/tmp/new_workspace_jihuuui'

class WorkspaceTestCase(unittest.TestCase):


    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testNew(self):
        dirName = tempfile.mkdtemp(prefix='new_workspace_')
        try:
            ws = Manager()
            ws.new(dirName)
            assert(os.path.exists(dirName + '/workspace.conf'))
        finally:
            os.remove(dirName + '/workspace.conf')
            os.rmdir(dirName)
        
    def testNewWithNone(self):
        ws = Manager()
        try:
            ws.new(None)
        except WorkspaceError:
            pass
        
    def testNewWithNonexistentDir(self):
        ws = Manager()
        ws.new(TEST_WORKSPACE_DIR_NAME)
        assert(os.path.exists(TEST_WORKSPACE_DIR_NAME + '/workspace.conf'))

        # Get rid of test  output
        os.remove(TEST_WORKSPACE_DIR_NAME + '/workspace.conf')
        os.rmdir(TEST_WORKSPACE_DIR_NAME)
        
    def testOpen(self):
        ws = Manager()
        ws.new(TEST_WORKSPACE_DIR_NAME)
        ws.load(TEST_WORKSPACE_DIR_NAME)

        # Get rid of test  output
        os.remove(TEST_WORKSPACE_DIR_NAME + '/workspace.conf')
        os.rmdir(TEST_WORKSPACE_DIR_NAME)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()