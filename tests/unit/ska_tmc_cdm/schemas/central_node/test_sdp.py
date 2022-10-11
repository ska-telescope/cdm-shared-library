from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import (
    BeamConfigurationSchema,
    ChannelConfigurationSchema,
    ExecutionConfigurationSchema,
    FieldConfigurationSchema,
    PolarisationConfigurationSchema,
    ProcessingBlockSchema,
    ResourceConfigurationSchema,
    SDPConfigurationSchema,
    ScanTypesBeamsSchema,
    ScanTypesSchema
)
from ska_tmc_cdm.utils import assert_json_is_equal

VALID_SCAN_TYPES_JSON_PI16 = """[
         {
            "scan_type_id": ".default",
            "beams": {
               "vis0": {
                  "polarisations_id": "all",
                  "channels_id": "vis_channels"
               }
            }
         },
         {
            "scan_type_id": "science",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_a" }
            }
         },
         {
            "scan_type_id": "calibration",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_b" }
            }
         }
      ]
"""

VALID_SCAN_TYPES_JSON_PI16_test = """
[
         {
            "scan_type_id": ".default"
            
         },
         {
            "scan_type_id": "science",
            "derive_from": ".default"
            
         },
         {
            "scan_type_id": "calibration",
            "derive_from": ".default"
            
         }
      ]"""

VALID_RESOURCES_JSON_PI16 = """{ 
      "csp_links": [
        1,
        2,
        3,
        4
      ],
      "receptors": [
        "FS4",
        "FS8"
      ],
      "receive_nodes": 10 
    }"""

VALID_PROCESSING_BLOCK_JSON_PI16 = """[
    {
        "pb_id": "pb-mvp01-20200325-00001",
        "sbi_ids": [
            "sbi-mvp01-20200325-00001"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
    },
    {
        "pb_id": "pb-mvp01-20200325-00002",
        "sbi_ids": [
            "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
    },
    {
        "pb_id": "pb-mvp01-20200325-00003",
        "sbi_ids": [
            "sbi-mvp01-20200325-00001",
            "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
    }
]"""

VALID_FIELDS_JSON_PI16 = """[
    {
        "field_id": "field_a",
        "phase_dir": {
            "ra": [
                123,
                0.1
            ],
            "dec": [
                123,
                0.1
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
        },
        "pointing_fqdn": "low-tmc/telstate/0/pointing"
    }
]"""


VALID_POLARISATION_JSON_PI16 = """
    [
        {
          "polarisations_id": "all",
          "corr_type": [
            "XX",
            "XY",
            "YY",
            "YX"
          ]
        }
    ]"""

VALID_CHANNELS_JSON_PI16 = """
    [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "count": 744,
              "start": 0,
              "stride": 2,
              "freq_min": 0.35e9,
              "freq_max": 0.368e9,
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
            },
            {
              "spectral_window_id": "fsp_2_channels",
              "count": 744,
              "start": 2000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 368000000,
              "link_map": [
                [
                  2000,
                  4
                ],
                [
                  2200,
                  5
                ]
              ]
            },
            {
              "spectral_window_id": "zoom_window_1",
              "count": 744,
              "start": 4000,
              "stride": 1,
              "freq_min": 0.35e9,
                "freq_max": 0.368e9,
              "link_map": [
                [
                  4000,
                  6
                ],
                [
                  4200,
                  7
                ]
              ]
            }
          ]
        },
        {
          "channels_id": "pulsar_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "pulsar_fsp_channels",
              "count": 744,
              "start": 0,
              "freq_min": 0.35e9,
            "freq_max": 0.368e9
            }
          ]
        }
    ]"""

VALID_BEAMS_JSON_PI16 = """
    [ 
        {
          "beam_id": "vis0",
          "function": "visibilities"
        },
        {
          "beam_id": "pss1",
          "search_beam_id": 1,
          "function": "pulsar search"
        },
        {
          "beam_id": "pss2",
          "search_beam_id": 2,
          "function": "pulsar search"
        },
        {
          "beam_id": "pst1",
          "timing_beam_id": 1,
          "function": "pulsar timing"
        },
        {
          "beam_id": "pst2",
          "timing_beam_id": 2,
          "function": "pulsar timing"
        },
        {
          "beam_id": "vlbi1",
          "vlbi_beam_id": 1,
          "function": "vlbi"
        }
    ]"""

VALID_EXECUTION_BLOCK_JSON_PI16 = """
    {
      "eb_id": "eb-mvp01-20200325-00001",
      "max_length": 100,
      "context": {},
      "beams": [ 
        {
          "beam_id": "vis0",
          "function": "visibilities"
        },
        {
          "beam_id": "pss1",
          "search_beam_id": 1,
          "function": "pulsar search"
        },
        {
          "beam_id": "pss2",
          "search_beam_id": 2,
          "function": "pulsar search"
        },
        {
          "beam_id": "pst1",
          "timing_beam_id": 1,
          "function": "pulsar timing"
        },
        {
          "beam_id": "pst2",
          "timing_beam_id": 2,
          "function": "pulsar timing"
        },
        {
          "beam_id": "vlbi1",
          "vlbi_beam_id": 1,
          "function": "vlbi"
        }
      ],
      "channels": [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "count": 744,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000,
              "freq_max": 368000000,
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
            },
            {
              "spectral_window_id": "fsp_2_channels",
              "count": 744,
              "start": 2000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 368000000,
              "link_map": [
                [
                  2000,
                  4
                ],
                [
                  2200,
                  5
                ]
              ]
            },
            {
              "spectral_window_id": "zoom_window_1",
              "count": 744,
              "start": 4000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 361000000,
              "link_map": [
                [
                  4000,
                  6
                ],
                [
                  4200,
                  7
                ]
              ]
            }
          ]
        },
        {
          "channels_id": "pulsar_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "pulsar_fsp_channels",
              "count": 744,
              "start": 0,
              "freq_min": 350000000,
              "freq_max": 368000000
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
            "YY",
            "YX"
          ]
        }
      ],
      "fields": [
        {
          "field_id": "field_a",
          "phase_dir": {
            "ra": [
              123,
              0.1
            ],
            "dec": [
              123,
              0.1
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "low-tmc/telstate/0/pointing"
        }
      ]
    }"""


VALID_SDP_JSON_PI16 = """{
        "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
        "execution_block": {
            "eb_id": "eb-mvp01-20200325-00001",
            "max_length": 100,
            "context": {},
            "beams": [
                {
                    "beam_id": "vis0",
                    "function": "visibilities"
                },
                {
                    "beam_id": "pss1",
                    "search_beam_id": 1,
                    "function": "pulsar search"
                },
                {
                    "beam_id": "pss2",
                    "search_beam_id": 2,
                    "function": "pulsar search"
                },
                {
                    "beam_id": "pst1",
                    "timing_beam_id": 1,
                    "function": "pulsar timing"
                },
                {
                    "beam_id": "pst2",
                    "timing_beam_id": 2,
                    "function": "pulsar timing"
                },
                {
                    "beam_id": "vlbi1",
                    "vlbi_beam_id": 1,
                    "function": "vlbi"
                }
            ],
            "channels": [
                {
                    "channels_id": "vis_channels",
                    "spectral_windows": [
                        {
                            "count": 744,
                            "start": 0,
                            "stride": 2,
                            "freq_min": 350000000,
                            "freq_max": 368000000,
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
                        },
                        {
                            "spectral_window_id": "fsp_2_channels",
                            "count": 744,
                            "start": 2000,
                            "stride": 1,
                            "freq_min": 360000000,
                            "freq_max": 368000000,
                            "link_map": [
                                [
                                    2000,
                                    4
                                ],
                                [
                                    2200,
                                    5
                                ]
                            ]
                        },
                        {
                            "spectral_window_id": "zoom_window_1",
                            "count": 744,
                            "start": 4000,
                            "stride": 1,
                            "freq_min": 360000000,
                            "freq_max": 361000000,
                            "link_map": [
                                [
                                    4000,
                                    6
                                ],
                                [
                                    4200,
                                    7
                                ]
                            ]
                        }
                    ]
                },
                {
                    "channels_id": "pulsar_channels",
                    "spectral_windows": [
                        {
                            "spectral_window_id": "pulsar_fsp_channels",
                            "count": 744,
                            "start": 0,
                            "freq_min": 350000000,
                            "freq_max": 368000000
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
                        "YY",
                        "YX"
                    ]
                }
            ],
            "fields": [
                {
                    "field_id": "field_a",
                    "phase_dir": {
                        "ra": [
                            123,
                            0.1
                        ],
                        "dec": [
                            123,
                            0.1
                        ],
                        "reference_time": "...",
                        "reference_frame": "ICRF3"
                    },
                    "pointing_fqdn": "low-tmc/telstate/0/pointing"
                }
            ]
        },
        "processing_blocks": [
            {
                "pb_id": "pb-mvp01-20200325-00001",
                "sbi_ids": [
                    "sbi-mvp01-20200325-00001"
                ],
                "script": {},
                "parameters": {},
                "dependencies": []
            },
            {
                "pb_id": "pb-mvp01-20200325-00002",
                "sbi_ids": [
                    "sbi-mvp01-20200325-00002"
                ],
                "script": {},
                "parameters": {},
                "dependencies": []
            },
            {
                "pb_id": "pb-mvp01-20200325-00003",
                "sbi_ids": [
                    "sbi-mvp01-20200325-00001",
                    "sbi-mvp01-20200325-00002"
                ],
                "script": {},
                "parameters": {},
                "dependencies": []
            }
        ],
        "resources": {
            "csp_links": [
                1,
                2,
                3,
                4
            ],
            "receptors": [
                "FS4",
                "FS8"
            ],
            "receive_nodes": 10
        }
    }"""

VALID_ASSIGN_RESOURCE_JSON_PI16 = """
{
  "interface": "https://schema.skao.int/ska-tmc-assignresources/2.1",
  "transaction_id": "txn-....-00001",
  "subarray_id": 1,
  "dish": {
    "receptor_ids": [
      "0001"
    ]
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "execution_block": {
      "eb_id": "eb-mvp01-20200325-00001",
      "max_length": 100,
      "context": {},
      "beams": [
        {
          "beam_id": "vis0",
          "function": "visibilities"
        },
        {
          "beam_id": "pss1",
          "search_beam_id": 1,
          "function": "pulsar search"
        },
        {
          "beam_id": "pss2",
          "search_beam_id": 2,
          "function": "pulsar search"
        },
        {
          "beam_id": "pst1",
          "timing_beam_id": 1,
          "function": "pulsar timing"
        },
        {
          "beam_id": "pst2",
          "timing_beam_id": 2,
          "function": "pulsar timing"
        },
        {
          "beam_id": "vlbi1",
          "vlbi_beam_id": 1,
          "function": "vlbi"
        }
      ],
      "channels": [
        {
          "channels_id": "vis_channels",
          "spectral_windows": [
            {
              "count": 744,
              "start": 0,
              "stride": 2,
              "freq_min": 350000000,
              "freq_max": 368000000,
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
            },
            {
              "spectral_window_id": "fsp_2_channels",
              "count": 744,
              "start": 2000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 368000000,
              "link_map": [
                [
                  2000,
                  4
                ],
                [
                  2200,
                  5
                ]
              ]
            },
            {
              "spectral_window_id": "zoom_window_1",
              "count": 744,
              "start": 4000,
              "stride": 1,
              "freq_min": 360000000,
              "freq_max": 361000000,
              "link_map": [
                [
                  4000,
                  6
                ],
                [
                  4200,
                  7
                ]
              ]
            }
          ]
        },
        {
          "channels_id": "pulsar_channels",
          "spectral_windows": [
            {
              "spectral_window_id": "pulsar_fsp_channels",
              "count": 744,
              "start": 0,
              "freq_min": 350000000,
              "freq_max": 368000000
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
            "YY",
            "YX"
          ]
        }
      ],
      "fields": [
        {
          "field_id": "field_a",
          "phase_dir": {
            "ra": [
              123,
              0.1
            ],
            "dec": [
              123,
              0.1
            ],
            "reference_time": "...",
            "reference_frame": "ICRF3"
          },
          "pointing_fqdn": "low-tmc/telstate/0/pointing"
        }
      ]
    },
    "processing_blocks": [
      {
        "pb_id": "pb-mvp01-20200325-00001",
        "sbi_ids": [
          "sbi-mvp01-20200325-00001"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      },
      {
        "pb_id": "pb-mvp01-20200325-00002",
        "sbi_ids": [
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      },
      {
        "pb_id": "pb-mvp01-20200325-00003",
        "sbi_ids": [
          "sbi-mvp01-20200325-00001",
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": []
      }
    ],
    "resources": {
      "csp_links": [
        1,
        2,
        3,
        4
      ],
      "receptors": [
        "FS4",
        "FS8"
      ],
      "receive_nodes": 10
    }
  }
}"""

VALID_MINIMAL_ASSIGN_RESOURCES_JSON_PI16 = """
{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
        // SKA-TEL-AIV-2410001 Table 18 batch 1
        "receptors": ["SKA001", "SKA036", "SKA063", "SKA100"]
    },
    "execution_block": {
        "eb_id": "eb-mvp01-20220929-00000",
        // Length? Sum of scan lengths seems to add up to roughly an hour?
        "max_length": 3600.0,
        "context": {},
        // Single visibility beam
        "beams": [{ "beam_id": "vis0", "function": "visibilities" }],
        "scan_types": [{
            "scan_type_id": ".default",
            "beams": { "vis0": { "channels_id": "vis_channels", "polarisations_id": "all" } }
        }, {
            "scan_type_id": "science:target",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "science-target" } }
        }, {
            "scan_type_id": "flux:pks1934-638",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1934-638" } }
        }, {
            "scan_type_id": "delay:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "delay-field-TBD" } }
        }, {
            "scan_type_id": "bandpass:pks1921-203",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1921-203" } }
        }, {
            "scan_type_id": "gains:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "gains-field-TBD" } }
        }, {
            "scan_type_id": "polarisation:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "polarisation-field-TBD" } }
        }],
        "channels": [{
            "channels_id": "vis_channels",
            // Assuming a single FSP, covering 220 MHz from 0.95 GHz
            "spectral_windows": [{
                "spectral_window_id": "fsp_1_channels",
                "count": 14480, "start": 0, "stride": 1,
                "freq_min": 950000000.0, "freq_max": 1170000000.0,
                "link_map": [ [0, 0] ]
            }]
        }],
        // Assuming full linear polarisation
        "polarisations": [{
            "polarisations_id": "all",
            "corr_type": ["XX", "XY", "YY", "YX"]
        }],
        "fields": [{
            "field_id": "science-target",
            "phase_dir": {
                "ra": [/* TBD */], "dec": [/* TBD */],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1934-638",
            "phase_dir": {
                "ra": [294.85426888], "dec": [-63.71267788],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "delay-field-TBD",
            "phase_dir": {
                "ra": [/* TBD */], "dec": [/* TBD */],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1921-203",
            "phase_dir": {
                "ra": [291.21273125], "dec": [-29.23892167],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        }]
    },
  // Only stand-in processing block without receive for the moment
  "processing_blocks": [
    {
      "pb_id": "pb-test-20220916-00000",
      "script": {"kind": "realtime", "name": "test-receive-addresses", "version": "0.5.0"},
      "sbi_ids": ["sbi-test-20220916-00000"],
      "parameters": {}
    }
  ]
}
"""

VALID_ASSIGN_RESOURCES_ALL_PARAMETERS_JSON_PI16 = """{
   "interface":"https://schema.skao.int/ska-sdp-assignres/0.4",

   "resources": {
      "csp_links": [ 1, 2, 3, 4 ],
      "receptors": ["C10", "C136", "C1", "C217", "C13", "C42"],
      "receive_nodes": 1
   },

   "execution_block": {
      "eb_id":"eb-test-20210630-00000",
      "context": {},
      "max_length":21600.0,

      "channels": [ {
         "channels_id": "vis_channels",
         "spectral_windows": [ {
             "spectral_window_id": "fsp_1_channels",
             "count": 13824,
             "start": 0,
             "stride": 2,
             "freq_min": 0.35e9,
             "freq_max": 0.368e9,
             "link_map": [ [0, 0], [200, 1], [744, 2], [944, 3] ]
         } ]
      } ],

      "polarisations": [ {
         "polarisations_id": "all",
         "corr_type": [ "XX", "XY", "YY", "YX" ]
      } ],

      "fields": [ {
         "field_id": "field_a",
         "phase_dir" : {
           "ra": [ 2.711325 ],
           "dec": [ -0.01328889 ],
           "reference_time": "...",
           "reference_frame": "ICRF3"
         },
         "pointing_fqdn": "low-tmc/telstate/0/pointing"
      }, {
         "field_id": "field_b",
         "phase_dir" : {
           "ra": [ 12.48519 ],
           "dec": [ 2.052388 ],
           "reference_time": "...",
           "reference_frame": "ICRF3"
         },
         "pointing_fqdn": "low-tmc/telstate/0/pointing"
      } ],

      "beams": [ {
         "beam_id": "vis0",
         "function": "visibilities"
      } ],

      "scan_types":[
         {
            "scan_type_id": ".default",
            "beams": {
               "vis0": {
                  "polarisations_id": "all",
                  "channels_id": "vis_channels"
               }
            }
         },
         {
            "scan_type_id": "science",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_a" }
            }
         },
         {
            "scan_type_id": "calibration",
            "derive_from": ".default",
            "beams": {
              "vis0": { "field_id": "field_b" }
            }
         }
      ]
   },
   "processing_blocks":[
      {
         "pb_id":"pb-test-20211111-00000",
         "script":{
            "kind":"realtime",
            "name":"vis-receive",
            "version":"0.6.0"
         },
         "parameters": {
            "plasmaEnabled": true,
            "reception": {
               "layout": "http://127.0.0.1:80/model/default/ska1_low/layout",
               "num_channels": 13824,
               "channels_per_stream": 6912,
               "continuous_mode": true,
               "transport_protocol": "tcp"
            },
            "pvc": {
               "name": "receive-data"
            },
            "plasma_parameters": {
               "initContainers":[
                  {
                     "name":"existing-output-remover",
                     "image":"artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                     "command":["rm", "-rf", "/mnt/data/output*.ms"],
                     "volumeMounts":[
                        {
                           "mountPath":"/mnt/data",
                           "name":"receive-data"
                        }
                     ]
                  }
               ],
               "extraContainers":[
                  {
                     "name":"plasma-processor",
                     "image":"artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                     "command":[
                        "plasma-mswriter",
                        "-s",
                        "/plasma/socket",
                        "--max_payloads",
                        "12",
                        "--use_plasmastman",
                        "False",
                        "/mnt/data/output.ms"
                     ],
                     "volumeMounts":[
                        {
                           "name":"plasma-storage-volume",
                           "mountPath":"/plasma"
                        },
                        {
                           "mountPath":"/mnt/data",
                           "name":"receive-data"
                        }
                     ]
                  },
                  {
                     "name": "tmlite-server",
                     "image": "artefact.skao.int/ska-sdp-tmlite-server:0.3.0"
                  }
               ]
            }
         }
      }
   ]
}
"""

VALID_ASSIGN_RESOURCE_MINIMAL_JSON_PI16 = """{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
        // SKA-TEL-AIV-2410001 Table 18 batch 1
        "receptors": ["SKA001", "SKA036", "SKA063", "SKA100"]
    },
    "execution_block": {
        "eb_id": "eb-mvp01-20220929-00000",
        // Length? Sum of scan lengths seems to add up to roughly an hour?
        "max_length": 3600.0,
        "context": {},
        // Single visibility beam
        "beams": [{ "beam_id": "vis0", "function": "visibilities" }],
        "scan_types": [{
            "scan_type_id": ".default",
            "beams": { "vis0": { "channels_id": "vis_channels", "polarisations_id": "all" } }
        }, {
            "scan_type_id": "science:target",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "science-target" } }
        }, {
            "scan_type_id": "flux:pks1934-638",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1934-638" } }
        }, {
            "scan_type_id": "delay:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "delay-field-TBD" } }
        }, {
            "scan_type_id": "bandpass:pks1921-203",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "pks1921-203" } }
        }, {
            "scan_type_id": "gains:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "gains-field-TBD" } }
        }, {
            "scan_type_id": "polarisation:TBD",
            "derive_from": ".default", "beams": { "vis0": { "field_id": "polarisation-field-TBD" } }
        }],
        "channels": [{
            "channels_id": "vis_channels",
            // Assuming a single FSP, covering 220 MHz from 0.95 GHz
            "spectral_windows": [{
                "spectral_window_id": "fsp_1_channels",
                "count": 14480, "start": 0, "stride": 1,
                "freq_min": 950000000.0, "freq_max": 1170000000.0,
                "link_map": [ [0, 0] ]
            }]
        }],
        // Assuming full linear polarisation
        "polarisations": [{
            "polarisations_id": "all",
            "corr_type": ["XX", "XY", "YY", "YX"]
        }],
        "fields": [{
            "field_id": "science-target",
            "phase_dir": {
                "ra": [/* TBD */], "dec": [/* TBD */],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1934-638",
            "phase_dir": {
                "ra": [294.85426888], "dec": [-63.71267788],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "delay-field-TBD",
            "phase_dir": {
                "ra": [/* TBD */], "dec": [/* TBD */],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        },{
            "field_id": "pks1921-203",
            "phase_dir": {
                "ra": [291.21273125], "dec": [-29.23892167],
                "reference_time": "TBD", "reference_frame": "ICRF3"
            }
        }]
    },
  // Only stand-in processing block without receive for the moment
  "processing_blocks": [
    {
      "pb_id": "pb-test-20220916-00000",
      "script": {"kind": "realtime", "name": "test-receive-addresses", "version": "0.5.0"},
      "sbi_ids": ["sbi-test-20220916-00000"],
      "parameters": {}
    }
  ]
}

"""

VALID_BEAMS_VIS0_JSON_PI16 = """{
                  "polarisations_id": "all",
                  "channels_id": "vis_channels"
               }"""
def test_validate_serialization_and_deserialization_assign_resource_all_parameters_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    assign_resource_all_params_config = AssignResourcesRequestSchema().loads(
        VALID_ASSIGN_RESOURCES_ALL_PARAMETERS_JSON_PI16
    )
    serialized_assign_resource_all_params_config = AssignResourcesRequestSchema().dumps(
        assign_resource_all_params_config
    )

    assert_json_is_equal(
        VALID_ASSIGN_RESOURCES_ALL_PARAMETERS_JSON_PI16, serialized_assign_resource_all_params_config
    )


def test_validate_serialization_and_deserialization_scan_types_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    scan_types_config = ScanTypesSchema(many=True).loads(
        VALID_SCAN_TYPES_JSON_PI16
    )
    serialized_scan_types_config = ScanTypesSchema(many=True).dumps(
        scan_types_config
    )

    assert_json_is_equal(
        VALID_SCAN_TYPES_JSON_PI16, serialized_scan_types_config
    )


def test_validate_serialization_and_deserialization_beams_vis0_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    scan_types_beams_config = ScanTypesBeamsSchema().loads(
        VALID_BEAMS_VIS0_JSON_PI16
    )
    serialized_scan_types_beams_config= ScanTypesBeamsSchema().dumps(
        scan_types_beams_config
    )

    assert_json_is_equal(
        VALID_BEAMS_VIS0_JSON_PI16, serialized_scan_types_beams_config
    )

def test_validate_serialization_and_deserialization_assign_resource_using_schema_class():
    """
    Verifies that the Assign Resource schema marshal and Unmarshal works correctly
    """
    assign_resource_config = AssignResourcesRequestSchema().loads(
        VALID_ASSIGN_RESOURCE_JSON_PI16
    )
    serialized_assign_resource_config = AssignResourcesRequestSchema().dumps(
        assign_resource_config
    )

    assert_json_is_equal(
        VALID_ASSIGN_RESOURCE_JSON_PI16, serialized_assign_resource_config
    )


def test_validate_serialization_and_deserialization_execution_block_using_schema_class():
    """
    Verifies that the Execution Block schema marshal and Unmarshal works correctly
    """
    execution_block_config = ExecutionConfigurationSchema().loads(
        VALID_EXECUTION_BLOCK_JSON_PI16
    )
    serialized_execution_block_config = ExecutionConfigurationSchema().dumps(
        execution_block_config
    )

    assert_json_is_equal(
        VALID_EXECUTION_BLOCK_JSON_PI16, serialized_execution_block_config
    )


def test_validate_serialization_and_deserialization_beams_using_schema_class():
    """
    Verifies that the Beams schema marshal and Unmarshal works correctly
    """
    beams_config = BeamConfigurationSchema(many=True).loads(VALID_BEAMS_JSON_PI16)
    serialized_beams_config = BeamConfigurationSchema(many=True).dumps(beams_config)

    assert_json_is_equal(VALID_BEAMS_JSON_PI16, serialized_beams_config)


def test_validate_serialization_and_deserialization_channels_using_schema_class():
    """
    Verifies that the Channels schema marshal and Unmarshal works correctly
    """
    channels_config = ChannelConfigurationSchema(many=True).loads(
        VALID_CHANNELS_JSON_PI16
    )
    serialized_field_config = ChannelConfigurationSchema(many=True).dumps(
        channels_config
    )

    assert_json_is_equal(VALID_CHANNELS_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_polarisation_using_schema_class():

    """
    Verifies that the Polarisation schema marshal and Unmarshal works correctly
    """
    polarisation_config = PolarisationConfigurationSchema(many=True).loads(
        VALID_POLARISATION_JSON_PI16
    )
    serialized_field_config = PolarisationConfigurationSchema(many=True).dumps(
        polarisation_config
    )

    assert_json_is_equal(VALID_POLARISATION_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_fields_using_schema_class():
    """
    Verifies that the Fields schema marshal and Unmarshal works correctly
    """
    fields_config = FieldConfigurationSchema(many=True).loads(VALID_FIELDS_JSON_PI16)
    serialized_field_config = FieldConfigurationSchema(many=True).dumps(fields_config)

    assert_json_is_equal(VALID_FIELDS_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_resources_block_using_schema_class():
    """
    Verifies that the  Resource Block schema marshal and Unmarshal works correctly
    """
    resources_config = ResourceConfigurationSchema().loads(VALID_RESOURCES_JSON_PI16)
    serialized_resource_config = ResourceConfigurationSchema().dumps(resources_config)

    assert_json_is_equal(VALID_RESOURCES_JSON_PI16, serialized_resource_config)


def test_validate_serialization_and_deserialization_processing_block_using_schema_class():
    """
    Verifies that the Processing Block schema marshal and Unmarshal works correctly
    """
    processing_block_config = ProcessingBlockSchema(many=True).loads(
        VALID_PROCESSING_BLOCK_JSON_PI16
    )
    serialized_processing_block_config = ProcessingBlockSchema(many=True).dumps(
        processing_block_config
    )

    assert_json_is_equal(
        VALID_PROCESSING_BLOCK_JSON_PI16, serialized_processing_block_config
    )


def test_validate_serialization_and_deserialization_sdp_json_using_schema_class():
    """
    Verifies that the SDP schema marshal and Unmarshal works correctly
    """

    sdp_configuration_object = SDPConfigurationSchema().loads(VALID_SDP_JSON_PI16)
    serialized_sdp_config = SDPConfigurationSchema().dumps(sdp_configuration_object)

    assert_json_is_equal(VALID_SDP_JSON_PI16, serialized_sdp_config)
