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
#from PyQt4 import QtCore

TEST_WORKSPACE_DIR_NAME = '/new_workspace_jihuuui'

class FakeWidget(object):

    def loadState(self, ws):
        pass

    def saveState(self, ws):
        pass

class FakeMainWindow(object):

    def setWindowTitle(self, value):
        pass

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
            ws = Manager(FakeMainWindow())
            ws.new(dirName)
            assert(os.path.exists(dirName + '/workspace.conf'))
        finally:
            os.remove(dirName + '/workspace.conf')
            os.rmdir(dirName)

    def testNewWithNone(self):
        from workspace.Workspace import Manager, WorkspaceError
        ws = Manager(FakeMainWindow())
        try:
            ws.new(None)
        except WorkspaceError:
            pass

    def testNewWithNonexistentDir(self):
        from workspace.Workspace import Manager
        tempDir = tempfile.gettempdir() + TEST_WORKSPACE_DIR_NAME
        ws = Manager(FakeMainWindow())
        ws.new(tempDir)
        assert(os.path.exists(tempDir + '/workspace.conf'))

        # Get rid of test  output
        os.remove(tempDir + '/workspace.conf')
        os.rmdir(tempDir)

    def testSave(self):
        from workspace.Workspace import Manager
        tempDir = tempfile.gettempdir() + TEST_WORKSPACE_DIR_NAME
        ws = Manager(FakeMainWindow())
        ws.widget = FakeWidget()
        ws.new(tempDir)
        ws.save()

    def testOpen(self):
        from workspace.Workspace import Manager
        tempDir = tempfile.gettempdir() + TEST_WORKSPACE_DIR_NAME
        ws = Manager(FakeMainWindow())
        ws.widget = FakeWidget()
        ws.new(tempDir)
        ws.load(tempDir)

        # Get rid of test  output
        os.remove(tempDir + '/workspace.conf')
        os.rmdir(tempDir)

    def testPort(self):
        from workspace.WorkspaceStep import WorkspaceStepPort
        port = WorkspaceStepPort()
        port.addProperty(('pho#workspace#port', 'uses', 'images'))
        self.assertIn('pho#workspace#port', port.subj)


    def testPortConnect(self):
        from workspace.WorkspaceStep import WorkspaceStepPort
        portIn = WorkspaceStepPort()
        portIn.addProperty(('pho#workspace#port', 'uses', 'images'))
        portOut = WorkspaceStepPort()
        portOut.addProperty(('pho#workspace#port', 'provides', 'images'))
        port2 = WorkspaceStepPort()
        port2.addProperty(('pho#workspace#port', 'uses', 'dicom'))

        self.assertEqual(portOut.canConnect(portIn), True)
        self.assertEqual(portOut.canConnect(port2), False)

    def testPortDescription(self):
        from workspace.WorkspaceStep import WorkspaceStepPort
        port = WorkspaceStepPort()
        port.addProperty(('pho#workspace#port', 'uses', 'images'))
        port.addProperty(('pho#workspace#port', 'provides', 'pointcloud'))
        port.addProperty(('pho#workspace#port', 'uses', 'dicom'))

        objs = port.getTriplesForObj('images')
        self.assertIn('images', objs[0])
#        self.assertIn('dicom', objs)
#        self.assertIn('pointcloud', objs)

    def testPortPredicates(self):
        from workspace.WorkspaceStep import WorkspaceStepPort
        port = WorkspaceStepPort()
        port.addProperty(('pho#workspace#port', 'uses', 'images'))
        port.addProperty(('pho#workspace#port', 'provides', 'pointcloud'))
        port.addProperty(('pho#workspace#port', 'uses', 'dicom'))

        preds = port.getTriplesForPred('uses')
        self.assertIn(('pho#workspace#port', 'uses', 'images'), preds)
        self.assertNotIn(('pho#workspace#port', 'provides', 'pointcloud'), preds)
        preds = port.getTriplesForPred('nope')
        self.assert_(len(preds) == 0)

    def testStepConnection(self):
        from workspace.WorkspaceStep import WorkspaceStep
        step1 = WorkspaceStep()
        step1.addPort(('pho#workspace#port', 'provides', 'images'))
        step2 = WorkspaceStep()
        step2.addPort(('pho#workspace#port', 'uses', 'images'))
        step2.addPort(('pho#workspace#port', 'uses', 'dicom'))
        step2.addPort(('pho#workspace#port', 'provides', 'pointcloud'))

        self.assertEqual(step1.canConnect(step2), True)

    def testWorkspaceStepFactory(self):
        import sys
        from PyQt4 import QtCore
        app = QtCore.QCoreApplication(sys.argv)
        from segmentation.SegmentationStep import Step
        from workspace.WorkspaceStep import WorkspaceStepFactory
        self.assertEqual(WorkspaceStepFactory('Segmentation').name, 'Segmentation')
        self.assertRaises(ValueError, WorkspaceStepFactory, ('james'))
        app.argc()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()
