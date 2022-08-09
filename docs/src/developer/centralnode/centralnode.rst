.. _`central_node commands`:

===============
TMC central_node
===============

Overview
========

Sub-array resource allocation is achieved via communication with a TMC
central_node device. The ``central_node`` package models the JSON input and
responses for TMC central_node commands. The contents of this package are
shown in the figure below.

.. figure:: central_node.png
   :align: center
   :alt: High-level overview of central_node package

Classes in the `assign_resources.py`_ module model the arguments for the
``central_node.AssignResources()`` command.

Classes in the `release_resources.py`_ module model the arguments for the
``central_node.ReleaseResources()`` command.

assign_resources.py
===================

.. figure:: assignresources.png
   :align: center
   :alt: Overview of the assign_resources.py module

   assign_resources.py object model

The ``assign_resources.py`` module models the the JSON input and response
for a ``central_node.AssignResources()`` command.

Example JSON input modelled by ``AssignResourcesRequest`` for MID:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-tmc-assignresources/2.0",
    "transaction_id": "txn-mvp01-20200325-00001",
    "subarray_id": 1,
    "dish": {
      "receptor_ids": ["0001", "0002"]
    },
     "sdp": {
        "interface": "https://schema.skao.int/ska-sdp-assignresources/2.0",
        "eb_id": "eb-mvp01-20200325-00001",
        "max_length": 100.0,
        "scan_types": [
          {
            "scan_type_id": "science_A",
            "reference_frame": "ICRS", "ra": "02:42:40.771", "dec": "-00:00:47.84",
            "channels": [{
               "count": 744, "start": 0, "stride": 2, "freq_min": 0.35e9, "freq_max": 1.05e9,
               "link_map": [[1,0], [101,1]]
            }]
          },
          {
            "scan_type_id": "calibration_B",
            "reference_frame": "ICRS", "ra": "12:29:06.699", "dec": "02:03:08.598",
            "channels": [{
              "count": 744, "start": 0, "stride": 2, "freq_min": 0.35e9, "freq_max": 1.05e9,
              "link_map": [[1,0], [101,1]]
            }]
          }
        ],
        "processing_blocks": [
          {
            "pb_id": "pb-mvp01-20200325-00001",
            "workflow": {"kind": "realtime", "name": "vis_receive", "version": "0.1.0"},
            "parameters": {}
          },
          {
            "pb_id": "pb-mvp01-20200325-00002",
            "workflow": {"kind": "realtime", "name": "test_realtime", "version": "0.1.0"},
            "parameters": {}
          },
          {
            "pb_id": "pb-mvp01-20200325-00003",
            "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
            "parameters": {},
            "dependencies": [
              {"pb_id": "pb-mvp01-20200325-00001", "kind": ["visibilities"]}
            ]
          },
          {
            "pb_id": "pb-mvp01-20200325-00004",
            "workflow": {"kind": "batch", "name": "dpreb", "version": "0.1.0"},
            "parameters": {},
            "dependencies": [
              {"pb_id": "pb-mvp01-20200325-00003", "kind": ["calibration"]}
            ]
          }
        ]
      }
  }

Example JSON response modelled by ``AssignResourcesResponse`` for MID:

.. code-block:: JSON

  {
    "dish": {
      "receptor_ids_allocated": ["0001", "0002"]
    }
  }


Example JSON input modelled by ``AssignResourcesRequest`` for LOW:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-low-tmc-assignresources/2.0",
    "subarray_id": 1,
    "mccs": {
        "subarray_beam_ids": [1],
        "station_ids": [[1,2]],
        "channel_blocks": [3]
     }
  }


release_resources.py
====================

.. figure:: releaseresources.png
   :align: center
   :alt: Overview of the release_resources.py module

   release_resources.py object model

The ``release_resources.py`` module models the input JSON for a
``central_node.ReleaseResources()`` command.

Example ReleaseResourcesRequest JSON that requests specific dishes be released
from a sub-array:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "transaction_id": "txn-mvp01-20200325-00001",
    "subarray_id": 1, 
    "receptor_ids": ["0001", "0002"]
  }

Example JSON that requests all sub-array resources be released:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "transaction_id": "txn-mvp01-20200325-00001",
    "subarray_id": 1,
    "release_all": true
  }

Example JSON that requests all sub-array resources be released for LOW:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    "subarray_id": 1,
    "release_all": true
  }
  
telescope_start.py
====================

.. figure:: telescopestart.png
   :align: center
   :alt: Overview of the telescope_start.py module
   :width: 400

   telescope_start.py object model

The ``telescope_start`` module models the input JSON for a
``central_node.StartTelescope()`` command.

Example JSON that requests specific (here id=1) sub array be started:
 # dummy interface link given
.. code-block:: JSON

  {
    "subarray_id": 1, 
    "interface": "https://schema.skao.int/ska-tmc-telescopestart/1.0", 
    "transaction_id":"txn-ts01-20220803-00004"  
  }
