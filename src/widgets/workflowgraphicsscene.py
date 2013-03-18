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

from core.workflowscene import MetaStep, Connection
from widgets.workflowgraphicsitems import Node, Edge
from widgets.workflowcommands import CommandConfigure

       
class WorkflowGraphicsScene(QtGui.QGraphicsScene):
    '''
    This view side class is a non-authoratative representation
    of the current workflow scene model.  It must be kept in 
    sync with the authoratative workflow scene model.
    '''
    
    sceneWidth = 500
    sceneHeight = 1.618 * sceneWidth

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, -self.sceneHeight // 2, -self.sceneWidth // 2, self.sceneHeight, self.sceneWidth, parent)
        self._workflow_scene = None
        self._previousSelection = []
        self._undoStack = None

    def setWorkflowScene(self, scene):
        self._workflow_scene = scene
        
    def workflowScene(self):
        return self._workflow_scene
        
    def setUndoStack(self, stack):
        self._undoStack = stack
        
    def addItem(self, item):
        QtGui.QGraphicsScene.addItem(self, item)
        if hasattr(item, 'Type'):
            if item.Type == Node.Type:
                self._workflow_scene.addItem(item._metastep)
            elif item.Type == Edge.Type:
                self._workflow_scene.addItem(item._connection)
        
    def removeItem(self, item):
        QtGui.QGraphicsScene.removeItem(self, item)
        if hasattr(item, 'Type'):
            if item.Type == Node.Type:
                self._workflow_scene.removeItem(item._metastep)
            elif item.Type == Edge.Type:
                print('remove item')
                # who has this connection?
                item.
                self._workflow_scene.removeItem(item._connection)
                
    def updateModel(self):
        '''
        Clears the QGraphicScene and re-populates it with what is currently 
        in the WorkflowScene.
        '''
        QtGui.QGraphicsScene.clear(self)
        meta_steps = {}
        connections = []
        for workflowitem in self._workflow_scene.items():
            if workflowitem.Type == MetaStep.Type:
                node = Node(workflowitem)
                workflowitem._step.registerConfiguredObserver(self.stepConfigured)
                # Put the node into the scene straight away so that the items scene will
                # be valid when we set the position.
                QtGui.QGraphicsScene.addItem(self, node)
                node.setPos(workflowitem.pos())
                self.blockSignals(True)
                node.setSelected(workflowitem.selected())
                self.blockSignals(False)
                meta_steps[workflowitem] = node
            elif workflowitem.Type == Connection.Type:
                connections.append(workflowitem)
                
        for connection in connections:
            edge = Edge(meta_steps[connection.source()], meta_steps[connection.destination()])
            # Overwrite the connection created in the Edge with the original one that is in the 
            # WorkflowScene
            edge._connection = connection
            # Again put the edge into the scene straight away so the scene will be valid
            QtGui.QGraphicsScene.addItem(self, edge)
            self.blockSignals(True)
            edge.setSelected(connection.selected())
            self.blockSignals(False)
            
        self._previousSelection = self.selectedItems()
            
    def ensureItemInScene(self, item, newPos):
        bRect = item.boundingRect()
        xp1 = bRect.x() + newPos.x()
        yp1 = bRect.y() + newPos.y()
        xp2 = bRect.x() + bRect.width() + newPos.x()
        yp2 = bRect.y() + bRect.height() + newPos.y()
        bRect.setCoords(xp1, yp1, xp2, yp2)
        rect = self.sceneRect()
        if not rect.contains(bRect):
            x1 = max(bRect.left(), rect.left()) + 2.0 # plus bounding rectangle adjust
            x2 = min(bRect.x() + bRect.width(), rect.x() + rect.width()) - bRect.width() + 2.0
            y1 = max(bRect.top(), rect.top()) + 2.0 # plus bounding rectangle adjust
            y2 = min(bRect.bottom(), rect.bottom()) - bRect.height() + 2.0
            if newPos.x() != x1:
                newPos.setX(x1)
            elif newPos.x() != x2:
                newPos.setX(x2)
            if newPos.y() != y1:
                newPos.setY(y1)
            elif newPos.y() != y2:
                newPos.setY(y2)
    
        return newPos

    def clear(self):
        QtGui.QGraphicsScene.clear(self)
        self._workflow_scene.clear()
        
    def previouslySelectedItems(self):
        return self._previousSelection
    
    def setPreviouslySelectedItems(self, selection):
        self._previousSelection = selection
        
    def stepConfigured(self):
        print('step configured!')
        self._undoStack.push(CommandConfigure(self))

