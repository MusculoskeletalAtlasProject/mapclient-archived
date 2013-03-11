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

class CommandDeleteSelection(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, selection):
        super(CommandDeleteSelection, self).__init__()
        self.scene = scene
        self.selection = selection
        self.edges = {} # Need to keep the edges alive in case of undo
        self.edgeUnique = {} # Keep a record of edges marked for deletion to avoid repetition
        for item in self.selection:
            self.edges[item] = []
            for edge in item.edgeList:
                if edge() not in self.edgeUnique:
                    self.edges[item].append(edge())
                    self.edgeUnique[edge()] = 1

    def redo(self):
        self.scene.blockSignals(True)
        for item in self.selection:
            self.scene.removeItem(item)
            for edge in self.edges[item]:
                self.scene.removeItem(edge)
        self.scene.blockSignals(False)

    def undo(self):
        self.scene.blockSignals(True)
        for item in self.selection:
            self.scene.addItem(item)
            for edge in self.edges[item]:
                self.scene.addItem(edge)
        self.scene.blockSignals(False)


class CommandSelectionChange(QtGui.QUndoCommand):
    '''
    We block signals  when setting the selection so that we
    don't end up in a recursive loop.
    '''
    def __init__(self, selection, previous):
        super(CommandSelectionChange, self).__init__()
        self.selection = selection
        self.previousSelection = previous

    def blockSignalsAndClear(self):
        if len(self.selection) > 0:
            self.selection[0].scene().blockSignals(True)
            self.selection[0].scene().clearSelection()
        if len(self.selection) == 0 and len(self.previousSelection) > 0:
            self.previousSelection[0].scene().blockSignals(True)
            self.previousSelection[0].scene().clearSelection()

    def unblockSignals(self):
        if len(self.selection) > 0:
            self.selection[0].scene().blockSignals(False)
        if len(self.selection) == 0 and len(self.previousSelection) > 0:
            self.previousSelection[0].scene().blockSignals(False)

    def redo(self):
        self.blockSignalsAndClear()
        for item in self.selection:
            item.setSelected(True)
        self.unblockSignals()

    def undo(self):
        self.blockSignalsAndClear()
        for item in self.previousSelection:
            item.setSelected(True)
        self.unblockSignals()


class CommandAdd(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, item):
        super(CommandAdd, self).__init__()
        self.scene = scene
        self.item = item

    def undo(self):
        self.scene.removeItem(self.item)

    def redo(self):
        self.scene.addItem(self.item)


class CommandMove(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, node, posFrom, posTo):
        super(CommandMove, self).__init__()
        self._node = node
        self._from = posFrom
        self._to = posTo

    def redo(self):
        self._node.setPos(self._to)

    def undo(self):
        self._node.setPos(self._from)

