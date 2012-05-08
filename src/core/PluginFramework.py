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

'''
Inspired by Marty Alchin's Simple plugin framework.
http://martyalchin.com/2008/jan/10/simple-plugin-framework/
'''

import os, imp

def loadPlugins(pluginDir=None):
    '''
    Utility method to load all plugins found in pluginDir.  By default loads 
    plugins in the src/plugin directory if no pluginDir is given.
    '''
    if pluginDir is None:
        fileDir = os.path.dirname(__file__)
        pluginDir = os.path.realpath(fileDir + '/../plugins')

    for dirList in os.listdir(pluginDir):
        if (os.path.isfile(dirList)):
            continue
        try :
            filename, path, description = imp.find_module(dir, [pluginDir])
            module = imp.load_module(dir, filename, path, description)
            print("Plugin {} v{} by {} loaded".format(dir, module.__version__, module.__author__))
        except :
            # non modules will fail
            # print(sys.exc_info()[1])
            pass


class PluginsAt(object):
    '''
    Descriptor to get plugins on a given mount point.
    '''
    def __init__(self, mount_point):
        '''
        Initialise the descriptor with the mount point wanted.
        Eg: PluginsAt(PluginFramework.MenuOption) to get extensions that change the GUI Menu.
        '''
        self.mount = mount_point

    def __get__(self, instance, owner=None):
        '''
        Plugins are instantiated with the object that is calling them.
        '''
        return [p(instance) for p in self.mount.plugins]



class MountPoint(type):
    '''
    * A way to declare a mount point for plugins. Since plugins are an example 
      of loose coupling, there needs to be a neutral location, somewhere between
      the plugins and the code that uses them, that each side of the system can
      look at, without having to know the details of the other side. Trac calls
      this is an 'extension point'.
    * A way to register a plugin at a particular mount point. Since internal code
      can't (or at the very least, shouldn't have to) look around to find plugins 
      that might work for it, there needs to be a way for plugins to announce their
      presence. This allows the guts of the system to be blissfully ignorant of 
      where the plugins come from; again, it only needs to care about the mount point.
    * A way to retrieve the plugins that have been registered. Once the plugins 
      have done their thing at the mount point, the rest of the system needs to
      be able to iterate over the installed plugins and use them according to its need.

    Add the parameter `metaclass = MountPoint` in any class to make it a mount point.
    '''

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)
       

# Plugin mount points are defined below.
class MenuOption(object):
    '''
    Plugins can inherit this mount point in order to amending the menu of the GUI.

     A plugin that registers this mount point must have attributes
     * label
     * command
     
     It must implement
     def execute(self):
     '''
    __metaclass__ = MountPoint
    
    def __init__(self):
        pass





