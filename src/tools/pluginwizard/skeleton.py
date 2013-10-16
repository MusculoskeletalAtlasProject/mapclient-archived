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

class Skeleton(object):
    '''
    This class uses the skeleton options to write the
    skeleton code to disk.
    '''

    def __init__(self, options):
        self._options = options

    def _writePackageInit(self):
        init_string = '''
\'\'\'
MAP Client Plugin
\'\'\'
__version__ = '0.1.0'
__author__ = 'Xxxx Yyyyy'

import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    # Using __file__ will not work if py2exe is used,
    # Possible problem of OSX10.6 also.
    sys.path.insert(0, current_dir)

# import class that derives itself from the step mountpoint.
from {package_name} import step

( _, tail ) = os.path.split(current_dir)
print("Plugin '{{0}}' version {{1}} by {{2}} loaded".format(tail, __version__, __author__))

'''.format(package_name=self._options.getPackageName())

        init_file = os.path.join(self._options.getOutputDirectory(), self._options.getPackageName(), '__init__.py')
        f = open(init_file, 'w')
        f.write(init_string)
        f.close()

    def _writeStep(self):
        class_string = '''
\'\'\'
MAP Client Plugin Step
\'\'\'

from mountpoints.workflowstep import WorkflowStepMountPoint

class {step_name}Step(WorkflowStepMountPoint):
    \'\'\'
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    \'\'\'
'''
        init_string = '''
    def __init__(self, location):
        super({step_name}Step, self).__init__('{step_name}', location)
        self._configured = False # A step cannot be executed until it has been configured.
        # Add any other initialisation code here:
        # Like ports:
'''

        method_string = '''
    def configure(self):
        \'\'\'
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        \'\'\'
        pass

    def getIdentifier(self):
        \'\'\'
        The identifier is a string that must be unique within a workflow.
        \'\'\'
        return '' # TODO: The empty string must be replaced with the step's identifier

    def setIdentifier(self, identifier):
        \'\'\'
        The framework will set the identifier for this step when it is loaded.
        \'\'\'
        pass # TODO: Must actually set the step's identifier here

    def serialize(self, location):
        \'\'\'
        Add code to serialize this step to disk.  The filename should
        use the step identifier (received from getIdentifier()) to keep it
        unique within the workflow.  The suggested name for the file on
        disk is:
            filename = getIdentifier() + '.conf'
        \'\'\'
        pass

    def deserialize(self, location):
        \'\'\'
        Add code to deserialize this step from disk.  As with the serialize 
        method the filename should use the step identifier.  Obviously the 
        filename used here should be the same as the one used by the
        serialize method.
        \'\'\'
        pass

'''
        step_file = os.path.join(self._options.getOutputDirectory(), self._options.getPackageName(), self._options.getPackageName(), 'step.py')
        f = open(step_file, 'w')

        f.write(class_string.format(step_name=self._options.getName()))
        tmp_string = init_string.format(step_name=self._options.getName())
        port_index = 0
        uses = []
        provides = []
        while port_index < self._options.portCount():
            current_port = self._options.getPort(port_index)
            tmp_string += '''        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      '{0}',
                      '{1}'))\n'''.format(current_port[0], current_port[1])
            if current_port[0].endswith('uses'):
                uses.append(current_port[1])
            elif current_port[0].endswith('provides'):
                provides.append(current_port[1])
            port_index += 1

        uses_count = len(uses)
        if uses_count > 0:
            uses_index = 0
            tmp_string += '\n    def execute(self, '
            while uses_index < uses_count:
                uses_index += 1
                tmp_string += 'dataIn{0}'.format(uses_index)
                if uses_index != uses_count:
                    tmp_string += ', '
            tmp_string += '''):
        \'\'\'
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        \'\'\'
        self._doneExecution()
'''
        provides_count = len(provides)
        if provides_count > 0:
            provides_index = 0
            tmp_string += '''
    def portOutput(self):
        \'\'\'
        Add your code here that will return the appropriate objects for this step.
        The objects must be returned in the *order* they are specified in 
        the port list.
        \'\'\'
'''
            init_out_string = ''
            return_string = '        return '
            while provides_index < provides_count:
                provides_index += 1
                if provides_count > 1 and provides_index == 1:
                    return_string += '['
                return_string += 'dataOut{0}'.format(provides_index)
                init_out_string += '        dataOut{0} = None # {1}\n'.format(provides_index, provides[provides_index - 1])
                if provides_count > 1 and provides_index != provides_count:
                    return_string += ', '

            if provides_count > 1:
                return_string += ']'

            tmp_string += init_out_string + return_string + '\n'

        f.write(tmp_string)
        f.write(method_string)
        f.close()

    def write(self):
        package_dir = os.path.join(self._options.getOutputDirectory(), self._options.getPackageName())
        os.mkdir(package_dir)

        self._writePackageInit()

        step_package_dir = os.path.join(package_dir, self._options.getPackageName())
        os.mkdir(step_package_dir)
        step_package_init_file = os.path.join(step_package_dir, '__init__.py')
        f = open(step_package_init_file, 'w')
        f.close()

        self._writeStep()


class SkeletonOptions(object):
    '''
    This class hold all the options for the skeleton plugin code.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._name = ''
        self._packageName = ''
        self._imageFile = ''
        self._outputDirectory = ''
        self._ports = []

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getPackageName(self):
        return self._packageName

    def setPackageName(self, packageName):
        self._packageName = packageName

    def getImageFile(self):
        return self._imageFile

    def setImageFile(self, imageFile):
        self._imageFile = imageFile

    def getOutputDirectory(self):
        return self._outputDirectory

    def setOutputDirectory(self, outputDirectory):
        self._outputDirectory = outputDirectory

    def portCount(self):
        return len(self._ports)

    def getPort(self, index):
        return self._ports[index]

    def addPort(self, predicate, port_object):
        self._ports.append([predicate, port_object])

