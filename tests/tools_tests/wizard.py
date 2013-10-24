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
import os, unittest
from PySide import QtGui

from tools.pluginwizard import wizarddialog
from tools.pluginwizard.skeleton import SkeletonOptions, Skeleton

if QtGui.qApp == None: QtGui.QApplication([])
import widgets.resources_rc

import alltests

test_path = os.path.join(os.path.dirname(alltests.__file__), 'test_resources', 'wizard_test')

PLUGIN_WRITE_TO_DIRECTORY = test_path
PLUGIN_PACKAGE_NAME = 'abcdalphastep'
PLUGIN_NAME = 'Abcd Alpha'
PLUGIN_IMAGE_FILE = os.path.join(test_path, 'logo.png')
CATEGORY = 'Viewer'
AUTHOR_NAME = 'Prince of Persia'

class WizardTestCase(unittest.TestCase):


    def _doCleanUp(self, package_name):
        rmdir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, package_name)
        if os.path.exists(rmdir):
            directories = []
            for package_dir, _, files in os.walk(rmdir):
                for file_ in files:
                    src_file = os.path.join(package_dir, file_)
                    os.remove(src_file)

                directories.append(package_dir)

            directories.reverse()
            for directory in directories:
                os.rmdir(directory)


    def tearDown(self):
        pass


#     def testRunWizard(self):
#         '''
#         Visual test for wizard, uncomment to manually test.
#         '''
#         dlg = wizarddialog.WizardDialog()
#         result = dlg.exec_()
#         self.assertTrue(result == dlg.Accepted or result == dlg.Rejected)

    def testWizard(self):
        dlg = wizarddialog.WizardDialog()

        p1 = dlg.page(1)
        p1._ui.nameLineEdit.setText(PLUGIN_NAME)
        p1._ui.iconLineEdit.setText(PLUGIN_IMAGE_FILE)
        p2 = dlg.page(2)
        p2._ui.portTableWidget.insertRow(0)
        cb = QtGui.QComboBox()
        cb.addItems(['provides', 'uses'])
        p2._ui.portTableWidget.setCellWidget(0, 0, cb)
        p2._ui.portTableWidget.setItem(0, 1, QtGui.QTableWidgetItem('http://my.example.org/1.0/workflowstep#octopus'))
        p3 = dlg.page(3)
        p3._ui.configTableWidget.setItem(0, 1, QtGui.QTableWidgetItem('xxx'))
        p4 = dlg.page(4)
        p4._ui.authorNameLineEdit.setText(AUTHOR_NAME)
        p4._ui.categoryLineEdit.setText(CATEGORY)
        p5 = dlg.page(5)
        p5._ui.directoryLineEdit.setText(PLUGIN_WRITE_TO_DIRECTORY)

        dlg.accept()

        options = dlg.getOptions()
        self.assertEqual(PLUGIN_NAME, options.getName())
        self.assertEqual(PLUGIN_IMAGE_FILE, options.getImageFile())
        self.assertEqual(PLUGIN_PACKAGE_NAME, options.getPackageName())
        self.assertEqual(PLUGIN_WRITE_TO_DIRECTORY, options.getOutputDirectory())
        self.assertEqual(1, options.portCount())
        self.assertEqual([u'http://physiomeproject.org/workflow/1.0/rdf-schema#provides', u'http://my.example.org/1.0/workflowstep#octopus'], options.getPort(0))
        self.assertEqual(1, options.configCount())
        self.assertEqual([u'identifier', u''], options.getConfig(0))
        self.assertEqual(CATEGORY, options.getCategory())
        self.assertEqual(AUTHOR_NAME, options.getAuthorName())

    def testSkeleton1(self):

        local_package_name = PLUGIN_PACKAGE_NAME.replace('step', str(1) + 'step')

        options = SkeletonOptions()
        options.setImageFile(PLUGIN_IMAGE_FILE)
        options.setName(PLUGIN_NAME + str(1))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(PLUGIN_WRITE_TO_DIRECTORY)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')
        options.addConfig('identifier', '')
        options.setAuthorName(AUTHOR_NAME)
        options.setCategory(CATEGORY)

        s = Skeleton(options)
        s.write()

        package_dir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, local_package_name)
        self.assertTrue(os.path.exists(package_dir))
        package_init_file = os.path.join(package_dir, '__init__.py')
        self.assertTrue(os.path.exists(package_init_file))
        init_contents = open(package_init_file).read()
        self.assertIn(AUTHOR_NAME, init_contents)

        step_file = os.path.join(package_dir, local_package_name, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('return self._config[', file_contents)
        self.assertIn('] = identifier', file_contents)
        self.assertIn('self._category = \'' + CATEGORY + '\'', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)


        resources_file = os.path.join(package_dir, local_package_name, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(package_dir, local_package_name, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))

        config_contents = open(config_file).read()
        self.assertIn('validate', config_contents)

        self._doCleanUp(local_package_name)  # Move this to the start of the test if you want to see the output

    def testSkeleton2(self):

        local_package_name = PLUGIN_PACKAGE_NAME.replace('step', str(2) + 'step')

        options = SkeletonOptions()
        options.setImageFile(PLUGIN_IMAGE_FILE)
        options.setName(PLUGIN_NAME + str(2))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(PLUGIN_WRITE_TO_DIRECTORY)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')

        s = Skeleton(options)
        s.write()

        package_dir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, local_package_name)
        self.assertTrue(os.path.exists(package_dir))
        package_init_file = os.path.join(package_dir, '__init__.py')
        self.assertTrue(os.path.exists(package_init_file))
        step_file = os.path.join(package_dir, local_package_name, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('# TODO: The string must be replaced with', file_contents)
        self.assertIn('# TODO: Must actually set the step', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(package_dir, local_package_name, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        self._doCleanUp(local_package_name)  # Move this to the start of the test if you want to see the output

    def testSkeleton3(self):

        local_package_name = PLUGIN_PACKAGE_NAME.replace('step', str(3) + 'step')

        options = SkeletonOptions()
        options.setImageFile(PLUGIN_IMAGE_FILE)
        options.setName(PLUGIN_NAME + str(3))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(PLUGIN_WRITE_TO_DIRECTORY)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')
        options.addConfig('identifier', '')
        options.addConfig('Cabbage', 'Brown')
        options.addConfig('Path', '')
        options.addConfig('Carrot', 'tis a long way down')

        s = Skeleton(options)
        s.write()

        package_dir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, local_package_name)
        self.assertTrue(os.path.exists(package_dir))
        package_init_file = os.path.join(package_dir, '__init__.py')
        self.assertTrue(os.path.exists(package_init_file))
        step_file = os.path.join(package_dir, local_package_name, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('Cabbage', file_contents)
        self.assertIn('Carrot', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(package_dir, local_package_name, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(package_dir, local_package_name, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))

        self._doCleanUp(local_package_name)  # Move this to the start of the test if you want to see the output

    def testSkeleton4(self):

        local_package_name = PLUGIN_PACKAGE_NAME.replace('step', str(4) + 'step')

        options = SkeletonOptions()
        options.setImageFile(PLUGIN_IMAGE_FILE)
        options.setName(PLUGIN_NAME + str(4))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(PLUGIN_WRITE_TO_DIRECTORY)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')
        options.addConfig('Cabbage', 'Brown')
        options.addConfig('Path', '')
        options.addConfig('Carrot', 'tis a long way down')


        s = Skeleton(options)
        s.write()

        package_dir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, local_package_name)
        self.assertTrue(os.path.exists(package_dir))
        package_init_file = os.path.join(package_dir, '__init__.py')
        self.assertTrue(os.path.exists(package_init_file))
        step_file = os.path.join(package_dir, local_package_name, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('Cabbage', file_contents)
        self.assertIn('Carrot', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(package_dir, local_package_name, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(package_dir, local_package_name, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))

        self._doCleanUp(local_package_name)  # Move this to the start of the test if you want to see the output


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
