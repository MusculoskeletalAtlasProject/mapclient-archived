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
from workspace.MountPoint import WorkspaceStepMountPoint

class WorkspaceStepPort(object):
    '''
    Describes the location and properties of a port for a workspace step.
    '''
    def __init__(self):
        self.subj = {}
        self.pred = {}
        self.obj = {}

    def addProperty(self, rdftriple):
        if rdftriple[0] in self.subj:
            self.subj[rdftriple[0]].append(rdftriple)
        else:
            self.subj[rdftriple[0]] = [rdftriple]

        if rdftriple[1] in self.pred:
            self.pred[rdftriple[1]].append(rdftriple)
        else:
            self.pred[rdftriple[1]] = [rdftriple]

        if rdftriple[2] in self.obj:
            self.obj[rdftriple[2]].append(rdftriple)
        else:
            self.obj[rdftriple[2]] = [rdftriple]

    def getTriplesForObj(self, obj):
        if obj in self.obj:
            return self.obj[obj]

        return []
#        return [triple[2] for triple in self.obj[obj]]

    def getTriplesForPred(self, pred):
        if pred in self.pred:
            return self.pred[pred]

        return []
#        return [triple for triple in self.pred[pred]]

    def canConnect(self, other):
        if 'pho#workspace#port' in self.subj and 'pho#workspace#port' in other.subj:
            myPorts = self.subj['pho#workspace#port']
            thierPorts = other.subj['pho#workspace#port']
            mineProvides = [triple for triple in myPorts if 'provides' == triple[1]]
            thiersUses = [triple for triple in thierPorts if 'uses' == triple[1]]
            for mine in mineProvides:
                for thiers in thiersUses:
                    if mine[2] == thiers[2]:
                        return True

        return False


class WorkspaceStep(WorkspaceStepMountPoint):
    '''
    A step that acts like the step plugin duck.  Takes an optional manager argument 
    that implements a function addStep.  Any derived WorkspaceStep must call the manager.addStep
    function (if the manager exists) at the end of it's initialisation if it wants to be visible.
    '''

    def __init__(self, manager=None):
        '''
        Constructor
        '''
        self.manager = manager
        self.name = 'empty'
        self.ports = []
        self.pixmap = None
        self.configured = False

    def configure(self):
        raise NotImplementedError

    def isConfigured(self):
        return self.configured

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

def WorkspaceStepFactory(step_name, *args, **kwargs):
    for step in WorkspaceStepMountPoint.getPlugins(*args, **kwargs):
        if step_name == step.name:
            return step

    raise ValueError
