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

PLUGIN_WRITE_TO_DIRECTORY = '.'
PLUGIN_PACKAGE_NAME = 'abcdstep'
PLUGIN_NAME = 'Abcd'
PLUGIN_IMAGE_FILE = ''

class WizardTestCase(unittest.TestCase):


    def _doCleanUp(self):
        rmdir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, PLUGIN_PACKAGE_NAME)
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


    def testRunWizard(self):
        dlg = wizarddialog.WizardDialog()
        if dlg.exec_() == dlg.Accepted:
            print('accepted')

    def testWizard(self):
        dlg = wizarddialog.WizardDialog()

        p1 = dlg.page(1)
        p1._ui.nameLineEdit.setText(PLUGIN_NAME)
        p2 = dlg.page(2)
        p2._ui.portTableWidget.insertRow(0)
        p2._ui.portTableWidget.setItem(0, 0, QtGui.QTableWidgetItem('provides'))
        p2._ui.portTableWidget.setItem(0, 1, QtGui.QTableWidgetItem('http://my.example.org/1.0/workflowstep#octopus'))
        p3 = dlg.page(3)
        p3._ui.directoryLineEdit.setText(PLUGIN_WRITE_TO_DIRECTORY)

        dlg.accept()

        options = dlg.getOptions()
        self.assertEqual(PLUGIN_NAME, options.getName())
        self.assertEqual(PLUGIN_IMAGE_FILE, options.getImageFile())
        self.assertEqual(PLUGIN_PACKAGE_NAME, options.getPackageName())
        self.assertEqual(PLUGIN_WRITE_TO_DIRECTORY, options.getOutputDirectory())
        self.assertEqual(1, options.portCount())
        self.assertEqual([u'provides', u'http://my.example.org/1.0/workflowstep#octopus'], options.getPort(0))

    def testSkeleton(self):

        options = SkeletonOptions()
        options.setImageFile(PLUGIN_IMAGE_FILE)
        options.setName(PLUGIN_NAME)
        options.setPackageName(PLUGIN_PACKAGE_NAME)
        options.setOutputDirectory(PLUGIN_WRITE_TO_DIRECTORY)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')

        s = Skeleton(options)
        s.write()

        package_dir = os.path.join(PLUGIN_WRITE_TO_DIRECTORY, PLUGIN_PACKAGE_NAME)
        self.assertTrue(os.path.exists(package_dir))
        package_init_file = os.path.join(package_dir, '__init__.py')
        self.assertTrue(os.path.exists(package_init_file))
        step_file = os.path.join(package_dir, PLUGIN_PACKAGE_NAME, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)


        self._doCleanUp()  # Move this to the start of the test if you want to see the output



#         dlg.exec_()



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
