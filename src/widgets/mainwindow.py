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

from PySide import QtGui

from widgets.ui_mainwindow import Ui_MainWindow
# from mountpoints.stackedwidget import StackedWidgetMountPoint
from widgets.workflowwidget import WorkflowWidget
from settings.info import DEFAULT_WORKFLOW_ANNOTATION_FILENAME

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

        self._model.readSettings()
        self.resize(self._model.size())
        self.move(self._model.pos())

        self._model.pluginManager().load()

        self._workflowWidget = WorkflowWidget(self)
        self._ui.stackedWidget.addWidget(self._workflowWidget)
        self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())

    def model(self):
        return self._model

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        self._ui.action_About.triggered.connect(self.about)
        self._ui.actionPluginManager.triggered.connect(self.pluginManager)
        self._ui.actionPMR.triggered.connect(self.pmr)
        self._ui.actionAnnotation.triggered.connect(self.annotationTool)
        self._ui.actionUndo.triggered.connect(self._model.undoManager().undo)
        self._ui.actionRedo.triggered.connect(self._model.undoManager().redo)

    def setCurrentUndoRedoStack(self, stack):
        current_stack = self._model.undoManager().currentStack()
        if current_stack:
            current_stack.canRedoChanged.disconnect(self._canRedoChanged)
            current_stack.canUndoChanged.disconnect(self._canUndoChanged)

        self._model.undoManager().setCurrentStack(stack)

        self._ui.actionRedo.setEnabled(stack.canRedo())
        self._ui.actionUndo.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._canUndoChanged)
        stack.canRedoChanged.connect(self._canRedoChanged)

    def _canRedoChanged(self, canRedo):
        self._ui.actionRedo.setEnabled(canRedo)

    def _canUndoChanged(self, canUndo):
        self._ui.actionUndo.setEnabled(canUndo)

    def execute(self):
        self._ui.stackedWidget.setCurrentWidget(self._workflowWidget)
        self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())
        self.model().workflowManager().execute()

    def setCurrentWidget(self, widget):
        if self._ui.stackedWidget.indexOf(widget) <= 0:
            self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

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

    def pluginManager(self):
        from tools.pluginmanagerdialog import PluginManagerDialog
        dlg = PluginManagerDialog(self)
        dlg.setDirectories(self._model.pluginManager().directories())
        dlg.setLoadDefaultPlugins(self._model.pluginManager().loadDefaultPlugins())

        dlg.setModal(True)
        if dlg.exec_():
            self._model.pluginManager().setDirectories(dlg.directories())
            self._model.pluginManager().setLoadDefaultPlugins(dlg.loadDefaultPlugins())
            self._model.pluginManager().load()
            self._workflowWidget.updateStepTree()

    def pmr(self):
        from tools.pmr.pmrsearchdialog import PMRSearchDialog
        dlg = PMRSearchDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def annotationTool(self):
        from tools.annotation.annotationdialog import AnnotationDialog
        location = self._model.workflowManager().location()
        dlg = AnnotationDialog(location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, self)
        dlg.setModal(True)
        dlg.exec_()

