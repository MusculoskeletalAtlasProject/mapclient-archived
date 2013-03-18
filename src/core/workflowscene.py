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
import os

from PyQt4 import QtCore

from mountpoints.workflowstep import workflowStepFactory


class Item(object):
    
    
    def __init__(self):
        self._selected = True
        
    def selected(self):
        return self._selected
    
    
class MetaStep(Item):
    
    
    Type = 'Step'
    
    def __init__(self, step):
        Item.__init__(self)
        self._step = step
        self._pos = QtCore.QPoint(0, 0)
        
    def pos(self):
        return self._pos

class Connection(Item):
    
    
    Type = 'Connection'

    def __init__(self, source, destination):
        Item.__init__(self)
        self._source = source
        self._destination = destination
        
    def source(self):
        return self._source
    
    def destination(self):
        return self._destination


class WorkflowDependencyGraph(object):
    
    
    def __init__(self, scene):
        self._scene = scene
    
    def canExecute(self):
        can = False
        for item in self._scene.items():
            if item.Type == Connection.Type:
                can = True

        return can
    
    
class WorkflowScene(object):
    '''
    This is the authoratative model for the workflow scene.
    '''
    
    
    def __init__(self, manager):
        self._manager = manager
        self._items = {}
        self._dependencyGraph = WorkflowDependencyGraph(self)

    def saveState(self, ws):
        connectionMap = {}
        connectionSelectionMap = {}
        stepList = []
        for item in self._items:
            if item.Type == MetaStep.Type:
                stepList.append(item)
            elif item.Type == Connection.Type:
                connectionSelectionMap[item.source()] = item.selected()
                if item.source() in connectionMap:
                    connectionMap[item.source()].append(item.destination())
                else:
                    connectionMap[item.source()] = [item.destination()]

        location = self._manager.location()
        ws.remove('nodes')
        ws.beginGroup('nodes')
        ws.beginWriteArray('nodelist')
        nodeIndex = 0
        for metastep in stepList:
            if metastep._step.isConfigured():
                step_location = os.path.join(location, metastep._step.getIdentifier())
                metastep._step.serialize(step_location)
            ws.setArrayIndex(nodeIndex)
            ws.setValue('name', metastep._step.getName())
            ws.setValue('position', metastep._pos)
            ws.setValue('selected', metastep._selected)
            ws.setValue('identifier', metastep._step.getIdentifier())
            ws.beginWriteArray('connections')
            connectionIndex = 0
            if metastep in connectionMap:
                for destination in connectionMap[metastep]:
                    ws.setArrayIndex(connectionIndex)
                    ws.setValue('connectedTo', stepList.index(destination))
                    ws.setValue('selected', connectionSelectionMap[metastep])
                    connectionIndex += 1
            ws.endArray()
            nodeIndex += 1
        ws.endArray()
        ws.endGroup()

    def loadState(self, ws):
        self.clear()
        location = self._manager.location()
        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        metaStepList = []
        edgeConnections = []
        for i in range(nodeCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            position = ws.value('position')
            selected = ws.value('selected', 'false') == 'true'
            identifier = ws.value('identifier')
            step = workflowStepFactory(name)
            step.setIdentifier(identifier)
            step.deserialize(location)
            metastep = MetaStep(step)
            metastep._pos = position
            metastep._selected = selected
            metaStepList.append(metastep)
            self.addItem(metastep)
            edgeCount = ws.beginReadArray('connections')
            for j in range(edgeCount):
                ws.setArrayIndex(j)
                connectedTo = int(ws.value('connectedTo'))
                selected = ws.value('selected', 'false') == 'true'
                edgeConnections.append((i, connectedTo, selected))
            ws.endArray()
        ws.endArray()
        ws.endGroup()
        for edge in edgeConnections:
            node1 = metaStepList[edge[0]]
            node2 = metaStepList[edge[1]]
            c = Connection(node1, node2)
            c._selected = edge[2]
            self.addItem(c)

    def manager(self):
        return self._manager
    
    def canExecute(self):
        return self._dependencyGraph.canExecute()
    
    def clear(self):
        self._items.clear()
    
    def items(self):
        return self._items.keys()
    
    def addItem(self, item):
        self._items[item] = item
    
    def removeItem(self, item):
        print(item in self._items)
        if item in self._items:
            del self._items[item]
            
        print(self._items)
    
    def setItemPos(self, item, pos):
        if item in self._items:
            self._items[item]._pos = pos
    
    def setItemSelected(self, item, selected):
        if item in self._items:
            self._items[item]._selected = selected
    
    
