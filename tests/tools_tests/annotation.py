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
import re

from tools.annotation.annotationtool import AnnotationTool, SECTION_HEADER_RE

class AnnotationToolTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testReadVocab(self):
        a =  AnnotationTool()
        a._readVocabulary()
        
        self.assertEqual(8, len(a._vocab._terms))
        self.assertEqual('1.0', a._vocab._version)
        self.assertEqual('http://physiomeproject.org/mapclient', a._vocab._namespace)
        
    def testSectionHeaderRe(self):
        s = re.compile(SECTION_HEADER_RE)
        
        test_1 = '[hello]'
        r = s.match(test_1)
        self.assertEqual('hello', r.group(1))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()