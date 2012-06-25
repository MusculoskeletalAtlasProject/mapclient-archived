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
from core.PluginFramework import ToolMountPoint
from pmr2register.RegisterDialog import RegisterDialog

class RegisterTool(ToolMountPoint):

    def __init__(self, menu_Tool, parent):
        self.parent = parent
        # add action to menu
        lastMenuAction = None
        if menu_Tool.actions():
            lastMenuAction = menu_Tool.actions()[-1]

        action_Register = QtGui.QAction('&PMR Register', menu_Tool)
        action_Register.setObjectName('action_Register')
        action_Register.triggered.connect(self.onRegister)
        menu_Tool.insertAction(lastMenuAction, action_Register)

    def onRegister(self):
        dlg = RegisterDialog(self.parent)
        dlg.show()
        dlg.exec_()


