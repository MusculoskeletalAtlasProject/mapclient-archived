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
from PyQt4 import QtGui, QtCore

class SegmentationTestCase(unittest.TestCase):


    def testPlugin(self):
        import sys
        app = QtGui.QApplication(sys.argv)
        from segmentation.Step import Step
        myStep = Step()
        assert(myStep.description == 'This step is for segmenting images.')

    def testSerialisation(self):
        import sys
        app = QtGui.QApplication(sys.argv)
        from segmentation.Step import Step
        myStep = Step()

        itemData = QtCore.QByteArray()
        writeDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

        writeDataStream = myStep.serialize(writeDataStream)

        readDataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
        retStep = Step.deserialize(readDataStream)
        assert(retStep.description == 'This step is for segmenting images.')
        assert(retStep.name == 'segmentation')
        assert(retStep.icon)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
