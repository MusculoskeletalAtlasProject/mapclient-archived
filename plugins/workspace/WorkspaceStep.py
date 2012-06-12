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
from workspace.MountPoint import WorkspaceStepMountPoint

class WorkspaceStepPort(object):
    '''
    Describes the location and properties of a port for a workspace step.
    '''
    def __init__(self):
        self.subj = {}
        self.pred = {}
        self.obj = {}

    def serialize(self, stream):
        keyCount = len(self.subj)
        stream.writeUInt32(keyCount)
        for key in self.subj:
            triple = self.subj[key]
            for mem in triple:
                name = bytearray(mem, sys.stdout.encoding)
                stream.writeUInt32(len(name))
                stream.writeRawData(name)

        return stream

    @staticmethod
    def deserialize(newStepPort, stream):
        keyCount = stream.readUInt32()
        for _ in range(keyCount):
            subjLen = stream.readUInt32()
            subj = stream.readRawData(subjLen).decode(sys.stdout.encoding)
            predLen = stream.readUInt32()
            pred = stream.readRawData(predLen).decode(sys.stdout.encoding)
            objLen = stream.readUInt32()
            obj = stream.readRawData(objLen).decode(sys.stdout.encoding)
            newStepPort.addProperty((subj, pred, obj))

        return newStepPort

    def addProperty(self, rdftriple):
        self.subj[rdftriple[0]] = rdftriple
        self.pred[rdftriple[1]] = rdftriple
        self.obj[rdftriple[2]] = rdftriple

    def canConnect(self, other):
        if 'pho#workspace#port' in self.subj and 'pho#workspace#port' in other.subj:
            mine = self.subj['pho#workspace#port']
            thiers = other.subj['pho#workspace#port']
            if mine[1] == 'provides' and thiers[1] == 'uses':
                if mine[2] == thiers[2]:
                    return True

        return False


class WorkspaceStep(WorkspaceStepMountPoint):
    '''
    A step that acts like the step plugin duck
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'empty'
        self.ports = []
        self.pixmap = None
        self.configured = False

    def configure(self):
        raise NotImplementedError

    def isConfigured(self):
        return self.configured


#    def serialize(self, stream):
#        name = bytearray(self.name, sys.stdout.encoding)
#        stream.writeUInt32(len(name))
#        stream.writeRawData(name)
#
#        portLen = len(self.ports)
#        stream.writeUInt32(portLen)
#        for port in self.ports:
#            stream = port.serialize(stream)
#
#        stream << self.pixmap

#        return stream

#    @staticmethod
#    def deserialize(newStep, stream):
#        # Clear any legacy information that needs to be removed
#        newStep.name = 'empty'
#        newStep.ports = []
#        newStep.pixmap = QtGui.QPixmap()
#        nameLen = stream.readUInt32()
#        newStep.name = stream.readRawData(nameLen).decode(sys.stdout.encoding)
#
#        portLen = stream.readUInt32()
#        for _ in range(portLen):
#            newStepPort = WorkspaceStepPort()
#            port = WorkspaceStepPort.deserialize(newStepPort, stream)
#            newStep.ports.append(port)
#
#        stream >> newStep.pixmap
#
#        return newStep

    def addPort(self, triple):
        port = WorkspaceStepPort()
        port.addProperty(triple)
        self.ports.append(port)

    def canConnect(self, other):
        # Try to find compatible ports
        for port in self.ports:
            for otherPort in other.ports:
                if port.canConnect(otherPort):
                    return True

        return False

def WorkspaceStepFactory(step_name):
    for step in WorkspaceStepMountPoint.getPlugins():
        if step_name == step.name:
            return step

    raise ValueError
