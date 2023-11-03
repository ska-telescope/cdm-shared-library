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

Example PI16 JSON input modelled by ``AssignResourcesRequest`` for MID:

.. code-block:: JSON

    {
       "interface":"https://schema.skao.int/ska-tmc-assignresources/2.1",
       "transaction_id":"txn-....-00001",
       "subarray_id":1,
       "dish":{
          "receptor_ids":[
             "0001"
          ]
       },
       "sdp":{
          "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",
          "resources":{
             "receptors":[
                "SKA001",
                "SKA002",
                "SKA003",
                "SKA004"
             ]
          },
          "execution_block":{
             "eb_id":"eb-test-20220916-00000",
             "context":{

             },
             "max_length":3600.0,
             "beams":[
                {
                   "beam_id":"vis0",
                   "function":"visibilities"
                }
             ],
             "scan_types":[
                {
                   "scan_type_id":".default",
                   "beams":{
                      "vis0":{
                         "channels_id":"vis_channels",
                         "polarisations_id":"all"
                      }
                   }
                },
                {
                   "scan_type_id":"target:a",
                   "derive_from":".default",
                   "beams":{
                      "vis0":{
                         "field_id":"field_a"
                      }
                   }
                },
                {
                   "scan_type_id":"calibration:b",
                   "derive_from":".default",
                   "beams":{
                      "vis0":{
                         "field_id":"field_b"
                      }
                   }
                }
             ],
             "channels":[
                {
                   "channels_id":"vis_channels",
                   "spectral_windows":[
                      {
                         "spectral_window_id":"fsp_1_channels",
                         "count":4,
                         "start":0,
                         "stride":2,
                         "freq_min":350000000.0,
                         "freq_max":368000000.0,
                         "link_map":[
                            [
                               0,
                               0
                            ],
                            [
                               200,
                               1
                            ],
                            [
                               744,
                               2
                            ],
                            [
                               944,
                               3
                            ]
                         ]
                      }
                   ]
                }
             ],
             "polarisations":[
                {
                   "polarisations_id":"all",
                   "corr_type":[
                      "XX",
                      "XY",
                      "YX",
                      "YY"
                   ]
                }
             ],
             "fields":[
                {
                   "field_id":"field_a",
                   "phase_dir":{
                      "ra":[
                         123.0
                      ],
                      "dec":[
                         -60.0
                      ],
                      "reference_time":"...",
                      "reference_frame":"ICRF3"
                   },
                   "pointing_fqdn":"..."
                },
                {
                   "field_id":"field_b",
                   "phase_dir":{
                      "ra":[
                         123.0
                      ],
                      "dec":[
                         -60.0
                      ],
                      "reference_time":"...",
                      "reference_frame":"ICRF3"
                   },
                   "pointing_fqdn":"..."
                }
             ]
          },
          "processing_blocks":[
             {
                "pb_id":"pb-test-20220916-00000",
                "script":{
                   "kind":"realtime",
                   "name":"test-receive-addresses",
                   "version":"0.5.0"
                },
                "sbi_ids":[
                   "sbi-test-20220916-00000"
                ],
                "parameters":{

                }
             }
          ]
       }
    }

For PI14 JSON, Please `refer confluence schema page <https://confluence.skatelescope.org/display/SWSI/Configuration+Schemas>`_

Example JSON response modelled by ``AssignResourcesResponse`` for MID:

.. code-block:: JSON

  {
    "dish": {
      "receptor_ids_allocated": ["0001", "0002"]
    }
  }


Example PI 17 JSON input modelled by ``AssignResourcesRequest`` for LOW:

.. code-block:: JSON

  {
   "interface": "https://schema.skao.int/ska-low-tmc-assignresources/3.2",
   "transaction_id": "txn-....-00001",
   "subarray_id": 1,
   "mccs": {
      "interface": "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0",
      "subarray_beams": [
         {
         "subarray_beam_id": 1,
         "apertures": [
            {
               "station_id": 1,
               "aperture_id": "AP001.01"
            },
            {
               "station_id": 1,
               "aperture_id": "AP001.02"
            },
            {
               "station_id": 2,
               "aperture_id": "AP002.01"
            },
            {
               "station_id": 2,
               "aperture_id": "AP002.02"
            },
            {
               "station_id": 3,
               "aperture_id": "AP003.01"
            }
         ],
         "number_of_channels": 32
         }
      ]
   },
   "sdp": {
      "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
      "resources": {
         "receptors": [
         "SKA001",
         "SKA002",
         "SKA003",
         "SKA004"
         ]
      },
      "execution_block": {
         "eb_id": "eb-test-20220916-00000",
         "context": {},
         "max_length": 3600.0,
         "beams": [
         {
            "beam_id": "vis0",
            "function": "visibilities"
         }
         ],
         "scan_types": [
         {
            "scan_type_id": ".default",
            "beams": {
               "vis0": {
               "channels_id": "vis_channels",
               "polarisations_id": "all"
               }
            }
         },
         {
            "scan_type_id": "target:a",
            "derive_from": ".default",
            "beams": {
               "vis0": {
               "field_id": "field_a"
               }
            }
         },
         {
            "scan_type_id": "calibration:b",
            "derive_from": ".default",
            "beams": {
               "vis0": {
               "field_id": "field_b"
               }
            }
         }
         ],
         "channels": [
         {
            "channels_id": "vis_channels",
            "spectral_windows": [
               {
               "spectral_window_id": "fsp_1_channels",
               "count": 4,
               "start": 0,
               "stride": 2,
               "freq_min": 350000000.0,
               "freq_max": 368000000.0,
               "link_map": [
                  [
                     0,
                     0
                  ],
                  [
                     200,
                     1
                  ],
                  [
                     744,
                     2
                  ],
                  [
                     944,
                     3
                  ]
               ]
               }
            ]
         }
         ],
         "polarisations": [
         {
            "polarisations_id": "all",
            "corr_type": [
               "XX",
               "XY",
               "YX",
               "YY"
            ]
         }
         ],
         "fields": [
         {
            "field_id": "field_a",
            "phase_dir": {
               "ra": [
               123.0
               ],
               "dec": [
               -60.0
               ],
               "reference_time": "...",
               "reference_frame": "ICRF3"
            },
            "pointing_fqdn": "..."
         },
         {
            "field_id": "field_b",
            "phase_dir": {
               "ra": [
               123.0
               ],
               "dec": [
               -60.0
               ],
               "reference_time": "...",
               "reference_frame": "ICRF3"
            },
            "pointing_fqdn": "..."
         }
         ]
      },
      "processing_blocks": [
         {
         "pb_id": "pb-test-20220916-00000",
         "script": {
            "kind": "realtime",
            "name": "test-receive-addresses",
            "version": "0.5.0"
         },
         "sbi_ids": [
            "sbi-test-20220916-00000"
         ],
         "parameters": {}
         }
      ]
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
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-mvp01-20200325-00001",
    "subarray_id": 1, 
    "receptor_ids": ["0001", "0002"]
  }

Example JSON that requests all sub-array resources be released:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-mvp01-20200325-00001",
    "subarray_id": 1,
    "release_all": true
  }

Example JSON that requests all sub-array resources be released for LOW:

.. code-block:: JSON

  {
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    "subarray_id": 1,
    "release_all": true,
    "transaction_id": "txn-....-00001"
  }
