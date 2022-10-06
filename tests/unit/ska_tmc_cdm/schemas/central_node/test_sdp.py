import pytest
import json
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.utils import assert_json_is_equal
from ska_tmc_cdm.schemas.central_node.sdp import (

    ScanTypeSchema,
    SDPWorkflowSchema,
    PbDependencySchema,
    ChannelSchema,
    ProcessingBlockSchema,
    SDPConfigurationSchema,
    ExecutionBlockConfugurationSchema,
    BeamConfigurationSchema,
    ChannelConfigurationSchema,
    PolarisationConfigurationSchema,
    FieldConfigurationSchema,
    PhaseDirSchema,
    ResourceBlockConfigurationSchema
)
from .. import utils
VALID_SDP_JSON_PI16 = """{
    "interface": "1",
    "execution_block": {
      "eb_id": "eb-mvp01-20200325-00001",
      "max_length": 100.0,
      "context": {"temp": 1},
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
        "dependencies": {}
      },
      {
        "pb_id": "pb-mvp01-20200325-00002",
        "sbi_ids": [
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": {}
      },
      {
        "pb_id": "pb-mvp01-20200325-00003",
        "sbi_ids": [
          "sbi-mvp01-20200325-00001",
          "sbi-mvp01-20200325-00002"
        ],
        "script": {},
        "parameters": {},
        "dependencies": {}
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


def test_validate_serialization_and_deserialization_assign_resource_json_using_schema_class():
    """
    Verifies that the SDP schema marshal and Unmarshal works correctly
    """

    sdp_configuration_object = SDPConfigurationSchema().loads(VALID_SDP_JSON_PI16)

    deserialized = SDPConfigurationSchema().dump(sdp_configuration_object)

    assert_json_is_equal(SDPConfigurationSchema().dumps(sdp_configuration_object), VALID_SDP_JSON_PI16)

