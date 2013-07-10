.. _MAP-tutorial-plugin:

============================
MAP Tutorial - Create Plugin
============================

.. sectionauthor:: Hugh Sorby

.. _launchpad project: http://launchpad.net/mapclient
.. _MAP: https://simtk.org/home/map

.. note::
   `MAP`_ is currently under active development, and this document will be updated to reflect any changes to the software or new features that are added. You can follow the development of MAP at the `launchpad project`_.

This document details takes the reader through the process of creating a new plugin for the MAP Client.  The :doc:`MAP-create-plugin` document defines the plugin interface that the new plugin must adhere to.

A Simple Source Step Example
============================

We need to create a source step for supplying Zinc model files.  

First copy the skeletonstep directory to another directory.  To make this step our own we first change the skeletonstep name to zincmodelsourcestep.  The places we have to change are:

 #. The topmost directory
 #. The inner directory, this directory is used to namespace our new step.
 #. In __init__.py file in the topmost directory, we also need to uncomment the lines::

     from zincmodelsourcestep import step
     print("Plugin '{0}' version {1} by {2} loaded".format(tail, __version__, __author__))
     
 #. In __init__.py file in the inner directory.  We have to change the name of the class to 'ZincModelSourceStep' and change the name of the step to 'Zinc Model Source'. 

Now we need to be able to configure the step.  To do this we can use qt-designer to create a 'configuredialog.ui' file that we can convert into Python code using 'pyside-uic'.  We want the configuredialog.ui to look like this:

  
