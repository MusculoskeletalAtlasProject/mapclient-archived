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
import logging

from mapclient.core.mainapplication import PluginManager
from tests.utils import ConsumeOutput

def initialiseLogger():
    logging.basicConfig(format='%(asctime)s %(levelname)s - %(name)s--> %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level='DEBUG')
    logging.addLevelName(29, 'PLUGIN')

class PluginFrameworkTestCase(unittest.TestCase):


    def testLoadPlugins(self):

        initialiseLogger()

        redirectstdout = ConsumeOutput()
        root = logging.getLogger('mapclient.core.mainapplication')
        ch = logging.StreamHandler(redirectstdout)
        ch.setLevel(29)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
        root.propagate = False

        pm = PluginManager()

        pm.load()

        features = [True for msg in redirectstdout.messages if "Plugin 'pointcloudserializerstep' version 0.3.0 by Hugh Sorby loaded" in msg]
        self.assertEqual(1, len(features))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadPlugins']
    unittest.main()
