.. _MAP-feature-demonstration:

==========================
MAP Features Demonstration
==========================

.. sectionauthor:: Hugh Sorby

.. _MAP: https://simtk.org/home/map
.. _launchpad project: http://launchpad.net/mapclient
.. _physiome: http://physiomeproject.org/zinclibrary
.. _project downloads: https://launchpad.net/mapclient/+download

.. note::
   `MAP`_ is currently under active development, and this document will be updated to reflect any changes to the software or new features that are added. You can follow the development of MAP at the `launchpad project`_.

This document details the features of `MAP`_, a cross-platform framework for managing workflows. MAP is a plugin-based application that can be used to create workflows from a collection of workflow steps.

In this demonstration is based on version 0.9.0 of MAP, available from the `project downloads`_. Directions for installing MAP and getting the MAP plugins are available in the :ref:`MAP-install-setup`.

In this demonstration we will cover the features of MAP.  We will start with a quick tour and then create a new workflow that will help us segment a region of interest from a stack of images.

Quick Tour
==========

When you first load MAP, it will look something like this:

.. figure:: /MAP/images/blank_MAP_1.png
   :align: center
   :width: 75%

In the main window we can see three distinct areas that make up the workflow management side of the software.  These three areas are the menu bar (at the top), the step box (on the left) that contains the steps that you can use to create your workflow and the workflow canvas (on the right) an area for constructing a workflow.

In the Step box we will only see two steps, this is because we have only loaded the default Steps and not loaded any of the external plugins that MAP can use.

Menu Bar
--------

The Menu bar provides a selection of drop down menus for accessing the applications functions.  The File menu provides access to opening, importing, closing workspaces as well as quitting the application.  The Edit menu provides access to the undo/redo functionality.  The Tools menu provides access to the Plugin Manager tool, Physiome Model Repository (PMR) tool and the Annotation tool.  The Help menu provides access to the about box which contains information on contributors and the license that the MAP application is released under.

Step Box
--------

The Step box provides a selection of steps that are available to construct a workflow from.  The first time we start the program only the default plugins are available.  To add more steps we can use the Plugin Manager tool.  To use a step in our workflow we drag the desired step from the step box onto the workflow canvas.

Workflow canvas
---------------

The workflow canvas is where we construct our workflow.  We do this by adding the steps to the workflow canvas from the step box that make up our workflow.  We then make connections between the workflow steps to define the complete workflow.

When a step is added to the workflow the icon which is visible in the Step box is augmented with visualisations of the Steps ports and the steps configured status.  The annotation of the steps ports will show when the mouse is hovered over a port.  The image below shows the Image Source step with the annotation for the port displayed.

.. figure:: /MAP/images/step_with_port_info_displayed_1.png
   :align: center
   :width: 40%
  
Tools
=====

MAP currently has three tools that may be used to aide the management of the workflow.  They are the Plugin Manager tool, the Physiome Model Repository (PMR) tool and the Annotation tool.  For a description of each tool see the relevant sections.

.. _MAP-plugin-manager-tool:

Plugin Manager Tool
-------------------

The plugin tool is a simple tool that enables the user to add or remove additional plugin directories.  MAP comes with some default plugins which the user can decide to load or not.  External directories are added with the add directory button.  Directories are removed by selecting the required directory in the Plugin directories list and clicking the remove directory button.

Whilst additions to the plugin path will be visible immediately in the Step box deletions will not be apparent until the next time the MAP Client is started.  This behaviour is a side-effect of the Python programming language.  

.. figure:: /MAP/images/plugin_manager_1.png
   :align: center
   :width: 25%
  

Physiome Model Repository (PMR) Tool
------------------------------------

The PMR tool uses webservices and OAuth to communicate between itself (the consumer) and the PMR website (the server).  Using this tool we can search for and find suitable resources on PMR.

The PMR website uses OAuth to authenticate a consumer and determine consumer access privileges.  Here we will discuss the parts of OAuth that are relevant to getting you (the user) able to access resources on PMR.

In OAuth we have three players the server, the consumer and the user.  The server is providing a service that the consumer wishes to use.  It is up to the user to allow the consumer access to the servers resources and set the level of access to the resource.  For the the consumer to access privileged information of the user stored on the server the user must register the consumer with the server, this is done by the user giving the consumer a temporary access token.  This temporary access token is then used by the consumer to finalise the transaction and acquire a permanent access token.  The user can deny the consumer access at anytime by logging into the server and revoking the permanent access token.

If you want the PMR tool to have access to privileged information (your non-public workspaces stored on PMR) you will need to register the PMR tool with the PMR website.  We do this by clicking on the `register` link as shown in the figure below.  This does two things: it shows the Application Authorisation dialog; opens a webbrowser at the PMR website.  [If you are not logged on at the PMR website you will need to do so now to continue, instructions on obtaining a PMR account are availble here XXXXX].  On the PMR website you are asked to either accept or deny access to the PMR tool.  If you allow access then the website will display a temporary access token that you will need to copy and paste into the Application Authorisation dialog so that the PMR tool can get the permanent access token.

.. figure:: /MAP/images/PMRTool_1.png
   :align: center
   :width: 25%

Annotation Tool
---------------

The Annotation tool is a very simple tool to help a user annotate the Workflow itself and the Step data directories that are linked to PMR.  At this stage there is a limited vocabulary that the Annotation tool knows about, but this is intended to be extended in coming releases.  The vocabulary that the annotation is aware of is available in the three combo-boxes near the top of the dialog.

.. figure:: /MAP/images/top_annotation_1.png
   :align: center
   :width: 40%

The main part of the Annotation tool shows the current annotation from the current target.  

.. figure:: /MAP/images/main_annotation_1.png
   :align: center
   :width: 25%

In the above image we can see the list of annotations that have been added to the current target.  This is a simplified view of the annotation with the prefix of the terms removed for clarity.
