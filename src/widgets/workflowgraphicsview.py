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
import sys, os

from PyQt4 import QtCore, QtGui

from mountpoints.workflowstep import workflowStepFactory
from core.workflowcommands import CommandSelectionChange, CommandDeleteSelection, CommandAdd
from core.workflowscene import WorkflowScene, Node, Edge, ErrorItem, ensureItemInScene

class WorkflowGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.mainWindow = None
        self.undoStack = QtGui.QUndoStack(self)
        self.selectedNodes = []
        self.errorIconTimer = QtCore.QTimer()
        self.errorIconTimer.setInterval(3000)
        self.errorIconTimer.setSingleShot(True)
        self.errorIconTimer.timeout.connect(self.errorIconTimeout)
        self.errorIcon = None

        scene = WorkflowScene(self)
        scene.selectionChanged.connect(self.selectionChanged)

        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
#        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
#        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)

    def saveState(self, ws):
        sceneItems = self.scene().items()
        nodeList = []
        for item in sceneItems:
            if item.type() == Node.Type:
                nodeList.append(item)

        location = self.mainWindow.workflowManager.location
        ws.remove('nodes')
        ws.beginGroup('nodes')
        ws.beginWriteArray('nodelist')
        nodeIndex = 0
        for node in nodeList:
            if node.step.isConfigured():
                step_location = os.path.join(location, node.step.getIdentifier())
                node.step.serialize(step_location)
            ws.setArrayIndex(nodeIndex)
            ws.setValue('name', node.step.getName())
            ws.setValue('position', node.pos())
            ws.setValue('identifier', node.step.getIdentifier())
            ws.beginWriteArray('edgeList')
            edgeIndex = 0
            for edge in node.edgeList:
                if edge().source() == node:
                    ws.setArrayIndex(edgeIndex)
                    indecies = [i for i, x in enumerate(nodeList) if x == edge().dest()]
                    ws.setValue('connectedTo', indecies[0])
                    edgeIndex += 1
            ws.endArray()
            nodeIndex += 1
        ws.endArray()
        ws.endGroup()

    def loadState(self, ws):
        self.clear()
        self.undoStack.clear()
        location = self.mainWindow.workflowManager.location
        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        nodeList = []
        edgeConnections = []
        for i in range(nodeCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            position = ws.value('position')
            identifier = ws.value('identifier')
            step = workflowStepFactory(name)
            step.setIdentifier(identifier)
            step_location = os.path.join(location, identifier)
            step.deserialize(step_location)
            node = Node(step, location, self)
            node.setPos(position)
            nodeList.append(node)
            command = CommandAdd(self.scene(), node)
            self.undoStack.push(command)
            edgeCount = ws.beginReadArray('edgeList')
            for j in range(edgeCount):
                ws.setArrayIndex(j)
                connectedTo = int(ws.value('connectedTo'))
                edgeConnections.append((i, connectedTo))
            ws.endArray()
        ws.endArray()
        ws.endGroup()
        for edge in edgeConnections:
            node1 = nodeList[edge[0]]
            node2 = nodeList[edge[1]]
            command = CommandAdd(self.scene(), Edge(node1, node2))
            #command = CommandAddEdge(self.scene(), node1, node2)
            self.undoStack.push(command)


        self.undoStack.clear()

    def clear(self):
        self.scene().clear()

    def connectNodes(self, node1, node2):
        # Check if nodes are already connected
        if not node1.hasEdgeToDestination(node2):
            if node1.step.canConnect(node2.step):
                command = CommandAdd(self.scene(), Edge(node1, node2))
                self.undoStack.push(command)
            else:
                # add temporary line ???
                if self.errorIconTimer.isActive():
                    self.errorIconTimer.stop()
                    self.errorIconTimeout()

                self.errorIcon = ErrorItem(node1, node2)
                self.scene().addItem(self.errorIcon)
                self.errorIconTimer.start()

    def selectionChanged(self):
        # Search the undo stack to get the previous selection
        previousSelection = []
        previousSelectionFound = False
        for index in range(self.undoStack.count(), 0, -1):
            com = self.undoStack.command(index - 1)
            if type(com) is CommandSelectionChange:
                previousSelection = com.selection
                previousSelectionFound = True
            elif type(com) is QtGui.QUndoCommand:
                for childIndex in range(com.childCount(), 0, -1):
                    childCom = com.child(childIndex)
                    if type(childCom) is CommandSelectionChange:
                        previousSelection = childCom.selection
                        previousSelectionFound = True
                        break
            if previousSelectionFound:
                break

        command = CommandSelectionChange(self.scene().selectedItems(), previousSelection)
        self.undoStack.push(command)

    def nodeSelected(self, node, state):
        if state == True and node not in self.selectedNodes:
            self.selectedNodes.append(node)
        elif state == False and node in self.selectedNodes:
            found = self.selectedNodes.index(node)
            del self.selectedNodes[found]

        if len(self.selectedNodes) == 2:
            self.connectNodes(self.selectedNodes[0], self.selectedNodes[1])

    def keyPressEvent(self, event):
#        super(WorkflowGraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            command = CommandDeleteSelection(self.scene(), self.scene().selectedItems())
            self.undoStack.push(command)
            event.accept()
        else:
            event.ignore()

    def errorIconTimeout(self):
        self.scene().removeItem(self.errorIcon)
        del self.errorIcon

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.EnabledChange:
            self.invalidateScene(self.sceneRect())
       
    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        rightShadow = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
            painter.fillRect(rightShadow, QtCore.Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
            painter.fillRect(bottomShadow, QtCore.Qt.darkGray)

        # Fill.
        gradient = QtGui.QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        if self.isEnabled():
            gradient.setColorAt(0, QtGui.QColor('aliceblue'))
            gradient.setColorAt(1, QtGui.QColor('lightskyblue'))
        else:
            gradient.setColorAt(0, QtGui.QColor('lightgrey'))
            gradient.setColorAt(1, QtGui.QColor('darkgrey'))
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            pieceData = event.mimeData().data("image/x-workflow-step")
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            hotspot = QtCore.QPoint()

            nameLen = stream.readUInt32()
            name = stream.readRawData(nameLen).decode(sys.stdout.encoding)
            step = workflowStepFactory(name)
            stream >> hotspot

            position = self.mapToScene(event.pos() - hotspot)
            location = self.mainWindow.workflowManager.location
            node = Node(step, location, self)
            node.setPos(ensureItemInScene(self.scene(), node, position))

            self.undoStack.beginMacro('Add node')
            command = CommandAdd(self.scene(), node)
            self.undoStack.push(command)
            self.scene().clearSelection()
            node.setSelected(True)
            self.undoStack.endMacro()

            event.setDropAction(QtCore.Qt.MoveAction);
            event.accept();
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            event.setDropAction(QtCore.Qt.MoveAction);
            event.accept();
        else:
            event.ignore();

        self.update()

    def dragLeaveEvent(self, event):
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            event.accept()
        else:
            event.ignore()
