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
import sys, unittest
from core.PluginFramework import loadPlugins
from Utils import ConsumeOutput
    
class PluginFrameworkTestCase(unittest.TestCase):

    def testLoadPlugins(self):
        old_stdout = sys.stdout
        sys.stdout = redirectStdout = ConsumeOutput()
        loadPlugins()
        sys.stdout = old_stdout
        #print(redirectStdout.messages)
        assert(redirectStdout.messages[0] == "Plugin 'WokspaceMenu' ver -.-.- by ? loaded")
        assert(redirectStdout.messages[2] == "Plugin 'CoolMenu' ver -.-.- by ? loaded")
        #print(redirectStdout.messages[0])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLoadPlugins']
    unittest.main()