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

class UndoManager(object):
    '''
    This class is the undo redo manager for multiple undo stacks. It is a
    singleton class. 
    
    Don't inherit from this class.
    '''
    _instance = None
    undoAction = None
    redoAction = None
    stack = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UndoManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def createUndoAction(self, parent):
        self.undoAction = QtGui.QAction('Undo', parent)
        self.undoAction.triggered.connect(self.undo)
        if self.stack:
            self.undoAction.setEnabled(self.stack.canUndo())
        else:
            self.undoAction.setEnabled(False)

        return self.undoAction

    def createRedoAction(self, parent):
        self.redoAction = QtGui.QAction('Redo', parent)
        self.redoAction.triggered.connect(self.redo)
        if self.stack:
            self.redoAction.setEnabled(self.stack.canRedo())
        else:
            self.redoAction.setEnabled(False)

        return self.redoAction

    def setCurrentStack(self, stack):
        if self.stack:
            self.stack.canRedoChanged.disconnect(self._canRedoChanged)
            self.stack.canUndoChanged.disconnect(self._canUndoChanged)

        self.stack = stack
        self.redoAction.setEnabled(stack.canRedo())
        self.undoAction.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._canUndoChanged)
        stack.canRedoChanged.connect(self._canRedoChanged)

    def currentStack(self):
        return self.stack

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def _canRedoChanged(self, canRedo):
        self.redoAction.setEnabled(canRedo)

    def _canUndoChanged(self, canUndo):
        self.undoAction.setEnabled(canUndo)


