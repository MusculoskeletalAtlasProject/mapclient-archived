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
VERSION_MAJOR       = 0
VERSION_MINOR       = 2
VERSION_PATCH       = 0
VERSION_STRING      = str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_PATCH)
GPL_VERSION         = '3'
APPLICATION_NAME    = 'MAP Client'
ORGANISATION_NAME   = 'Musculo Skeletal'
ORGANISATION_DOMAIN = 'musculoskeletal.org' 

# Contributors list
HS = {'name': 'Hugh Sorby', 'email': 'h.sorby@auckland.ac.nz'}

CREDITS = {
           'programming'  : [HS],
           'artwork'      : [HS],
           'documentation': [HS]
           }

ABOUT = {
         'name'       : APPLICATION_NAME,
         'version'    : VERSION_STRING,
         'license'    : 'GNU GPL v.' + GPL_VERSION,
         'description': 'Create and manage detailed musculoskeletal models for OpenSim.'
         }

# APPLICATION
WORKSPACE_NAME = 'workspace.conf'