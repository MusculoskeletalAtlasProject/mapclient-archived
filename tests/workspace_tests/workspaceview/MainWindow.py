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
import random
import weakref

from MainWindowUi import Ui_MainWindow
from PyQt4.Qt import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import QAbstractListModel, QModelIndex, QByteArray, QDataStream, QIODevice, QMimeData, QPoint, QRect
from PyQt4.QtGui import QMainWindow, QIcon, QPixmap, QWidget, QPainter, QColor, QDrag

class PiecesModel(QAbstractListModel):

    def __init__(self, parent=None, *args, **kwargs):
        QAbstractListModel.__init__(self, parent, *args, **kwargs)
        self.locations = []
        self.pixmaps = []

    def data(self, index, role):
        if not index.isValid():
            return None;

        if role == Qt.DecorationRole:
            return QIcon(self.pixmaps[index.row()].scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif role == Qt.UserRole:
            return self.pixmaps[index.row()]
        elif role == Qt.UserRole + 1:
            return self.locations[index.row()]

        return None;

    def addPiece(self, pixmap, location):
        if random.random() < 0.5:
            row = 0;
        else:
            row = len(self.pixmaps);

        self.beginInsertRows(QModelIndex(), row, row);
        self.pixmaps.insert(row, pixmap);
        self.locations.insert(row, location);
        self.endInsertRows();

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

        return Qt.ItemIsDropEnabled;

    def removeRows(self, row, count, parent):
        if parent.isValid():
            return False

        if (row >= len(self.pixmaps) or row + count <= 0):
            return False

        beginRow = max(0, row);
        endRow = min(row + count - 1, len(self.pixmaps) - 1)

        self.beginRemoveRows(parent, beginRow, endRow)

        del self.pixmaps[beginRow:endRow + 1]
        del self.locations[beginRow:endRow + 1]

        self.endRemoveRows();
        return True

    def mimeTypes(self):
        return ['image/x-puzzle-piece']

    def mimeData(self, indexes):
        mimeData = QMimeData()
        encodedData = QByteArray()

        stream = QDataStream(encodedData, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = self.data(index, Qt.UserRole)
                location = self.data(index, Qt.UserRole + 1)
                stream << pixmap << location;

        mimeData.setData("image/x-puzzle-piece", encodedData);
        return mimeData;

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat("image/x-puzzle-piece"):
            return False

        if action == Qt.IgnoreAction:
            return True;

        if column > 0:
            return False;

        if not parent.isValid():
            if row < 0:
                endRow = len(self.pixmaps)
            else:
                endRow = min(row, len(self.pixmaps))
        else:
            endRow = parent.row();

        encodedData = data.data("image/x-puzzle-piece")
        stream = QDataStream(encodedData, QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = QPixmap();
            location = QPoint();
            stream >> pixmap >> location;

            self.beginInsertRows(QModelIndex(), endRow, endRow);
            self.pixmaps.insert(endRow, pixmap);
            self.locations.insert(endRow, location);
            self.endInsertRows();

            endRow += 1

        return True

    def rowCount(self, parent):
        if parent.isValid():
            return 0

        return len(self.pixmaps)

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def addPieces(self, pixmap):
        self.beginRemoveRows(QModelIndex(), 0, 24);
        self.pixmaps = []
        self.locations = []
        self.endRemoveRows();
        for y in [0, 1, 2, 3, 4]:
            for x in [0, 1, 2, 3, 4]:
                pieceImage = pixmap.copy(x * 80, y * 80, 80, 80);
                self.addPiece(pieceImage, QPoint(x, y))


class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, puzzleWidget):
        QtGui.QGraphicsItem.__init__(self)

        self.graph = weakref.ref(puzzleWidget)
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        self.selected = None

    def type(self):
        return Node.Type


class WorkspaceWidget(QtGui.QGraphicsView):

    puzzleCompleted = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QRect()
        self.inPlace = 0

        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QRect()
        self.inPlace = 0;
        self.update()

    def targetSquare(self, position):
        return QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80);

    def findPiece(self, pieceRect):
        try:
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

#    def paintEvent(self, event):
#    def render(self, painter, target):
#        print('hi')
#        painter.begin(self)
#        painter.fillRect(target, Qt.white)
#
#        print(target)
#        print(self.sceneRect())
#        if self.highlightedRect.isValid():
#            painter.setBrush(QColor("#ffcccc"))
#            painter.setPen(Qt.NoPen)
#            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))
#
#        for i, pieceRect in enumerate(self.pieceRects):
#            painter.drawPixmap(pieceRect, self.piecePixmaps[i])
#
#        painter.end()

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos());
        found = self.findPiece(square);

        if found == -1:
            return;

        location = self.pieceLocations[found]
        pixmap = self.piecePixmaps[found]
        del self.pieceLocations[found]
        del self.piecePixmaps[found]
        del self.pieceRects[found]

        if location == QPoint(square.x() / 80, square.y() / 80):
            self.inPlace = self.inPlace - 1

        self.update(square);

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)

        dataStream << pixmap << location;

        mimeData = QMimeData()
        mimeData.setData("image/x-puzzle-piece", itemData);

        drag = QDrag(self);
        drag.setMimeData(mimeData);
        drag.setHotSpot(event.pos() - square.topLeft());
        drag.setPixmap(pixmap);

        if drag.start(Qt.MoveAction) == 0:
            self.pieceLocations.insert(found, location);
            self.piecePixmaps.insert(found, pixmap);
            self.pieceRects.insert(found, square);
            self.update(self.targetSquare(event.pos()));

            if location == QPoint(square.x() / 80, square.y() / 80):
                self.inPlace = self.inPlace + 1

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/x-puzzle-piece") \
            and self.findPiece(self.targetSquare(event.pos())) == -1:

            pieceData = event.mimeData().data("image/x-puzzle-piece")
            stream = QDataStream(pieceData, QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QPixmap()
            location = QPoint()
            stream >> pixmap >> location;

            self.pieceLocations.append(location);
            self.piecePixmaps.append(pixmap);
            ic = self.scene().addPixmap(pixmap)
            ic.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
            ic.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
            self.pieceRects.append(square);

            self.highlightedRect = QRect();
            self.update(square);

            event.setDropAction(Qt.MoveAction);
            event.accept();

            if location == QPoint(square.x() / 80, square.y() / 80):
                self.inPlace = self.inPlace + 1;
                if self.inPlace == 25:
                    self.puzzleCompleted.emit()
        else:
            self.highlightedRect = QRect();
            event.ignore()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.unite(self.targetSquare(event.pos()));

        if event.mimeData().hasFormat("image/x-puzzle-piece") \
            and self.findPiece(self.targetSquare(event.pos())) == -1:

            self.highlightedRect = self.targetSquare(event.pos());
            event.setDropAction(Qt.MoveAction);
            event.accept();
        else:
            self.highlightedRect = QRect();
            event.ignore();

        self.update(updateRect)

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect;
        self.highlightedRect = QRect();
        self.update(updateRect);
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/x-puzzle-piece"):
            event.accept()
        else:
            event.ignore()

class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.widget_Puzzle = WorkspaceWidget(self.frame)
        self.frame.layout().addWidget(self.widget_Puzzle)
        self.piecesModel = PiecesModel()
        self.puzzleImage = QPixmap(':/images/bolton_game.jpg')
        self.listView.setModel(self.piecesModel)

        self._makeConnections()
        self._setupPuzzle()


    def _makeConnections(self):
        self.action_Open.triggered.connect(self._openImage)
        self.action_Restart.triggered.connect(self._setupPuzzle)

    def _openImage(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = QPixmap()

            if not newImage.load(path):
                QtGui.QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QtGui.QMessageBox.Cancel)

                return

            self.puzzleImage = newImage
            self._setupPuzzle()




    def _setupPuzzle(self):
        size = min(self.puzzleImage.width(), self.puzzleImage.height());
        self.puzzleImage = self.puzzleImage.copy((self.puzzleImage.width() - size) / 2,
            (self.puzzleImage.height() - size) / 2, size, size).scaled(400,
                400, Qt.IgnoreAspectRatio, Qt.SmoothTransformation);

        random.seed(QtGui.QCursor.pos().x() ^ QtGui.QCursor.pos().y())

        self.piecesModel.addPieces(self.puzzleImage);
        self.widget_Puzzle.clear()
