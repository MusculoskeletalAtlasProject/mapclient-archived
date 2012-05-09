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
import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

import unittest

if __name__ == '__main__':
    tests = unittest.TestSuite()
    
    from settings_tests import SettingsTests
    tests.addTests(SettingsTests.suite())
    
    from widgets_tests import WidgetsTests
    tests.addTests(WidgetsTests.suite())
    
    from core_tests import CoreTests
    tests.addTests(CoreTests.suite())
    
    from workspace_tests import WorkspaceTests
    tests.addTests(WorkspaceTests.suite())

    unittest.TextTestRunner().run(tests)