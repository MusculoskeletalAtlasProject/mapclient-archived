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
from PyQt4 import QtGui

#import imagesource.Resources_rc
from workspace.WorkspaceStep import WorkspaceStep

class ImageSourceStep(WorkspaceStep):
    '''
    A step satisfies the step plugin duck.
    
    It describes the location of an image/a set of images.
    It can be used as an image source.
    '''
    def __init__(self, manager=None):
        '''
        Constructor
        '''
        super(ImageSourceStep, self).__init__(manager)
        self.name = 'Image source'
        self.pixmap = QtGui.QPixmap(':/imagesource/icons/landscapeimages.png')
        self.addPort(('pho#workspace#port', 'provides', 'images'))
        if self.manager:
            self.manager.addStep(self)

    def configure(self):
        print('configure image source step')

