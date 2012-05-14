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

import os, sys, imp

def listPyFiles(directories):
    l = list()
    for dirName in directories:

        for dirEntry in os.listdir(dirName):

            absDirEntry = os.path.join(dirName, dirEntry)
            if os.path.isfile(absDirEntry):
                rootname, ext = os.path.splitext(dirEntry)
                if ext == '.py':
                    absfile = os.path.join(dirName, rootname)
                    l.append(absfile)
    
    return l

def listPlugins(pluginDir):
    '''
    Utility method to list available plugins
    '''
    l = list()
    for dirEntry in os.listdir(pluginDir):

        absDirEntry = os.path.join(pluginDir, dirEntry)
        if os.path.isfile(absDirEntry):
            rootname, ext = os.path.splitext(dirEntry)
            if ext == '.py':
                absfile = os.path.join(pluginDir, rootname)
                l.append(absfile)

    return l

def loadPlugins(pluginDir, **kwargs):
    '''
    Utility method to load all plugins found in pluginDir.  Adds the plugin
    directory to the current path.
    '''

    plugins = listPlugins(pluginDir)

    if pluginDir not in sys.path:
        sys.path.append(pluginDir)

    loaded_plugins = {}
    for plugin in plugins:
        pluginName = os.path.basename(plugin)
        pluginDir = os.path.dirname(plugin)
        
        fp, path, description = imp.find_module(pluginName, [pluginDir])
        module = imp.load_module(pluginDir, fp, path, description)
        moduleVersion = '-.-.-'
        if hasattr(module, '__version__'):
            moduleVersion = module.__version__
        moduleAuthor = '?'
        if hasattr(module, '__author__'):
            moduleAuthor = module.__author__
        print("Plugin '{}' ver {} by {} loaded".format(pluginName, moduleVersion, moduleAuthor))
        loaded_plugins[pluginName] = module

        try:
            pass
        except:
            # non modules will fail
            print("Plugin '{}' not loaded".format(pluginName))
        finally:
            if fp:
                fp.close()
              
    if len(loaded_plugins) == 0:
        sys.path.remove(pluginDir)
        
    return loaded_plugins


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
        return [p() for p in self.mount.plugins]



class MetaPluginMountPoint(type):
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

    For compatibility across python 2.x and python 3.x we must construct the PluginMountPoint
    classes like so:
    MyPlugin = MetaPluginMountPoint('MyPlugin', (object, ), {})
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
            
    def getPlugins(self, *args, **kwargs):
        return [p(*args, **kwargs) for p in self.plugins]
       

# Plugin mount points are defined below.
# For running in both python 2.x and python 3.x we must follow the example found
# at http://mikewatkins.ca/2008/11/29/python-2-and-3-metaclasses/
from PyQt4.QtCore import QObject

MetaQObject = type(QObject)

# For multiple inheritance in classes we also need to create a metaclass that also
# inherits from the metaclasses of the inherited classes
class MetaQObjectPluginMountPoint(MetaQObject, MetaPluginMountPoint):

    def __init__(self, name, bases, attrs):
        MetaPluginMountPoint.__init__(self, name, bases, attrs)
        MetaQObject.__init__(self, name, bases, attrs)
 
'''
Plugins can inherit this mount point in order to add to the menu of the GUI.

 A plugin that registers this mount point must have attributes
 * menuLabel
 * menuName
 * actionLabel
 
 A plugin that registers this mount point could have attributes
 * subMenuLabel
 * subMenuName
 * shortcut
 * statustip
  
 It must implement
 * def execute(self):
 
 And it must call
 * QObject.__init__(self)
 in it's __init__ function
 '''  
MenuOption = MetaQObjectPluginMountPoint('MenuOption', (QObject, ), {'subMenuLabel': None, 'subMenuName': None, 'shortcut': None, 'statustip': ''})

