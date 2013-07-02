#!/usr/bin/python
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

def suite():
    tests = unittest.TestSuite()

    from settings_tests import settingstests
    tests.addTests(settingstests.suite())

    from widgets_tests import widgetstests
    tests.addTests(widgetstests.suite())

    from core_tests import coretests
    tests.addTests(coretests.suite())

    from imagesourcestep_tests import imagesourcesteptests
    tests.addTests(imagesourcesteptests.suite())
    
    from pointcloudserializerstep_tests import pointcloudserializertests
    tests.addTests(pointcloudserializertests.suite())
    
    return tests

def load_tests(loader, tests, pattern):
    return suite()


if __name__ == '__main__':
    #unittest.main()
    unittest.TextTestRunner().run(suite())
