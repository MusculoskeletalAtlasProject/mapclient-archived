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

from widgets.workflowgraphicsscene import Node, Edge

class CommandDeleteSelection(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, selection):
        super(CommandDeleteSelection, self).__init__()
        self._scene = scene
        self._selection = selection
        self.edges = {} # Need to keep the edges alive in case of undo
        self.edgeUnique = {} # Keep a record of edges marked for deletion to avoid repetition
        for item in self._selection:
            if item.Type == Node.Type:
                self.edges[item] = []
                for edge in item._connections:
                    if edge() not in self.edgeUnique:
                        self.edges[item].append(edge())
                        self.edgeUnique[edge()] = 1
            elif item.Type == Edge.Type:
                self.edgeUnique[item] = 1

    def redo(self):
        self._scene.blockSignals(True)
        for item in self._selection:
            self._scene.removeItem(item)
            if item in self.edges:
                for edge in self.edges[item]:
                    self._scene.removeItem(edge)
        self._scene.blockSignals(False)

    def undo(self):
        self._scene.blockSignals(True)
        for item in self._selection:
            self._scene.addItem(item)
            if item in self.edges:
                for edge in self.edges[item]:
                    self._scene.addItem(edge)
        self._scene.blockSignals(False)


class CommandSelectionChange(QtGui.QUndoCommand):
    '''
    We block signals  when setting the _selection so that we
    don't end up in a recursive loop.
    '''
    def __init__(self, scene, selection, previous):
        super(CommandSelectionChange, self).__init__()
        print('========= creating selection change')
        self._scene = scene
        self._selection = selection
        self._previousSelection = previous

    def redo(self):
        self._scene.blockSignals(True)
        for item in self._scene.items():
            item.setSelected(item in self._selection)
        self._scene.blockSignals(False)

    def undo(self):
        self._scene.blockSignals(True)
        for item in self._scene.items():
            item.setSelected(item in self._previousSelection)
        self._scene.blockSignals(False)


class CommandAdd(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, item):
        super(CommandAdd, self).__init__()
        self._scene = scene
        self.item = item

    def undo(self):
        self._scene.blockSignals(True)
        self._scene.removeItem(self.item)
        self._scene.blockSignals(False)

    def redo(self):
        self._scene.blockSignals(True)
        self._scene.addItem(self.item)
        self._scene.blockSignals(False)


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

