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
from PySide import QtGui

import widgets.resources_rc
from widgets.utils import _checkExtent, createDefaultImageIcon

if QtGui.qApp == None: QtGui.QApplication([])

class UtilsTestCase(unittest.TestCase):


    def testExtentA(self):
        name = 'A'
        image = QtGui.QImage(':/workflow/images/default_step_icon.png')
        p = QtGui.QPainter(image)
        result = _checkExtent(p, image.size(), name)
        self.assertFalse(result)
#         p.end()


    def testExtentB(self):
        name = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
        image = QtGui.QImage(':/workflow/images/default_step_icon.png')
        p = QtGui.QPainter(image)
        result = _checkExtent(p, image.size(), name)
        self.assertFalse(result)


    def testIncreaseA(self):
        name = 'AAAA'
        image = QtGui.QImage(':/workflow/images/default_step_icon.png')
        p = QtGui.QPainter(image)
        f = p.font()
        point_size = f.pointSize()
        count = 1
        while not _checkExtent(p, image.size(), name) and count < 500:
            p.begin(image)
            point_size += 1
            count += 1
            f = p.font()
            f.setPointSize(point_size)
            p.setFont(f)
            print(f.pointSize())

        p.begin(image)
        f = p.font()
        f.setPointSize(point_size)
        p.setFont(f)
        self.assertTrue(_checkExtent(p, image.size(), name))

#         p.end()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
