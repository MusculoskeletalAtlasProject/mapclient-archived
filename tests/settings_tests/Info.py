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

from settings import Info

class InfoTestCase(unittest.TestCase):


    def testABOUT(self):
        assert(len(Info.ABOUT.keys()) == 4)
        assert('name' in Info.ABOUT)
        assert('version' in Info.ABOUT)
        assert('license' in Info.ABOUT)
        assert('description' in Info.ABOUT)
        
    def testCREDITS(self):
        assert(len(Info.CREDITS.keys()) == 3)
        assert('programming' in Info.CREDITS)
        assert('artwork' in Info.CREDITS)
        assert('documentation' in Info.CREDITS)
        for contributor in Info.CREDITS['programming']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)
        for contributor in Info.CREDITS['artwork']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)
        for contributor in Info.CREDITS['documentation']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInfo']
    unittest.main()
