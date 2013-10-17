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
from shutil import copyfile
from subprocess import call

QT_RESOURCE_FILENAME = 'resources.qrc'
PYTHON_QT_RESOURCE_FILENAME = 'resources_rc.py'
IMAGES_DIRECTORY = 'images'

class Skeleton(object):
    '''
    This class uses the skeleton options to write the
    skeleton code to disk.
    '''

    def __init__(self, options):
        self._options = options

    def _writePackageInit(self, init_dir):
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

        init_file = os.path.join(init_dir, '__init__.py')
        f = open(init_file, 'w')
        f.write(init_string)
        f.close()

    def _writeStep(self, step_dir):
        class_string = '''
\'\'\'
MAP Client Plugin Step
\'\'\'

from PySide import QtGui

from mountpoints.workflowstep import WorkflowStepMountPoint

class {step_object_name}Step(WorkflowStepMountPoint):
    \'\'\'
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    \'\'\'
'''
        init_string = '''
    def __init__(self, location):
        super({step_object_name}Step, self).__init__('{step_name}', location)
        self._configured = False # A step cannot be executed until it has been configured.
        # Add any other initialisation code here:
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
        step_file = os.path.join(step_dir, 'step.py')
        f = open(step_file, 'w')

        object_name = self._options.getName().replace(' ', '')
        f.write(class_string.format(step_object_name=object_name, step_name=self._options.getName()))
        tmp_string = init_string.format(step_object_name=object_name, step_name=self._options.getName())
        image_filename = self._options.getImageFile()
        if image_filename:
            (_, tail) = os.path.split(image_filename)
            icon_string = '        self._icon =  QtGui.QImage(\':/{step_package_name}/' + IMAGES_DIRECTORY + '/{image_filename}\')\n'
            tmp_string += icon_string.format(step_package_name=self._options.getPackageName(), image_filename=tail)
        port_index = 0
        uses = []
        provides = []
        tmp_string += '''        # Ports:
'''
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

    def _writeStepPackageInit(self, init_dir):
        init_file = os.path.join(init_dir, '__init__.py')
        f = open(init_file, 'w')
        image_filename = self._options.getImageFile()
        if image_filename:
            (package, _) = os.path.splitext(PYTHON_QT_RESOURCE_FILENAME)
            f.write('import ' + package)
        f.close()

    def _createStepIcon(self, step_dir):
        '''
        The step icon requires the creation of directories, resources
        and files if an image file has been specified.
        
        The image file in the options is assumed to exist.
        '''
        image_filename = self._options.getImageFile()
        if image_filename:
            # Create directories
            qt_dir = os.path.join(step_dir, 'qt')
            images_dir = os.path.join(qt_dir, IMAGES_DIRECTORY)
            os.mkdir(qt_dir)
            os.mkdir(images_dir)

            (_, tail) = os.path.split(image_filename)
            # Copy image file
            copyfile(image_filename, os.path.join(images_dir, tail))

            # Create resources file
            resource_file_string = '''
<RCC>
  <qresource prefix="{step_package_name}">
    <file>images/{image_filename}</file>
  </qresource>
</RCC>
'''

            resource_file = os.path.join(qt_dir, QT_RESOURCE_FILENAME)
            f = open(resource_file, 'w')
            f.write(resource_file_string.format(step_package_name=self._options.getPackageName(), image_filename=tail))
            f.close()

            # Generate resources file, I'm going to assume that I can find pyside-rcc
            call(['pyside-rcc', '-o', os.path.join(step_dir, PYTHON_QT_RESOURCE_FILENAME), os.path.join(qt_dir, QT_RESOURCE_FILENAME)])

    def write(self):
        '''
        Write out the step using the options set on initialisation, assumes the output
        directory is writable otherwise an exception will be raised.
        '''
        # Make package directory
        package_dir = os.path.join(self._options.getOutputDirectory(), self._options.getPackageName())
        os.mkdir(package_dir)

        # Write the package init file
        self._writePackageInit(package_dir)

        # Make step pakcage directory
        step_package_dir = os.path.join(package_dir, self._options.getPackageName())
        os.mkdir(step_package_dir)

        # Write step packate init file
        self._writeStepPackageInit(step_package_dir)

        # Write out the step file
        self._writeStep(step_package_dir)

        # Prepare step icon
        self._createStepIcon(step_package_dir)


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

