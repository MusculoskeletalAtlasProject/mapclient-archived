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

class ErrorItem(QtGui.QGraphicsItem):

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.pixmap = QtGui.QPixmap(':/workflow/images/cancel_256.png').scaled(16, 16, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
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


class Edge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
#        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
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

        sceneRect = QtCore.QRectF(self.sourcePoint,
                         QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                       self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
 
        return sceneRect
    

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        brush = QtGui.QBrush(QtCore.Qt.black)
        if option.state & (QtGui.QStyle.State_Selected | QtGui.QStyle.State_HasFocus): #or self.selected:
            brush = QtGui.QBrush(QtCore.Qt.red)
        
        painter.setBrush(brush)

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle


        # Draw the arrows if there's enough room.
        if line.dy() * line.dy() + line.dx() * line.dx() > 200 * self.arrowSize:
            midPoint = (self.destPoint + self.sourcePoint) / 2

            destArrowP1 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi / 3) * self.arrowSize)
            destArrowP2 = midPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

            painter.drawPolygon(QtGui.QPolygonF([midPoint, destArrowP1, destArrowP2]))

        painter.setPen(QtGui.QPen(brush, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        # painter.setPen(QtGui.QPen(QtCore.Qt.SolidLine))
        painter.drawLine(line)

class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, step, location, workflowGraphicsView):
        QtGui.QGraphicsItem.__init__(self)

        self.step = step
        self.pixmap = step._pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self.configure_red = QtGui.QPixmap(':/workflow/images/configure_red.png').scaled(24, 24, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self.graph = weakref.ref(workflowGraphicsView)
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
        configureAction.triggered.connect(lambda: self.step.configure(location))
        self.contextMenu.addAction(configureAction)
        portsProvidesTip = ''
        portsUsesTip = ''
        for port in step._ports:
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

#            super(Node, self).paint(painter, option, widget)
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

    def showContextMenu(self, pos):
        self.contextMenu.popup(pos)
     
        
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


class WorkflowScene(QtGui.QGraphicsScene):
    
    sceneWidth = 500
    sceneHeight = 1.618 * sceneWidth

    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, -self.sceneHeight // 2, -self.sceneWidth // 2, self.sceneHeight, self.sceneWidth, parent)

