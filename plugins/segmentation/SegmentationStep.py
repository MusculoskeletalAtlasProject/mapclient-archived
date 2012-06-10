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
from workspace.Workspace import WorkspaceStepPort

class Step(WorkspaceStep):
    '''
    A step that acts like the step plugin duck
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'segmentation'
        self.ports = []
        self.icon = QtGui.QPixmap(':/icons/seg.gif')
        portIn = WorkspaceStepPort()
        portIn.addProperty(('pho#workspace#port', 'uses', 'images'))
        portOut = WorkspaceStepPort()
        portOut.addProperty(('pho#workspace#port', 'provides', 'pointcloud'))
        self.ports.append(portIn)
        self.ports.append(portOut)

    def serialize(self, stream):
        description = bytearray(self.description, sys.stdout.encoding)
        stream.writeUInt32(len(description))
        stream.writeRawData(description)

        name = bytearray(self.name, sys.stdout.encoding)
        stream.writeUInt32(len(name))
        stream.writeRawData(name)

        stream << self.icon

        return stream

    @staticmethod
    def deserialize(stream):
        newStep = Step()
        descriptionLen = stream.readUInt32()
        newStep.description = stream.readRawData(descriptionLen).decode(sys.stdout.encoding)

        nameLen = stream.readUInt32()
        newStep.name = stream.readRawData(nameLen).decode(sys.stdout.encoding)

        stream >> newStep.icon

        return newStep

