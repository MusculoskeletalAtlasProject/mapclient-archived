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

class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

import unittest

class UnitTestOutputTestCase(unittest.TestCase):

    def test1(self):
        [p, f] = parseUnitTestOutput('py1.log')
        assert(p == 9)
        assert(f == 0)

    def test2(self):
        [p, f] = parseUnitTestOutput('py2.log')
        assert(p == 8)
        assert(f == 1)

    def test3(self):
        [p, f] = parseUnitTestOutput('py3.log')
        assert(p == 12)
        assert(f == 2)

    def test4(self):
        [p, f] = parseUnitTestOutput('py4.log')
        assert(p == 13)
        assert(f == 1)
        
    def test5(self):
        [p, f] = parseUnitTestOutput('py5.log')
        self.assertEqual(p, 21)
        self.assertEqual(f, 0)
      

import re

def parseUnitTestOutput(filename):
    '''
    Function for parsing unittest output for gathering pass and fail counts. 
    '''
    f = open(filename)
    lines = f.readlines()

    lines.reverse()
    if len(lines) >= 3:
        statusLine = lines[0].rstrip('\r\n')
        totalLine = lines[2].rstrip('\r\n')

        m = re.match('Ran (\d+)', totalLine)
        total = int(m.group(1))
        if statusLine.startswith('OK'):
            passed = total
            failed = 0
        else:
            errorDesc = ['failures', 'errors']
            failed = 0
            for errorType in errorDesc:
                m = re.match('.*{0}=(\d+)'.format(errorType), statusLine)
                if m:
                    failed += int(m.group(1))

            passed = total - failed
    else:
        passed = 0
        failed = 0

    return passed, failed

def suite():
    tests = unittest.TestSuite()
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTestOutputTestCase))
    return tests

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
