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
from PyQt4 import QtGui
from workspace.MountPoint import WorkspaceStep

import imagesource.Resources_rc
from workspace.Workspace import WorkspaceStepPort

class ImageSourceStep(WorkspaceStep):
    '''
    A step satisfies the step plugin duck.
    
    It describes the location of an image/a set of images.
    It can be used as an image source.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'image source'
        self.ports = []
        self.pixmap = QtGui.QPixmap(':/imagesource/icons/landscapeimages.png')
        port = WorkspaceStepPort()
        port.addProperty(('pho#workspace#port', 'provides', 'images'))
        self.ports.append(port)


    def serialize(self, stream):
        description = bytearray(self.description, sys.stdout.encoding)
        stream.writeUInt32(len(description))
        stream.writeRawData(description)

        name = bytearray(self.name, sys.stdout.encoding)
        stream.writeUInt32(len(name))
        stream.writeRawData(name)

        stream << self.pixmap

        return stream

    @staticmethod
    def deserialize(stream):
        newStep = ImageSourceStep()
        descriptionLen = stream.readUInt32()
        newStep.description = stream.readRawData(descriptionLen).decode(sys.stdout.encoding)

        nameLen = stream.readUInt32()
        newStep.name = stream.readRawData(nameLen).decode(sys.stdout.encoding)

        stream >> newStep.pixmap

        return newStep

