.. _MAP-index:

==========
MAP Client
==========

.. _MAP Client: https://simtk.org/home/map

The `MAP Client`_ is a cross-platform framework for managing workflows. MAP Client is a plugin-based application that can be used to create workflows from a collection of workflow steps.  Each workflow step is simply a plugin for the MAP Client which performs a basic task.  Each workflow step is broken down to be as general as possible to make it as reusable by other users and developers. 

One of the central ideas for the MAP Client is to allow users to easily develop and share their own plugins that can be used in a workflow.  The requirements for developing a workflow step have been kept as low as practicable thus allowing plugin creators to concentrate on the practical implementation of the step rather than conforming to the plugin API.  Additionally the Plugin Wizard tool greatly simplifies the first stage in creating a workflow step and generates a considerable amount of the skeleton code required.

Having a plugin based framework makes it possible for groups to share their workflows and workflow steps without requiring a lot of extraneous software.  Also having users create and share their plugins increases the flexibility of the MAP Client and distances users from relying on an external team of developers.

The MAP Client is an application written in Python and based on Qt the cross-platform application and UI framework.  Further details are available in the documents listed below.
 
.. toctree::
   :maxdepth: 1
   
   MAP-install-setup
   MAP-feature-demonstration
   MAP-plugin
   MAP-plugin-wizard
   MAP-tutorial-create
   MAP-tutorial-plugin
   
   glossary
   appendix
   