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
#import random
import weakref, math
import Resources_rc
#from MainWindowUi import Ui_MainWindow
from PyQt4.Qt import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

class StepList(QtGui.QListWidget):

    def __init__(self, stepIconSize, parent=None):
        super(StepList, self).__init__(parent)
        self.stepIconSize = stepIconSize

        size = QtCore.QSize(stepIconSize, stepIconSize)
        self.setIconSize(size)
        self.setSpacing(10)
#        self.setViewMode(QtGui.QListWidget.IconMode)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def addStep(self, pixmap, name):
        stepItem = QtGui.QListWidgetItem(self)
        stepItem.setText(name)
        stepItem.setIcon(QtGui.QIcon(pixmap))
        stepItem.setData(QtCore.Qt.UserRole, pixmap)
#        stepItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        stepItem.setFlags(QtCore.Qt.ItemIsEnabled)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return None

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        pixmap = QtGui.QPixmap(item.data(QtCore.Qt.UserRole))
        pixmap = pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.IgnoreAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

        dataStream << pixmap << hotspot

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-puzzle-piece', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(hotspot)
        drag.setPixmap(pixmap)

        drag.exec_(QtCore.Qt.MoveAction)

        return QtGui.QListWidget.mousePressEvent(self, event)

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
        self.adjust()

    def type(self):
        return Edge.Type

    def adjust(self):
        if not self.source() or not self.dest():
            return

        line = QtCore.QLineF(self.mapFromItem(self.source(), 0, 0), self.mapFromItem(self.dest(), 0, 0))
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

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)
#        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, pixmap, workspaceWidget):
        QtGui.QGraphicsItem.__init__(self)

        self.pixmap = pixmap
        self.graph = weakref.ref(workspaceWidget)
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

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-adjust, -adjust,
                             self.pixmap.width() + adjust,
                             self.pixmap.height() + adjust)

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
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.selected = not self.selected
            self.graph().nodeSelected(self, self.selected)

class WorkspaceWidget(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.selectedNodes = []

        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-322, -200, 644, 400)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)
        self.setMinimumSize(700, 500)
        self.setMaximumSize(700, 500)

    def clear(self):
        self.piecePixmaps = []
        self.update()

    def nodeSelected(self, node, state):
        if state == True and node not in self.selectedNodes:
            self.selectedNodes.append(node)
        elif state == False and node in self.selectedNodes:
            found = self.selectedNodes.index(node)
            del self.selectedNodes[found]

        if len(self.selectedNodes) == 2:
            self.scene().addItem(Edge(self.selectedNodes[0], self.selectedNodes[1]))
            for x in self.selectedNodes:
                x.setSelected(False)
            self.selectedNodes = []

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
        if event.mimeData().hasFormat("image/x-puzzle-piece"):
            pieceData = event.mimeData().data("image/x-puzzle-piece")
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

            event.setDropAction(Qt.MoveAction);
            event.accept();
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("image/x-puzzle-piece"):
            event.setDropAction(Qt.MoveAction);
            event.accept();
        else:
            event.ignore();

        self.update()

    def dragLeaveEvent(self, event):
        print('leaving viewport')
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-puzzle-piece"):
            event.accept()
        else:
            event.ignore()


class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__(parent)
        self.piecesList = None
        self.workspaceWidget = None

        self._makeConnections()
        self._setupWidgets()
        self._loadSteps()


    def _makeConnections(self):
        pass

    def _setupWidgets(self):
        frame = QtGui.QFrame()
        frameLayout = QtGui.QHBoxLayout(frame);
#        puzzleWidget = PuzzleWidget(400);

        self.piecesList = StepList(64, self)
        self.workspaceWidget = WorkspaceWidget()

        frameLayout.addWidget(self.piecesList)
        frameLayout.addWidget(self.workspaceWidget)
        self.setCentralWidget(frame);

    def _openImage(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = QtGui.QPixmap()

            if not newImage.load(path):
                QtGui.QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QtGui.QMessageBox.Cancel)

                return

            self.puzzleImage = newImage
            self._setupWorkspaceView()




    def _loadSteps(self):
        icons = [':/icons/pink-folder-icon.png', ':/icons/yellow-folder-icon.png', ':/icons/red-folder-icon.png', ':/icons/blue-folder-icon.png', ':/icons/green-folder-icon.png', ]
        for icon in icons:
            newImage = QtGui.QPixmap()
            newImage.load(icon)
            self.piecesList.addStep(newImage, 'image')

