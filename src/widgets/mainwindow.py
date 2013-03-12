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

from widgets.ui_mainwindow import Ui_MainWindow
from mountpoints.stackedwidget import StackedWidgetMountPoint
from widgets.workflowwidget import WorkflowWidget

class MainWindow(QtGui.QMainWindow):
    '''
    This is the main window for the MAP Client.
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)

        self._model = model
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._makeConnections()

#        undoManager = self.mainWindow.workflowManager.undoManager
        undoAction = self._createUndoAction(self._ui.menu_Edit)
        undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        redoAction = self._createRedoAction(self._ui.menu_Edit)
        redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))

        self._ui.menu_Edit.addAction(undoAction)
        self._ui.menu_Edit.addAction(redoAction)

        self._ui.stackedWidget.currentChanged.connect(self.centralWidgetChanged)
        self.stackedWidgetPages = StackedWidgetMountPoint.getPlugins(self)
        self.stackedWidgetPages.insert(0, WorkflowWidget(self))
        self._ui.stackedWidget.addWidget(self.stackedWidgetPages[0])

#        for stackedWidgetPage in self.stackedWidgetPages:
#            if not hasattr(self, stackedWidgetPage.name):
#                setattr(self, stackedWidgetPage.name, stackedWidgetPage)
#                stackedWidgetPage.setWidgetIndex(self._ui.stackedWidget.addWidget(stackedWidgetPage.getWidget()))

        self._model.readSettings()
        self.resize(self._model.size())
        self.move(self._model.pos())


    def _createUndoAction(self, parent):
        self.undoAction = QtGui.QAction('Undo', parent)
        self.undoAction.triggered.connect(self._model.undoManager().undo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.undoAction.setEnabled(stack.canUndo())
        else:
            self.undoAction.setEnabled(False)

        return self.undoAction

    def _createRedoAction(self, parent):
        self.redoAction = QtGui.QAction('Redo', parent)
        self.redoAction.triggered.connect(self._model.undoManager().redo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.redoAction.setEnabled(stack.canRedo())
        else:
            self.redoAction.setEnabled(False)

        return self.redoAction

    def model(self):
        return self._model
    
    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        self._ui.action_About.triggered.connect(self.about)

    def setUndoStack(self, stack):
        self._model.undoManager().setCurrentStack(stack)

    def centralWidgetChanged(self, index):
        widget = self._ui.stackedWidget.currentWidget()
        widget.setActive()

    def closeEvent(self, event):
        self.quitApplication()

    def quitApplication(self):
        self._model.setSize(self.size())
        self._model.setPos(self.pos())
        self._model.writeSettings()
        QtGui.qApp.quit()

    def about(self):
        from widgets.aboutdialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()
