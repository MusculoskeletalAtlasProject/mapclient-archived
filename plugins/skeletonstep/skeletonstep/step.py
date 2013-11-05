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

from mountpoints.workflowstep import WorkflowStepMountPoint

class SkeletonStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be used as a starting point
    for new steps.
    '''

    def __init__(self, location):
        super(SkeletonStep, self).__init__('Skeleton', location)

    def configure(self):
        pass

    def getIdentifier(self):
        return 'skeleton'

    def setIdentifier(self, identifier):
        pass

    def serialize(self, location):
        pass

    def deserialize(self, location):
        pass

