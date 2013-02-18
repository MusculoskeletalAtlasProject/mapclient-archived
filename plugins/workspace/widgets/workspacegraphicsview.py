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
import weakref, math, sys
from PyQt4 import QtCore, QtGui
from workspacestep import WorkspaceStepFactory

class ErrorItem(QtGui.QGraphicsItem):

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.pixmap = QtGui.QPixmap(':/workspace/images/cancel_256.png').scaled(16, 16, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.setZValue(-1.5)
        self.adjust()

    def boundingRect(self):
        extra = (16) / 2.0 # Icon size divided by two

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def adjust(self):
        if not self.source() or not self.dest():
            return

        sourceCentre = self.source().boundingRect().center()
        destCentre = self.dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self.source(), sourceCentre.x(), sourceCentre.y()), self.mapFromItem(self.dest(), destCentre.x(), destCentre.y()))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def paint(self, painter, option, widget):
        midPoint = (self.destPoint + self.sourcePoint) / 2
        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        painter.drawPixmap(midPoint.x() - 8, midPoint.y() - 8, self.pixmap)

class CommandAddEdge(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, node1, node2):
        super(CommandAddEdge, self).__init__()
        self.scene = scene
        self.node1 = node1
        self.node2 = node2
        self.edge = None

    def redo(self):
        self.edge = Edge(self.node1, self.node2)
        self.scene.addItem(self.edge)

    def undo(self):
        self.scene.removeItem(self.edge)
        del self.edge

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

class CommandAddNode(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, scene, node):
        super(CommandAddNode, self).__init__()
        self.scene = scene
        self.node = node

    def redo(self):
        self.scene.addItem(self.node)

    def undo(self):
        self.scene.removeItem(self.node)

class CommandNodeMove(QtGui.QUndoCommand):
    '''
    '''
    def __init__(self, selection, posDifferential):
        super(CommandNodeMove, self).__init__()
        self.selection = selection
        self.posDifferential = posDifferential
        self.init = False

    def redo(self):
        # Attempting to get around the repositioning of the node
        # as redo is called automatically on push to the stack
        if not self.init:
            self.init = True
        else:
            for node in self.selection:
                node.moveBy(self.posDifferential.x(), self.posDifferential.y())

    def undo(self):
        for node in self.selection:
            node.moveBy(-self.posDifferential.x(), -self.posDifferential.y())

class ArrowLine(QtGui.QGraphicsLineItem):

    def __init__(self, *args, **kwargs):
        super(ArrowLine, self).__init__(*args, **kwargs)
        self.arrowSize = 10.0
        self.setZValue(-2.0)

    def boundingRect(self):

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0
        line = self.line()
        return QtCore.QRectF(line.p1(),
                             QtCore.QSizeF(line.p2().x() - line.p1().x(),
                                           line.p2().y() - line.p1().y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        super(ArrowLine, self).paint(painter, option, widget)

        line = self.line()
        if line.length() == 0:
            return

        angle = math.acos(line.dx() / line.length())
#        print('angle: ', angle)
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle
        # Draw the arrows if there's enough room.
        if line.dy() * line.dy() + line.dx() * line.dx() > 200 * self.arrowSize:
            midPoint = (line.p1() + line.p2()) / 2

            destArrowP1 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi / 3) * self.arrowSize)
            destArrowP2 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

            painter.setBrush(QtCore.Qt.black)
#        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
            painter.drawPolygon(QtGui.QPolygonF([midPoint, destArrowP1, destArrowP2]))

class Edge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.setZValue(-2.0)
        self.adjust()

    def type(self):
        return Edge.Type

    def adjust(self):
        if not self.source() or not self.dest():
            return

        sourceCentre = self.source().boundingRect().center()
        destCentre = self.dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self.source(), sourceCentre.x(), sourceCentre.y()), self.mapFromItem(self.dest(), destCentre.x(), destCentre.y()))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        angle = math.acos(line.dx() / line.length())
#        print('angle: ', angle)
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle


        # Draw the arrows if there's enough room.
        if line.dy() * line.dy() + line.dx() * line.dx() > 200 * self.arrowSize:
            midPoint = (self.destPoint + self.sourcePoint) / 2

            destArrowP1 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi / 3) * self.arrowSize)
            destArrowP2 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

            painter.setBrush(QtCore.Qt.black)
#        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
            painter.drawPolygon(QtGui.QPolygonF([midPoint, destArrowP1, destArrowP2]))

def ensureItemInScene(scene, item, newPos):
    bRect = item.boundingRect()
    xp1 = bRect.x() + newPos.x()
    yp1 = bRect.y() + newPos.y()
    xp2 = bRect.x() + bRect.width() + newPos.x()
    yp2 = bRect.y() + bRect.height() + newPos.y()
    bRect.setCoords(xp1, yp1, xp2, yp2)
    rect = scene.sceneRect()
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

class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, step, workspaceGraphicsView):
        QtGui.QGraphicsItem.__init__(self)

        self.step = step
        self.pixmap = step.pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self.configure_red = QtGui.QPixmap(':/workspace/images/configure_red.png').scaled(24, 24, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self.graph = weakref.ref(workspaceGraphicsView)
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

        self.connectLine = None

        self.contextMenu = QtGui.QMenu(self.graph())
        configureAction = QtGui.QAction('Configure', self.contextMenu)
        configureAction.triggered.connect(self.step.configure)
        self.contextMenu.addAction(configureAction)
        portsProvidesTip = ''
        portsUsesTip = ''
        for port in step.ports:
            triples = port.getTriplesForPred('uses')
            for triple in triples:
                portsUsesTip += '<li>' + triple[2] + '</li>'
            triples = port.getTriplesForPred('provides')
            for triple in triples:
                portsProvidesTip += '<li>' + triple[2] + '</li>'

        if len(portsUsesTip) > 0:
            portsUsesTip = '<font color="#FFFF00"><h4>Uses</h4><ul>' + portsUsesTip + '</ul></font>'
        if len(portsProvidesTip) > 0:
            portsProvidesTip = '<font color="#33FF33"><h4>Provides</h4><ul>' + portsProvidesTip + '</ul></font>'

        tip = portsProvidesTip + portsUsesTip
        self.setToolTip(tip)


    def type(self):
        return Node.Type

    def _removeDeadwood(self):
        '''
        Unfortunately the weakref doesn't work correctly for c based classes.  This function 
        removes any None type references in edgeList.
        '''
        prunedEdgeList = [ edge for edge in self.edgeList if edge() ]
        self.edgeList = prunedEdgeList


    def hasEdgeToDestination(self, node):
        self._removeDeadwood()
        for edge in self.edgeList:
            if edge().dest() == node:
                return True

        return False

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-adjust, -adjust,
                             self.pixmap.width() + 2 * adjust,
                             self.pixmap.height() + 2 * adjust)

    def paint(self, painter, option, widget):
            if option.state & QtGui.QStyle.State_Selected: #or self.selected:
                painter.setBrush(QtCore.Qt.darkGray)
                painter.drawRoundedRect(self.boundingRect(), 5, 5)

            painter.drawPixmap(0, 0, self.pixmap)
            if not self.step.isConfigured():
                painter.drawPixmap(40, 40, self.configure_red)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange and self.scene():
            return ensureItemInScene(self.scene(), self, value)
        elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self._removeDeadwood()
            for edge in self.edgeList:
                edge().adjust()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def contextMenuEvent(self, event):
        super(Node, self).contextMenuEvent(event)
#        self.update()
        self.contextMenu.exec_(event.screenPos())

    def mousePressEvent(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            centre = self.boundingRect().center()
            self.connectLine = ArrowLine(QtCore.QLineF(self.mapToScene(centre),
                                         event.scenePos()))
            self.scene().addItem(self.connectLine)
            return

        QtGui.QGraphicsItem.mousePressEvent(self, event)
#        modifiers = QtGui.QApplication.keyboardModifiers()
#        if modifiers == QtCore.Qt.ControlModifier:
#            pass
#        else:
#            self.graph().clearSelection()

        self.eventStartPos = self.pos()

    def mouseMoveEvent(self, event):
#        modifiers = QtGui.QApplication.keyboardModifiers()
        if self.connectLine:
            newLine = QtCore.QLineF(self.connectLine.line().p1(), event.scenePos());
            self.connectLine.setLine(newLine)
            return
#        if self.contextEvent:
#            return
        QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
#        modifiers = QtGui.QApplication.keyboardModifiers()
        if self.connectLine:
            item = self.scene().itemAt(event.scenePos())
            if item.type() == Node.Type:
                self.graph().connectNodes(self, item)
            self.scene().removeItem(self.connectLine)
            self.connectLine = None
            return
#        self.update()
#        modifiers = QtGui.QApplication.keyboardModifiers()
#        if modifiers == QtCore.Qt.ControlModifier:
#            self.selected = not self.selected
#            self.graph().nodeSelected(self, self.selected)
#        else:
#            self.graph().clearSelection()
#            self.selected = True
#            self.graph().nodeSelected(self, self.selected)

        if self.pos() != self.eventStartPos:
            command = CommandNodeMove(self.scene().selectedItems(), self.pos() - self.eventStartPos)
            self.graph().undoStack.push(command)
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

class WorkspaceGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.undoStack = QtGui.QUndoStack(self)
        self.selectedNodes = []
        self.errorIconTimer = QtCore.QTimer()
        self.errorIconTimer.setInterval(3000)
        self.errorIconTimer.setSingleShot(True)
        self.errorIconTimer.timeout.connect(self.errorIconTimeout)
        self.errorIcon = None

        sceneWidth = 500
        sceneHeight = 1.618 * sceneWidth
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-sceneHeight // 2, -sceneWidth // 2, sceneHeight, sceneWidth)
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

        ws.remove('nodes')
        ws.beginGroup('nodes')
        ws.beginWriteArray('nodelist')
        nodeIndex = 0
        for node in nodeList:
            ws.setArrayIndex(nodeIndex)
            ws.setValue('name', node.step.name)
            ws.setValue('position', node.pos())
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
        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        nodeList = []
        edgeConnections = []
        for i in range(nodeCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            position = ws.value('position')
            step = WorkspaceStepFactory(name)
            node = Node(step, self)
            node.setPos(position)
            nodeList.append(node)
            command = CommandAddNode(self.scene(), node)
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
            command = CommandAddEdge(self.scene(), node1, node2)
            self.undoStack.push(command)


        self.undoStack.clear()

    def clear(self):
        self.scene().clear()

    def connectNodes(self, node1, node2):
        # Check if nodes are already connected
        if not node1.hasEdgeToDestination(node2):
            if node1.step.canConnect(node2.step):
                command = CommandAddEdge(self.scene(), node1, node2)
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
#        super(WorkspaceGraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Delete:
            command = CommandDeleteSelection(self.scene(), self.scene().selectedItems())
            self.undoStack.push(command)
            event.accept()
        else:
            event.ignore()

    def errorIconTimeout(self):
        self.scene().removeItem(self.errorIcon)
        del self.errorIcon

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
        gradient.setColorAt(0, QtGui.QColor('aliceblue'))
        gradient.setColorAt(1, QtGui.QColor('lightskyblue'))
#        if self.isEnabled():
#            gradient.setColorAt(0, QtGui.QColor('aliceblue'))
#            gradient.setColorAt(1, QtGui.QColor('lightskyblue'))
#        else:
#            gradient.setColorAt(0, QtGui.QColor('lightgrey'))
#            gradient.setColorAt(1, QtGui.QColor('darkgrey'))
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-workspace-step"):
            pieceData = event.mimeData().data("image/x-workspace-step")
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            hotspot = QtCore.QPoint()

            nameLen = stream.readUInt32()
            name = stream.readRawData(nameLen).decode(sys.stdout.encoding)
            step = WorkspaceStepFactory(name)
            stream >> hotspot

            position = self.mapToScene(event.pos() - hotspot)
            node = Node(step, self)
            node.setPos(ensureItemInScene(self.scene(), node, position))

            self.undoStack.beginMacro('Add node')
            command = CommandAddNode(self.scene(), node)
            self.undoStack.push(command)
            self.scene().clearSelection()
            node.setSelected(True)
            self.undoStack.endMacro()

            event.setDropAction(QtCore.Qt.MoveAction);
            event.accept();
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("image/x-workspace-step"):
            event.setDropAction(QtCore.Qt.MoveAction);
            event.accept();
        else:
            event.ignore();

        self.update()

    def dragLeaveEvent(self, event):
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-workspace-step"):
            event.accept()
        else:
            event.ignore()
