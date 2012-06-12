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
from PyQt4 import QtCore

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

    def testPortSerialization(self):
        from workspace.WorkspaceStep import WorkspaceStepPort
        myPort = WorkspaceStepPort()
        myPort.addProperty(('somesubj', 'somepred', 'someobj'))
        myPort.addProperty(('anothersubj', 'anotherpred', 'anotherobj'))
        itemData = QtCore.QByteArray()
        writeDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

        writeDataStream = myPort.serialize(writeDataStream)

        readDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
        passedPort = WorkspaceStepPort()
        retPort = WorkspaceStepPort.deserialize(passedPort, readDataStream)
        self.assertIn('somesubj', retPort.subj)
        self.assertIn('somepred', retPort.pred)
        self.assertIn('someobj', retPort.obj)
        self.assertIn('anothersubj', retPort.subj)

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
        from PyQt4 import QtGui
        app = QtGui.QApplication(sys.argv)
        from workspace.WorkspaceStep import WorkspaceStepFactory
        self.assertRaises(ValueError, WorkspaceStepFactory, ('james'))
        self.assertEqual(WorkspaceStepFactory('segmentation').name, 'segmentation')
        app.argc()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNew']
    unittest.main()
