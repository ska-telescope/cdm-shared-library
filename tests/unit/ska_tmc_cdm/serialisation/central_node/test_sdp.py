from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    ChannelConfiguration,
    EBScanTypeBeam,
    EBScanType,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    SDPConfiguration,
)
from pydantic import TypeAdapter
from ska_tmc_cdm import CODEC
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

VALID_BEAM_JSON_PI16 = """
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
      "max_length": 100.0,
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
            "max_length": 100.0,
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

VALID_SDP_ALL_PARAMETERS_JSON_PI16 = """{
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
      }],
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

VALID_SDP_MINIMAL_JSON_PI16 = """
{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
        "receptors": ["SKA001", "SKA036", "SKA063", "SKA100"]
    },
    "execution_block": {
        "eb_id": "eb-mvp01-20220929-00000",
        "max_length": 3600.0,
        "context": {},
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
            "spectral_windows": [{
                "spectral_window_id": "fsp_1_channels",
                "count": 14480, "start": 0, "stride": 1,
                "freq_min": 950000000.0, "freq_max": 1170000000.0,
                "link_map": [ [0, 0] ]
            }]
        }],
        "polarisations": [{
            "polarisations_id": "all",
            "corr_type": ["XX", "XY", "YY", "YX"]
        }],
        "fields": [{
            "field_id": "science-target",
            "phase_dir": {
                "ra": [-1], "dec": [-1],
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
                "ra": [-1], "dec": [-1],
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

VALID_BEAM_VIS0_JSON_PI16 = """{
                  "polarisations_id": "all",
                  "channels_id": "vis_channels"
               }"""

VALID_SDP_JSON_PI17 = """
{
    "interface": "https://schema.skao.int/ska-sdp-assignres/0.4",
    "resources": {
      "receptors": ["SKA001","SKA002","SKA003","SKA004"]
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
"""


def test_validate_serialization_and_deserialization_sdpconfiguration_all_parameters():
    """
    Verifies that the SDPConfiguration schema marshal and Unmarshal works correctly with all parameters
    """
    sdp_all_params_config = CODEC.loads(
        SDPConfiguration, VALID_SDP_ALL_PARAMETERS_JSON_PI16
    )
    serialized_sdp_all_params_config = CODEC.dumps(sdp_all_params_config)

    assert_json_is_equal(
        VALID_SDP_ALL_PARAMETERS_JSON_PI16,
        serialized_sdp_all_params_config,
    )


def test_validate_serialization_and_deserialization_sdpconfiguration_minimal_parameters():
    """
    Verifies that the SDPConfiguration schema marshal and Unmarshal works correctly with minimum parameters
    """
    sdp_all_params_config = CODEC.loads(SDPConfiguration, VALID_SDP_MINIMAL_JSON_PI16)
    serialized_sdp_all_params_config = CODEC.dumps(sdp_all_params_config)

    assert_json_is_equal(
        VALID_SDP_MINIMAL_JSON_PI16,
        serialized_sdp_all_params_config,
    )


def test_validate_serialization_and_deserialization_ebscantype():
    """
    Verifies that the EBScanType schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[EBScanType])
    scan_types_config = adapter.validate_json(VALID_SCAN_TYPES_JSON_PI16)
    serialized_scan_types_config = adapter.dump_json(
        scan_types_config, exclude_none=True, by_alias=True
    )

    assert_json_is_equal(VALID_SCAN_TYPES_JSON_PI16, serialized_scan_types_config)


def test_validate_serialization_and_deserialization_beam_vis0():
    """
    Verifies that the EBScanType Beam schema marshal and Unmarshal works correctly
    """
    scan_types_beam_config = CODEC.loads(EBScanTypeBeam, VALID_BEAM_VIS0_JSON_PI16)
    serialized_scan_types_beam_config = CODEC.dumps(scan_types_beam_config)

    assert_json_is_equal(VALID_BEAM_VIS0_JSON_PI16, serialized_scan_types_beam_config)


def test_validate_serialization_and_deserialization_executionblockconfiguration():
    """
    Verifies that the ExecutionBlockConfiguration schema marshal and Unmarshal works correctly
    """
    execution_block_config = CODEC.loads(
        ExecutionBlockConfiguration, VALID_EXECUTION_BLOCK_JSON_PI16
    )
    serialized_execution_block_config = CODEC.dumps(execution_block_config)

    assert_json_is_equal(
        VALID_EXECUTION_BLOCK_JSON_PI16, serialized_execution_block_config
    )


def test_validate_serialization_and_deserialization_beamconfiguration():
    """
    Verifies that the BeamConfiguration schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[BeamConfiguration])
    beam_config = adapter.validate_json(VALID_BEAM_JSON_PI16)
    serialized_beam_config = adapter.dump_json(
        beam_config,
        exclude_none=True,
        by_alias=True,
    )

    assert_json_is_equal(VALID_BEAM_JSON_PI16, serialized_beam_config)


def test_validate_serialization_and_deserialization_channelconfiguration():
    """
    Verifies that the ChannelConfiguration schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[ChannelConfiguration])
    channels_config = adapter.validate_json(VALID_CHANNELS_JSON_PI16)
    serialized_field_config = adapter.dump_json(
        channels_config, exclude_none=True, by_alias=True
    )

    assert_json_is_equal(VALID_CHANNELS_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_polarisationconfiguration():

    """
    Verifies that the PolarisationConfiguration schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[PolarisationConfiguration])
    polarisation_config = adapter.validate_json(VALID_POLARISATION_JSON_PI16)
    serialized_field_config = adapter.dump_json(
        polarisation_config,
        exclude_none=True,
        by_alias=True,
    )

    assert_json_is_equal(VALID_POLARISATION_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_fieldconfiguration():
    """
    Verifies that the FieldConfiguration schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[FieldConfiguration])
    fields_config = adapter.validate_json(VALID_FIELDS_JSON_PI16)
    serialized_field_config = adapter.dump_json(
        fields_config, exclude_none=True, by_alias=True
    )

    assert_json_is_equal(VALID_FIELDS_JSON_PI16, serialized_field_config)


def test_validate_serialization_and_deserialization_processingblock():
    """
    Verifies that the ProcessingBlock schema marshal and Unmarshal works correctly
    """
    adapter = TypeAdapter(list[ProcessingBlockConfiguration])
    processing_block_config = adapter.validate_json(VALID_PROCESSING_BLOCK_JSON_PI16)
    serialized_processing_block_config = adapter.dump_json(
        processing_block_config, exclude_none=True, by_alias=True
    )

    assert_json_is_equal(
        VALID_PROCESSING_BLOCK_JSON_PI16, serialized_processing_block_config
    )


def test_validate_serialization_and_deserialization_sdpconfiguration_json():
    """
    Verifies that the SDPConfiguration schema marshal and Unmarshal works correctly
    """

    sdp_configuration_object = CODEC.loads(SDPConfiguration, VALID_SDP_JSON_PI17)
    serialized_sdp_config = CODEC.dumps(sdp_configuration_object)

    assert_json_is_equal(VALID_SDP_JSON_PI17, serialized_sdp_config)
