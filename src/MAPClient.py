#!/usr/bin/env python
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

import os, sys, locale
# Ensure the MAP Client module directory is in the system path so relative 'import' statements work
base_path = os.path.dirname(os.path.abspath(__file__))
if sys.path.count(base_path) == 0:
    sys.path.insert(0, base_path)
    

# This method starts MAP Client
def main():
    '''
    Initialise common settings and check the operating environment before starting the application.
    '''

    from settings import Info
    print("--------------------------------")
    print("   MAP Client (version %s)" % Info.ABOUT['version'])
    print("--------------------------------")

    # import the locale, and set the locale. This is used for 
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')
    
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    from widgets.MainWindow import MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()
