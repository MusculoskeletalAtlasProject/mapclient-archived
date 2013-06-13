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

from core.workflow import WorkflowManager, WorkflowError, workflowConfigurationExists, getWorkflowConfigurationAbsoluteFilename


class WorkflowManagerTestCase(unittest.TestCase):


    def setUp(self):
        self.tempDir = tempfile.mkdtemp(prefix='new_workflow_')
        
    def tearDown(self):
        if os.path.exists(self.tempDir):
            if os.path.exists(getWorkflowConfigurationAbsoluteFilename(self.tempDir)):
                os.remove(getWorkflowConfigurationAbsoluteFilename(self.tempDir))
            os.rmdir(self.tempDir)

    def testNew(self):
        wf = WorkflowManager()
        wf.new(self.tempDir)
        self.assertTrue(workflowConfigurationExists(self.tempDir))

    def testNewWithNone(self):
        wf = WorkflowManager()
        self.assertRaises(WorkflowError, wf.new, None)

    def testNewWithNonexistentDir(self):
        wf = WorkflowManager()
        wf.new(self.tempDir)
        self.assertTrue(workflowConfigurationExists(self.tempDir))

    def testSave(self):
        wf = WorkflowManager()
#        wf.widget = FakeWidget()
        wf.new(self.tempDir)
        wf.save()
        self.assertTrue(workflowConfigurationExists(self.tempDir))

    def testOpen(self):
        wf = WorkflowManager()
#        wf.widget = FakeWidget()
        wf.new(self.tempDir)
        wf.load(self.tempDir)
        self.assertTrue(workflowConfigurationExists(self.tempDir))
        
    def testLocation(self):
        wf = WorkflowManager()
        self.assertTrue(wf.setLocation('here') == None)
        self.assertEqual(wf.location(), 'here')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()
