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
import os, unittest
from PyQt4 import QtGui

class SegmentationTestCase(unittest.TestCase):


    def testPlugin(self):
        import sys
        # If on a posix system with no display set we are probably testing headless
        # and cannot do QPixmap
        if os.name == 'posix' and 'DISPLAY' not in os.environ:
            return
        app = QtGui.QApplication(sys.argv)
        #fileDir = os.path.dirname(__file__)
        #inbuiltPluginDir = os.path.realpath(fileDir + '/../../plugins')
#        loadPlugins(inbuiltPluginDir)

        #sys.path.insert(0, inbuiltPluginDir)
#        from workspace.Workspace import Manager
        from segmentationstep.step import Step
        myStep = Step()
        self.assertEqual(myStep._name, 'Segmentation')
        app.argc() # eclipse warning killer
        del sys.path[0]

#    def testSerialisation(self):
#        import sys
#        app = QtGui.QApplication(sys.argv)
#        from segmentation.SegmentationStep import Step
#        from workspace.WorkspaceStep import WorkspaceStep
#        myStep = Step()
#
#        itemData = QtCore.QByteArray()
#        writeDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
#
#        writeDataStream = myStep.serialize(writeDataStream)
#
#        readDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
#        passedStep = WorkspaceStep()
#        retStep = Step.deserialize(passedStep, readDataStream)
#        self.assertEqual(retStep.name, 'segmentation')
#        self.assertNotEqual(retStep.pixmap, None)
#        self.assertEqual(len(retStep.ports), 2)
#        app.argc() # eclipse warning killer


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
