.. _`CentralNode commands`:

===============
TMC CentralNode
===============

Overview
========

Sub-array resource allocation is achieved via communication with a TMC
CentralNode device. The ``centralnode`` package models the JSON input and
responses for TMC CentralNode commands. The contents of this package are
shown in the figure below.

.. figure:: centralnode.png
   :align: center
   :alt: High-level overview of centralnode package

Classes in the `assign_resources.py`_ module model the arguments for the
``CentralNode.AssignResources()`` command.

Classes in the `release_resources.py`_ module model the arguments for the
``CentralNode.ReleaseResources()`` command.

assign_resources.py
===================

.. figure:: assignresources.png
   :align: center
   :alt: Overview of the assign_resources.py module

   assign_resources.py object model

The ``assign_resources.py`` module models the the JSON input and response
for a ``CentralNode.AssignResources()`` command.

Example JSON input modelled by ``AssignResourcesRequest``:

.. code-block:: JSON

  {
    "subarrayID": 1,
    "dish": {
      "receptorIDList": ["0001", "0002"]
    }
  }

Example JSON response modelled by ``AssignResourcesResponse``:

.. code-block:: JSON

  {
    "dish": {
      "receptorIDList_success": ["0001", "0002"]
    }
  }


release_resources.py
====================

.. figure:: releaseresources.png
   :align: center
   :alt: Overview of the release_resources.py module

   release_resources.py object model

The ``release_resources.py`` module models the input JSON for a
``CentralNode.ReleaseResources()`` command.

Example ReleaseResourcesRequest JSON that requests specific dishes be released
from a sub-array:

.. code-block:: JSON

  {
    "subarrayID": 1,
    "dish": {
      "receptorIDList": ["0001", "0002"]
    }
  }

Example JSON that requests all sub-array resources be released:

.. code-block:: JSON

  {
    "subarrayID": 1,
    "releaseALL": true
  }
