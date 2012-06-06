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
import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

import os, sys, locale
from core.PluginFramework import loadPlugins
from settings import Info

# Ensure the MAP Client module directory is in the system path so relative 'import' statements work
base_path = os.path.dirname(os.path.abspath(__file__))
if sys.path.count(base_path) == 0:
    sys.path.insert(0, base_path)


def progheader():
    '''
    Display program header
    '''
    programHeader = '   MAP Client (version %s)   ' % Info.ABOUT['version']
    print('-' * len(programHeader))
    print(programHeader)
    print('-' * len(programHeader))

# This method starts MAP Client
def winmain():
    '''
    Initialise common settings and check the operating environment before starting the application.
    '''

    progheader()
    # import the locale, and set the locale. This is used for 
    # locale-aware number to string formatting
    locale.setlocale(locale.LC_ALL, '')

    from PyQt4 import QtGui, QtCore
    app = QtGui.QApplication(sys.argv)

    # Set the default organisation name and application name used to store application settings
    QtCore.QCoreApplication.setOrganizationName(Info.ORGANISATION_NAME)
    QtCore.QCoreApplication.setOrganizationDomain(Info.ORGANISATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationName(Info.APPLICATION_NAME)

    from PyQt4.QtCore import QSettings
    settings = QSettings()
    settings.beginGroup('Plugins')
    loadDefaultPlugins = settings.value('load_defaults', True)
    settings.endGroup()

    if loadDefaultPlugins:
        fileDir = os.path.dirname(os.path.abspath(__file__))
        inbuiltPluginDir = os.path.realpath(fileDir + '/../plugins')
        loadPlugins(inbuiltPluginDir)

    from widgets.MainWindow import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

def main():
#    progheader()
    locale.setlocale(locale.LC_ALL, '')

    from optparse import OptionParser
    from PyQt4 import QtCore
    app = QtCore.QCoreApplication(sys.argv)

    # Set the default organisation name and application name used to store application settings
    QtCore.QCoreApplication.setOrganizationName(Info.ORGANISATION_NAME)
    QtCore.QCoreApplication.setOrganizationDomain(Info.ORGANISATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationName(Info.APPLICATION_NAME)

    old_stdout = sys.stdout
    sys.stdout = redirectstdout = ConsumeOutput()
    progheader()
    sys.stdout = old_stdout
    versionstring = ''.join(redirectstdout.messages)

    progname = os.path.splitext(__file__)[0]
    usage = 'usage: {0} [options] workspace\n    Execute the given workspace'.format(progname)
    parser = OptionParser(usage, version=versionstring)
    options, args = parser.parse_args()

    print(sys.argv)
    print(options, args)

    # Possibly don't need to run app.exec_()
    sys.exit(app.quit())


if __name__ == '__main__':
    if len(sys.argv) == 1: # No command line args
        winmain()
    else:
        main()
