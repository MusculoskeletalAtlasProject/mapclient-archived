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

from core.workflow import WorkflowManager, WorkflowError
from mountpoints.workflowstep import WorkflowStepPort, WorkflowStepMountPoint

class WorkflowStep(WorkflowStepMountPoint):
    pass

#from mpl_toolkits.axes_grid1.axes_grid import im
#from PyQt4 import QtCore

TEST_WORKFLOW_DIR_NAME = '/new_workflow_jihuuui'

#class FakeWidget(object):
#
#    def loadState(self, wf):
#        pass
#
#    def saveState(self, wf):
#        pass
#
#class FakeMainWindow(object):
#
#    def setWindowTitle(self, value):
#        pass

class WorkflowTestCase(unittest.TestCase):


    def assertIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" in "b"'''
        try:
            f = super(WorkflowTestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertNotIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" NOT in "b"'''
        try:
            f = super(WorkflowTestCase, self).assertNotIn
        except AttributeError:
            self.assertFalse(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def testNew(self):
        dirName = tempfile.mkdtemp(prefix='new_workflow_')
        try:
            wf = WorkflowManager()
            wf.new(dirName)
            assert(os.path.exists(dirName + '/workflow.conf'))
        finally:
            os.remove(dirName + '/workflow.conf')
            os.rmdir(dirName)

    def testNewWithNone(self):
        wf = WorkflowManager()
        self.assertRaises(WorkflowError, wf.new, None)

    def testNewWithNonexistentDir(self):
        tempDir = tempfile.gettempdir() + TEST_WORKFLOW_DIR_NAME
        wf = WorkflowManager()
        wf.new(tempDir)
        assert(os.path.exists(tempDir + '/workflow.conf'))

        # Get rid of test  output
        os.remove(tempDir + '/workflow.conf')
        os.rmdir(tempDir)

    def testSave(self):
        tempDir = tempfile.gettempdir() + TEST_WORKFLOW_DIR_NAME
        print(tempDir)
        wf = WorkflowManager()
#        wf.widget = FakeWidget()
        wf.new(tempDir)
        wf.save()

    def testOpen(self):
        tempDir = tempfile.gettempdir() + TEST_WORKFLOW_DIR_NAME
        wf = WorkflowManager()
#        wf.widget = FakeWidget()
        wf.new(tempDir)
        wf.load(tempDir)

        # Get rid of test  output
        os.remove(tempDir + '/workflow.conf')
        os.rmdir(tempDir)
        
    def testLocation(self):
        wf = Workflow

    def testPort(self):
        port = WorkflowStepPort()
        port.addProperty(('pho#workflow#port', 'uses', 'images'))
        self.assertIn('pho#workflow#port', port.subj)


    def testPortConnect(self):
        portIn = WorkflowStepPort()
        portIn.addProperty(('pho#workflow#port', 'uses', 'images'))
        portOut = WorkflowStepPort()
        portOut.addProperty(('pho#workflow#port', 'provides', 'images'))
        port2 = WorkflowStepPort()
        port2.addProperty(('pho#workflow#port', 'uses', 'dicom'))

        self.assertEqual(portOut.canConnect(portIn), True)
        self.assertEqual(portOut.canConnect(port2), False)

    def testPortDescription(self):
        port = WorkflowStepPort()
        port.addProperty(('pho#workflow#port', 'uses', 'images'))
        port.addProperty(('pho#workflow#port', 'provides', 'pointcloud'))
        port.addProperty(('pho#workflow#port', 'uses', 'dicom'))

        objs = port.getTriplesForObj('images')
        self.assertIn('images', objs[0])
#        self.assertIn('dicom', objs)
#        self.assertIn('pointcloud', objs)

    def testPortPredicates(self):
        port = WorkflowStepPort()
        port.addProperty(('pho#workflow#port', 'uses', 'images'))
        port.addProperty(('pho#workflow#port', 'provides', 'pointcloud'))
        port.addProperty(('pho#workflow#port', 'uses', 'dicom'))

        preds = port.getTriplesForPred('uses')
        self.assertIn(('pho#workflow#port', 'uses', 'images'), preds)
        self.assertNotIn(('pho#workflow#port', 'provides', 'pointcloud'), preds)
        preds = port.getTriplesForPred('nope')
        self.assertEqual(0, len(preds))

    def testStepConnection(self):
        step1 = WorkflowStep()
        step1.addPort(('pho#workflow#port', 'provides', 'images'))
        step2 = WorkflowStep()
        step2.addPort(('pho#workflow#port', 'uses', 'images'))
        step2.addPort(('pho#workflow#port', 'uses', 'dicom'))
        step2.addPort(('pho#workflow#port', 'provides', 'pointcloud'))

        self.assertEqual(step1.canConnect(step2), True)

    def testWorkflowStepFactory(self):
        import sys
        # If on a posix system with no display set we are probably testing headless
        # and cannot do QPixmap
        if os.name == 'posix' and 'DISPLAY' not in os.environ:
            return
        from PyQt4 import QtGui
        app = QtGui.QApplication(sys.argv)
        #from segmentation_plugin.segmentationstep import Step
        from mountpoints.workflowstep import workflowStepFactory
        self.assertEqual(workflowStepFactory('Segmentation').getName(), 'Segmentation')
        self.assertRaises(ValueError, workflowStepFactory, ('james'))
        app.argc()
        #Step()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()
