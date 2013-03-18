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
import math, weakref

from PyQt4 import QtCore, QtGui

from core.workflowscene import Connection

class ErrorItem(QtGui.QGraphicsItem):

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        self._source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self._pixmap = QtGui.QPixmap(':/workflow/images/cancel_256.png').scaled(16, 16, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self._source().addEdge(self)
        self.dest().addEdge(self)
        self.setZValue(-1.5)
        self.adjust()

    def boundingRect(self):
        extra = (16) / 2.0 # Icon size divided by two

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def adjust(self):
        if not self._source() or not self.dest():
            return

        sourceCentre = self._source().boundingRect().center()
        destCentre = self.dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self._source(), sourceCentre.x(), sourceCentre.y()), self.mapFromItem(self.dest(), destCentre.x(), destCentre.y()))
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

        painter.drawPixmap(midPoint.x() - 8, midPoint.y() - 8, self._pixmap)

class Item(QtGui.QGraphicsItem):
    '''
    Class to contain the selection information that selectable scene items can be derived from.
    '''
    
    
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        
    def setSelected(self, selected):
        QtGui.QGraphicsItem.setSelected(self, selected)
        self.scene().workflowScene().setItemSelected(self.metaItem(), selected)
        
       
class Edge(Item):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        Item.__init__(self)

        self.arrowSize = 10.0
        
        self._connection = Connection(sourceNode._metastep, destNode._metastep)
        
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
#        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self._source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self._source().addEdge(self)
        self.dest().addEdge(self)
        self.setZValue(-2.0)
        self.adjust()

    def connection(self):
        return self._connection
    
    def type(self):
        return Edge.Type
    
    def metaItem(self):
        return self._connection

    def adjust(self):
        if not self._source() or not self.dest():
            return

        sourceCentre = self._source().boundingRect().center()
        destCentre = self.dest().boundingRect().center()
        line = QtCore.QLineF(self.mapFromItem(self._source(), sourceCentre.x(), sourceCentre.y()), self.mapFromItem(self.dest(), destCentre.x(), destCentre.y()))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self._source() or not self.dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0

        sceneRect = QtCore.QRectF(self.sourcePoint,
                         QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                       self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
 
        return sceneRect
    

    def paint(self, painter, option, widget):
        if not self._source() or not self.dest():
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

class Node(Item):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, metastep):
        Item.__init__(self)

        self._metastep = metastep
        self._pixmap = QtGui.QPixmap.fromImage(self._metastep._step._icon).scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self._configure_red = QtGui.QPixmap(':/workflow/images/configure_red.png').scaled(24, 24, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        self._connections = []
#        self.graph = weakref.ref(workflowGraphicsView)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)

        self._contextMenu = QtGui.QMenu()
        configureAction = QtGui.QAction('Configure', self._contextMenu)
        configureAction.triggered.connect(self._metastep._step.configure)
        self._contextMenu.addAction(configureAction)
        portsProvidesTip = ''
        portsUsesTip = ''
        for port in self._metastep._step._ports:
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


    def setPos(self, pos):
        QtGui.QGraphicsItem.setPos(self, pos)
        self.scene().workflowScene().setItemPos(self._metastep, pos)
        
    def type(self):
        return Node.Type
    
    def metaItem(self):
        return self._metastep

    def _removeDeadwood(self):
        '''
        Unfortunately the weakref doesn't work correctly for c based classes.  This function 
        removes any None type references in _connections.
        '''
        prunedEdgeList = [ edge for edge in self._connections if edge() ]
        self._connections = prunedEdgeList


    def hasEdgeToDestination(self, node):
        self._removeDeadwood()
        for edge in self._connections:
            if edge().dest() == node:
                return True

        return False

    def addEdge(self, edge):
        self._connections.append(weakref.ref(edge))
        
    def removeEdge(self, edge):
        if edge in self._connections:
            index = self._connections.index(edge)
            self._connections[index] = []

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-adjust, -adjust,
                             self._pixmap.width() + 2 * adjust,
                             self._pixmap.height() + 2 * adjust)

    def paint(self, painter, option, widget):
            if option.state & QtGui.QStyle.State_Selected: #or self.selected:
                painter.setBrush(QtCore.Qt.darkGray)
                painter.drawRoundedRect(self.boundingRect(), 5, 5)

#            super(Node, self).paint(painter, option, widget)
            painter.drawPixmap(0, 0, self._pixmap)
            if not self._metastep._step.isConfigured():
                painter.drawPixmap(40, 40, self._configure_red)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange and self.scene():
            return self.scene().ensureItemInScene(self, value)
        elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self._removeDeadwood()
            for edge in self._connections:
                edge().adjust()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def showContextMenu(self, pos):
        self._contextMenu.popup(pos)
     
        
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


