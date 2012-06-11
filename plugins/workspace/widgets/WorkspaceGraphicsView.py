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
import weakref, math
from PyQt4 import QtCore, QtGui

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


class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, pixmap, workspaceGraphicsView):
        QtGui.QGraphicsItem.__init__(self)

        self.pixmap = pixmap
        self.graph = weakref.ref(workspaceGraphicsView)
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        self.selected = False

    def type(self):
        return Node.Type

    def setSelected(self, state):
        self.selected = state
        self.update()

    def hasEdgeToDestination(self, node):
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
            if option.state & QtGui.QStyle.State_Sunken or self.selected:
                painter.setBrush(QtCore.Qt.darkGray)
                painter.drawRoundedRect(self.boundingRect(), 5, 5)

            painter.drawPixmap(0, 0, self.pixmap)

    def itemChange(self, change, value):

        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            pass
        else:
            self.graph().clearSelection()

        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.selected = not self.selected
            self.graph().nodeSelected(self, self.selected)
        else:
            self.graph().clearSelection()
            self.selected = True
            self.graph().nodeSelected(self, self.selected)

class WorkspaceGraphicsView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.selectedNodes = []

        sceneWidth = 800
        sceneHeight = 1.618 * sceneWidth
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-sceneHeight // 2, -sceneWidth // 2, sceneHeight, sceneWidth)
#        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
#        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
#        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)
#        self.setMinimumSize(sceneHeight + 20, sceneWidth + 20)
#        self.setMaximumSize(sceneHeight + 20, sceneWidth + 20)

    def clear(self):
        self.piecePixmaps = []
        self.update()


    def connectNodes(self, node1, node2):
        # Check if nodes are already connected
        if not node1.hasEdgeToDestination(node2):
#        if node1.
            self.scene().addItem(Edge(node1, node2))
#            for x in self.selectedNodes:
#                x.setSelected(False)

#        self.clearSelection()

    def clearSelection(self):
        for node in self.selectedNodes:
            node.selected = False
            node.update()

        self.selectedNodes = []

    def nodeSelected(self, node, state):
        if state == True and node not in self.selectedNodes:
            self.selectedNodes.append(node)
        elif state == False and node in self.selectedNodes:
            found = self.selectedNodes.index(node)
            del self.selectedNodes[found]

        if len(self.selectedNodes) == 2:
            self.connectNodes(self.selectedNodes[0], self.selectedNodes[1])

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
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)
#        print(QtGui.QColor.colorNames())

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-workspace-step"):
            pieceData = event.mimeData().data("image/x-workspace-step")
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            pixmap = QtGui.QPixmap()
            hotspot = QtCore.QPoint()

            stream >> pixmap >> hotspot

            node = Node(pixmap, self)
            node.setPos(self.mapToScene(event.pos() - hotspot))
            self.scene().addItem(node)
#            ic = self.scene().addPixmap(pixmap)
#            ic.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
#            ic.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
#            ic.setPos(self.mapToScene(event.pos() - hotspot))

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
