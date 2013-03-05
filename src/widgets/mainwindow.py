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

from PyQt4 import QtCore, QtGui

from widgets.ui_mainwindow import Ui_MainWindow
from mountpoints.stackedwidget import StackedWidgetMountPoint
from core.undomanager import UndoManager
from core.workspace import WorkspaceManager

class MainWindow(QtGui.QMainWindow):
    '''
    This is the main window for the MAP Client.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._makeConnections()
        self.undoManager = UndoManager()

#        undoManager = self.mainWindow.workspaceManager.undoManager
        undoAction = self.undoManager.createUndoAction(self._ui.menu_Edit)
        undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        redoAction = self.undoManager.createRedoAction(self._ui.menu_Edit)
        redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))

        self._ui.menu_Edit.addAction(undoAction)
        self._ui.menu_Edit.addAction(redoAction)

        self._ui.stackedWidget.currentChanged.connect(self.centralWidgetChanged)
        self.stackedWidgetPages = StackedWidgetMountPoint.getPlugins(self)
        self.stackedWidgetPages.insert(0, WorkspaceManager(self))

        for stackedWidgetPage in self.stackedWidgetPages:
            if not hasattr(self, stackedWidgetPage.name):
                setattr(self, stackedWidgetPage.name, stackedWidgetPage)
                stackedWidgetPage.setWidgetIndex(self._ui.stackedWidget.addWidget(stackedWidgetPage.getWidget()))

        self._readSettings()


    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        for stackedWidgetPage in self.stackedWidgetPages:
            stackedWidgetPage.writeSettings(settings)

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.resize(settings.value('size', QtCore.QSize(600, 400)))
        self.move(settings.value('pos', QtCore.QPoint(100, 100)))
        settings.endGroup()
        for stackedWidgetPage in self.stackedWidgetPages:
            stackedWidgetPage.readSettings(settings)

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        self._ui.action_About.triggered.connect(self.about)

    def setUndoStack(self, stack):
        self.undoManager.setCurrentStack(stack)

    def centralWidgetChanged(self, index):
        widget = self._ui.stackedWidget.currentWidget()
        widget.setActive()

    def closeEvent(self, event):
        self.quitApplication()

    def quitApplication(self):
        self._writeSettings()
        QtGui.qApp.quit()

    def about(self):
        from widgets.aboutdialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()
