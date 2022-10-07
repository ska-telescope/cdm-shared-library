from ska_tmc_cdm.schemas.central_node.assign_resources import (
    AssignResourcesRequestSchema,
)
from ska_tmc_cdm.schemas.central_node.sdp import (
    BeamConfigurationSchema,
    ChannelConfigurationSchema,
    ExecutionBlockConfugurationSchema,
    FieldConfigurationSchema,
    PolarisationConfigurationSchema,
    ProcessingBlockSchema,
    ResourceBlockConfigurationSchema,
    SDPConfigurationSchema,
)
from ska_tmc_cdm.utils import assert_json_is_equal

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
    execution_block_config = ExecutionBlockConfugurationSchema().loads(
        VALID_EXECUTION_BLOCK_JSON_PI16
    )
    serialized_execution_block_config = ExecutionBlockConfugurationSchema().dumps(
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
    resources_config = ResourceBlockConfigurationSchema().loads(
        VALID_RESOURCES_JSON_PI16
    )
    serialized_resource_config = ResourceBlockConfigurationSchema().dumps(
        resources_config
    )

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
