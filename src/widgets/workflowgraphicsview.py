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
import sys

from PyQt4 import QtCore, QtGui

from mountpoints.workflowstep import workflowStepFactory
from core.workflowcommands import CommandSelectionChange, CommandDeleteSelection, CommandAdd, CommandMove
from core.workflowscene import MetaStep
from widgets.workflowgraphicsscene import WorkflowGraphicsScene, Node, Edge, ErrorItem, ArrowLine, ensureItemInScene

class WorkflowGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self._mainWindow = None
        self.selectedNodes = []
        self.errorIconTimer = QtCore.QTimer()
        self.errorIconTimer.setInterval(2000)
        self.errorIconTimer.setSingleShot(True)
        self.errorIconTimer.timeout.connect(self.errorIconTimeout)
        self.errorIcon = None
        
        self.undoStack = None
        
        self.connectLine = None
        self.connectSourceNode = None
        
        self.selectionStartPos = None

        self._previousSelection = []
        
        scene = WorkflowGraphicsScene(self)
        scene.selectionChanged.connect(self.selectionChanged)
        self.setScene(scene)

        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
#        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
#        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)

    def clear(self):
        self.scene().clear()

    def setUndoStack(self, stack):
        self.undoStack = stack
        
    def connectNodes(self, node1, node2):
        # Check if nodes are already connected
        if not node1.hasEdgeToDestination(node2):
            if node1._metastep._step.canConnect(node2._metastep._step):
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
#        previousSelection = []
#        previousSelectionFound = False
#        for index in range(self.undoStack.count(), 0, -1):
#            com = self.undoStack.command(index - 1)
#            if type(com) is CommandSelectionChange:
#                previousSelection = com.selection
#                previousSelectionFound = True
#            elif type(com) is QtGui.QUndoCommand:
#                for childIndex in range(com.childCount(), 0, -1):
#                    childCom = com.child(childIndex)
#                    if type(childCom) is CommandSelectionChange:
#                        previousSelection = childCom.selection
#                        previousSelectionFound = True
#                        break
#            if previousSelectionFound:
#                break

        currentSelection = self.scene().selectedItems()
        print(self.scene().selectedItems())
        command = CommandSelectionChange(self.scene(), currentSelection, previousSelection)
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
            
    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.type() == Node.Type:
            item.showContextMenu(event.globalPos())

    def mousePressEvent(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if event.button() == QtCore.Qt.RightButton:
            event.ignore()
        elif modifiers & QtCore.Qt.ShiftModifier:
            item = self.scene().itemAt(self.mapToScene(event.pos()))
            if item and item.type() == Node.Type:
                centre = item.boundingRect().center()
                self.connectSourceNode = item
                self.connectLine = ArrowLine(QtCore.QLineF(item.mapToScene(centre),
                                             self.mapToScene(event.pos())))
                self.scene().addItem(self.connectLine)
        else:
            QtGui.QGraphicsView.mousePressEvent(self, event)
            self.selectionStartPos = event.pos()
            
    def mouseMoveEvent(self, event):
        if self.connectLine:
            newLine = QtCore.QLineF(self.connectLine.line().p1(), self.mapToScene(event.pos()))
            self.connectLine.setLine(newLine)
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.connectLine:
            item = self.scene().itemAt(self.mapToScene(event.pos()))
            if item and item.type() == Node.Type:
                self.connectNodes(self.connectSourceNode, item)
            self.scene().removeItem(self.connectLine)
            self.connectLine = None
            self.connectSourceNode = None
        else:
            QtGui.QGraphicsView.mouseReleaseEvent(self, event)
            diff = event.pos() - self.selectionStartPos
            if diff.x() != 0 and diff.y() != 0:
                self.undoStack.beginMacro('Move Step(s)')
                for item in self.scene().selectedItems():
                    if item.type() == Node.Type:
                        self.undoStack.push(CommandMove(item, item.pos() - diff, item.pos()))
                self.undoStack.endMacro()

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
            stream >> hotspot

            position = self.mapToScene(event.pos() - hotspot)
            location = self._mainWindow.model().workflowManager().location()
            step = MetaStep(workflowStepFactory(name))
            node = Node(step, location)

            self.undoStack.beginMacro('Add node')
            self.undoStack.push(CommandAdd(self.scene(), node))
            # Set the position after it has been added to the scene
            node.setPos(ensureItemInScene(self.scene(), node, position))
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

#    def dragLeaveEvent(self, event):
#        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-workflow-step"):
            event.accept()
        else:
            event.ignore()
     
