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

from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QSettings, QSize, QPoint

from widgets.MainWindowUi import Ui_MainWindow
from core import PluginFramework
from core.PluginFramework import PluginsAt, MenuOption

class MainWindow(QMainWindow):
    '''
    This is the main window for the MAP Client.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        QMainWindow.__init__(self)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.makeConnections()
        self._readSettings()
        #print(PluginsAt(PluginFramework.MenuOption))
        #print(PluginsAt(PluginFramework.MenuOption).__get__(self))
        
        self.menuPlugins = MenuOption.getPlugins()
        for plugin in self.menuPlugins:
            pluginAction = QtGui.QAction(plugin.actionLabel, plugin)
            pluginAction.triggered.connect(plugin.execute)
            
            pluginMenu = self.ui.menubar.addMenu(plugin.label)
            pluginMenu.addAction(pluginAction)
        
    def _writeSettings(self):
        settings = QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
    
    def _readSettings(self):
        settings = QSettings()
        settings.beginGroup('MainWindow')
        self.resize(settings.value('size', QSize(600, 400)))
        self.move(settings.value('pos', QPoint(100, 100)))
        settings.endGroup()
        
    def makeConnections(self):
        self.ui.action_Quit.triggered.connect(self.quitApplication)
        self.ui.action_About.triggered.connect(self.about)
        
    def closeEvent(self, event):
        self.quitApplication()
        
    def quitApplication(self):
        self._writeSettings()
        QtGui.qApp.quit()
        
    def about(self):
        from widgets.AboutDialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()
        
    def thisOne(self):
        print('here I am')
        