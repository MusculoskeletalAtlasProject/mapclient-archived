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

from core import pluginframework

class WorkflowStepPort(object):
    '''
    Describes the location and properties of a port for a workflow step.
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
        if 'pho#workflow#port' in self.subj and 'pho#workflow#port' in other.subj:
            myPorts = self.subj['pho#workflow#port']
            thierPorts = other.subj['pho#workflow#port']
            mineProvides = [triple for triple in myPorts if 'provides' == triple[1]]
            thiersUses = [triple for triple in thierPorts if 'uses' == triple[1]]
            for mine in mineProvides:
                for thiers in thiersUses:
                    if mine[2] == thiers[2]:
                        return True

        return False

'''
Plugins can inherit this mount point to add a workflow step.

A plugin that registers this mount point must have:
  - An attribute _icon that is a QImage icon for a visual representation of the step
  - Implement a function 'configure'
  - Implement a function 'setIdentifier'
  - Implement a function 'getIdentifier'
  - Implement a function 'serialize'
  - Implement a function 'deserialize'


A plugin that registers this mount point could have:
  - An attribute _name that is a string representation of the name
  - An attribute _category that is a string representation of the step's category
  
'''
#class WorkflowStep(WorkflowStepMountPoint):
#    '''
#    A step that acts like the step plugin duck
#    '''
#

def _workflow_step_init(self):
    '''
    Constructor
    '''
    self._location = None
    self._ports = []
    self._icon = None
    self._configured = False
    self._configuredObserver = None
    self._doneExecution = None

def _workflow_step_execute(self):
    print('executing: ' + self.getName())
    self._doneExecution()

def _workflow_step_registerDoneExecution(self, observer):
    self._doneExecution = observer

def _workflow_step_configure(self, location):
    raise NotImplementedError

def _workflow_step_getIdentifier(self):
    raise NotImplementedError

def _workflow_step_setIdentifier(self):
    raise NotImplementedError

def _workflow_step_serialize(self):
    raise NotImplementedError

def _workflow_step_deserialize(self):
    raise NotImplementedError

def _workflow_step_isConfigured(self):
    return self._configured

def _workflow_step_registerConfiguredObserver(self, observer):
    self._configuredObserver = observer

def _workflow_step_addPort(self, triple):
    port = WorkflowStepPort()
    port.addProperty(triple)
    self._ports.append(port)

def _workflow_step_canConnect(self, other):
    # Try to find compatible ports
    for port in self._ports:
        for otherPort in other._ports:
            if port.canConnect(otherPort):
                return True

    return False

def _workflow_step_getName(self):
    if hasattr(self, '_name'):
        return self._name
    
    return self.__class__.__name__

attr_dict = {'_category': 'General'}
attr_dict['__init__'] = _workflow_step_init
attr_dict['execute'] = _workflow_step_execute
attr_dict['registerDoneExecution'] = _workflow_step_registerDoneExecution
attr_dict['configure'] = _workflow_step_configure
attr_dict['isConfigured'] = _workflow_step_isConfigured
attr_dict['registerConfiguredObserver'] = _workflow_step_registerConfiguredObserver
attr_dict['addPort'] = _workflow_step_addPort
attr_dict['canConnect'] = _workflow_step_canConnect
attr_dict['getName'] = _workflow_step_getName
attr_dict['deserialize'] = _workflow_step_deserialize
attr_dict['serialize'] = _workflow_step_serialize

WorkflowStepMountPoint = pluginframework.MetaPluginMountPoint('WorkflowStepMountPoint', (object,), attr_dict)

def workflowStepFactory(step_name):
    for step in WorkflowStepMountPoint.getPlugins():
        if step_name == step.getName():
            return step
        
    raise ValueError('Failed to find step named: ' + step_name)


