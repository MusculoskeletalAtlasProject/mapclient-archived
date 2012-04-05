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

from settings import info

class Test(unittest.TestCase):


    def testABOUT(self):
        assert(len(info.ABOUT.keys()) == 4)
        assert(info.ABOUT.has_key('name'))
        assert(info.ABOUT.has_key('version'))
        assert(info.ABOUT.has_key('license'))
        assert(info.ABOUT.has_key('description'))
        
    def testCREDITS(self):
        assert(len(info.CREDITS.keys()) == 3)
        assert(info.CREDITS.has_key('programming'))
        assert(info.CREDITS.has_key('artwork'))
        assert(info.CREDITS.has_key('documentation'))
        for contributor in info.CREDITS['programming']:
            assert(len(contributor.keys()) == 2)
            assert(contributor.has_key('name'))
            assert(contributor.has_key('email'))
        for contributor in info.CREDITS['artwork']:
            assert(len(contributor.keys()) == 2)
            assert(contributor.has_key('name'))
            assert(contributor.has_key('email'))
        for contributor in info.CREDITS['documentation']:
            assert(len(contributor.keys()) == 2)
            assert(contributor.has_key('name'))
            assert(contributor.has_key('email'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInfo']
    unittest.main()
