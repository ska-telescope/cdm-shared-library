.. skeleton documentation master file, created by
   sphinx-quickstart on Thu May 17 15:17:35 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. HOME SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
   :maxdepth: 1
   :caption: ChangeLog
   :hidden:

   CHANGELOG.rst

.. toctree::
  :maxdepth: 3
  :caption: Table of Contents
  :hidden:

  developer/developer
  developer/expand_contract
  developer/centralnode/centralnode
  developer/validation_json
  developer/subarraynode/subarraynode
  developer/mccssubarray/mccssubarray
  developer/mccscontroller/mccscontroller
  client
  package/api
  developer/semantic_validation


=========================
ska-tmc-cdm documentation
=========================

Project description
===================

ska-tmc-cdm provides a Python object model and serialisation library
for resource allocation commands and telescope configuration commands, with a
focus on TMC interfaces with other subsystems.
an ICD support library, intended to be used by the Tango clients and Tango
servers on opposing sides of a telescope control interface.

Status
------

This library supports control and configuration payloads for the following
Tango devices:

* TMC CentralNode
* TMC SubArrayNode
* MCCSController
* MCCSSubArrayNode


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

