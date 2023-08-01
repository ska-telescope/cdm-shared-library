"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure module.
"""

from datetime import timedelta

import pytest
from ska_telmodel.telvalidation.semantic_validator import SchematicValidationError

from ska_tmc_cdm.messages.subarray_node.configure import SCHEMA, ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    Target,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    BeamConfiguration,
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget,
)
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska_tmc_cdm.schemas.subarray_node.configure import ConfigureRequestSchema

from .. import utils

NON_COMPLIANCE_MID_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.1",
    transaction_id="txn-....-00001",
    pointing=PointingConfiguration(
        Target(
            ra="21:08:47.92",
            dec="-88:57:22.9",
            target_name="Polaris Australis",
            reference_frame="icrs",
        )
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_5A),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration("science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_5B,
            subarray_id=1,
        ),
        pss_config={},
        pst_config={},
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=5,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=744,
                    output_link_map=[(0, 4), (200, 5)],
                    zoom_window_tuning=650000,
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
            ],
            vlbi_config={},
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

NON_COMPLIANCE_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.1",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    }
  },
  "dish": {
    "receiver_band": "5a"
  },
  "csp": {
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "5b",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        },
        {
          "fsp_id": 5,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 744,
          "output_link_map": [
            [
              0,
              4
            ],
            [
              200,
              5
            ]
          ],
          "zoom_window_tuning": 650000
        },
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        },
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        },
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        }, 
      ],
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-configure/2.0",
  "mccs": {
    "stations":[
      {
        "station_id": 1
      },
      {
        "station_id": 2
      }
    ],
    "subarray_beams": [
      {
        "subarray_beam_id":1,
        "station_ids": [1,2],
        "channels": [
          [0, 8, 1, 1],
          [8, 8, 2, 1],
          [24, 16, 2, 1]
        ],
        "update_rate": 0.0,
        "target": {
          "reference_frame": "horizon",
          "target_name": "DriftScan",
          "az": 180.0,
          "el": 45.0
        },
        "antenna_weights": [1.0, 1.0, 1.0],
        "phase_centre": [0.0, 0.0]
      }
    ]
  },
  "tmc": {
    "scan_duration": 10.0 
  }
}
"""

VALID_LOW_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-low-tmc-configure/2.0",
    mccs=MCCSConfiguration(
        station_configs=[StnConfiguration(1), StnConfiguration(2)],
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                station_ids=[1, 2],
                channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
                update_rate=0.0,
                target=SubarrayBeamTarget(180.0, 45.0, "DriftScan", "horizon"),
                antenna_weights=[1.0, 1.0, 1.0],
                phase_centre=[0.0, 0.0],
            )
        ],
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

VALID_LOW_CONFIGURE_JSON_PI17 = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-configure/3.0",
  "mccs": {
    "stations":[
      {
        "station_id": 1
      },
      {
        "station_id": 2
      }
    ],
    "subarray_beams": [
      {
        "subarray_beam_id":1,
        "station_ids": [1,2],
        "channels": [
          [0, 8, 1, 1],
          [8, 8, 2, 1],
          [24, 16, 2, 1]
        ],
        "update_rate": 0.0,
        "target": {
          "reference_frame": "horizon",
          "target_name": "DriftScan",
          "az": 180.0,
          "el": 45.0
        },
        "antenna_weights": [1.0, 1.0, 1.0],
        "phase_centre": [0.0, 0.0]
      }
    ]
  },
  "tmc": {
    "scan_duration": 10.0 
  },
  "sdp": {
     "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
     "scan_type": "science_A"
 },
   "csp": {
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A"
    },
     "lowcbf": {
      "stations": {
        "stns": [
          [
            1,
            0
          ],
          [
            2,
            0
          ],
          [
            3,
            0
          ],
          [
            4,
            0
          ]
        ],
           "stn_beams": [
          {
            "beam_id": 1,
            "freq_ids": [
              64,
              65,
              66,
              67,
              68,
              68,
              70,
              71
            ],
            "boresight_dly_poly": "url"
          }
        ]
      },
      "timing_beams": {
        "beams": [
          {
            "pst_beam_id": 13,
            "stn_beam_id": 1,
            "offset_dly_poly": "url",
            "stn_weights": [
              0.9,
              1.0,
              1.0,
              0.9
            ],
            "jones": "url",
            "dest_chans": [
              128,
              256
            ],
            "rfi_enable": [
              true,
              true,
              true
            ],
            "rfi_static_chans": [
              1,
              206,
              997
            ],
            "rfi_dynamic_chans": [
              242,
              1342
            ],
            "rfi_weighted": 0.87
          }
        ]
      }
      }
    }
}
"""

VALID_LOW_CONFIGURE_OBJECT_PI17 = ConfigureRequest(
    interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
    mccs=MCCSConfiguration(
        station_configs=[StnConfiguration(1), StnConfiguration(2)],
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                station_ids=[1, 2],
                channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
                update_rate=0.0,
                target=SubarrayBeamTarget(180.0, 45.0, "DriftScan", "horizon"),
                antenna_weights=[1.0, 1.0, 1.0],
                phase_centre=[0.0, 0.0],
            )
        ],
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration(subarray_name="science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
        ),
        lowcbf=LowCBFConfiguration(
            stations=StationConfiguration(
                stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
                stn_beams=[
                    StnBeamConfiguration(
                        beam_id=1,
                        freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                        boresight_dly_poly="url",
                    )
                ],
            ),
            timing_beams=TimingBeamConfiguration(
                beams=[
                    BeamConfiguration(
                        pst_beam_id=13,
                        stn_beam_id=1,
                        offset_dly_poly="url",
                        stn_weights=[0.9, 1.0, 1.0, 0.9],
                        jones="url",
                        dest_chans=[128, 256],
                        rfi_enable=[True, True, True],
                        rfi_static_chans=[1, 206, 997],
                        rfi_dynamic_chans=[242, 1342],
                        rfi_weighted=0.87,
                    )
                ]
            ),
        ),
    ),
)

INVALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-configure/2.0",
  "mccs": {
    "stations":[
      {
        "station_id": 1
      }
    ],
    "subarray_beams": [
      {
        "subarray_beam_id":-1,
        "station_ids": [1,2],
        "channels": [[1,2]],
        "update_rate": 1.0,
        "target": {
              "reference_frame": "horizon",
              "target_name": "DriftScan",
              "az": 180.0,
              "el": 45.0
        },
        "antenna_weights": [1.0, 1.0, 1.0],
        "phase_centre": [0.0, 0.0]
      }
    ]
  }
}
"""

VALID_MID_DISH_ONLY_JSON = (
    """
{
    "interface": """
    + f'"{SCHEMA}"'
    + """,
    "dish": {
        "receiver_band": "1"
    }
}
"""
)

VALID_MID_DISH_ONLY_OBJECT = ConfigureRequest(
    dish=DishConfiguration(ReceiverBand.BAND_1)
)

VALID_NULL_JSON = (
    """
{
    "interface": """
    + f'"{SCHEMA}"'
    + """
}
"""
)

VALID_NULL_OBJECT = ConfigureRequest()

VALID_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.1",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    }
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "1",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 1,
          "function_mode": "CORR",
          "frequency_slice_id": 1,
          "integration_factor": 1,
          "zoom_factor": 0,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 744,
          "output_link_map": [
            [
              0,
              4
            ],
            [
              200,
              5
            ]
          ],
          "zoom_window_tuning": 650000
        }
      ],
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}"""

INVALID_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.1",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    }
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "1",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 1,
          "function_mode": "CORR",
          "frequency_slice_id": 1,
          "integration_factor": 1,
          "zoom_factor": 0,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 0,
          "output_link_map": [
            [
              0,
              0
            ],
            [
              200,
              1
            ]
          ]
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
          "channel_averaging_map": [
            [
              0,
              2
            ],
            [
              744,
              0
            ]
          ],
          "channel_offset": 744,
          "output_link_map": [
            [
              0,
              4
            ],
            [
              200,
              5
            ]
          ],
          "zoom_window_tuning": 650000
        }
      ],
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": -10
  }
}"""

VALID_MID_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.1",
    transaction_id="txn-....-00001",
    pointing=PointingConfiguration(
        Target(
            ra="21:08:47.92",
            dec="-88:57:22.9",
            target_name="Polaris Australis",
            reference_frame="icrs",
        )
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration("science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
        ),
        pss_config={},
        pst_config={},
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(
                    fsp_id=1,
                    function_mode=FSPFunctionMode.CORR,
                    frequency_slice_id=1,
                    integration_factor=1,
                    zoom_factor=0,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=2,
                    function_mode=FSPFunctionMode.CORR,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=744,
                    output_link_map=[(0, 4), (200, 5)],
                    zoom_window_tuning=650000,
                ),
            ],
            vlbi_config={},
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)


def low_invalidator(o: ConfigureRequest):
    # function to make a valid LOW ConfigureRequest invalid
    o.mccs.subarray_beam_configs[0].subarray_beam_id = -1


def mid_invalidator(o: ConfigureRequest):
    # function to make a valid MID ConfigureRequest invalid
    o.tmc.scan_duration = timedelta(seconds=-10)


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ConfigureRequestSchema,
            VALID_MID_CONFIGURE_OBJECT,
            mid_invalidator,
            VALID_MID_CONFIGURE_JSON,
            INVALID_MID_CONFIGURE_JSON,
            True,
        ),
        (
            ConfigureRequestSchema,
            VALID_MID_DISH_ONLY_OBJECT,
            None,  # no validation on MID
            VALID_MID_DISH_ONLY_JSON,
            None,
            False,
        ),
        (
            ConfigureRequestSchema,
            VALID_NULL_OBJECT,
            None,  # no validation for null object
            VALID_NULL_JSON,
            None,
            False,
        ),
        (
            ConfigureRequestSchema,
            VALID_LOW_CONFIGURE_OBJECT,
            low_invalidator,
            VALID_LOW_CONFIGURE_JSON,
            INVALID_LOW_CONFIGURE_JSON,
            True,
        ),
        (
            ConfigureRequestSchema,
            VALID_LOW_CONFIGURE_OBJECT_PI17,
            None,
            VALID_LOW_CONFIGURE_JSON_PI17,
            None,
            False,
        ),
        (
            ConfigureRequestSchema,
            VALID_MID_CONFIGURE_OBJECT,
            None,
            VALID_MID_CONFIGURE_JSON,
            None,
            True,
        ),
    ],
)
def test_configure_serialisation_and_validation(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls,
        instance,
        modifier_fn,
        valid_json,
        invalid_json,
        is_validate,
    )


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ConfigureRequestSchema,
            NON_COMPLIANCE_MID_CONFIGURE_OBJECT,
            None,
            NON_COMPLIANCE_MID_CONFIGURE_JSON,
            None,
            True,
        ),
    ],
)
def test_configure_serialisation_and_validation_invalid_json(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly
    for invalid json and raise SchematicValidationError.
    """
    try:
        utils.test_schema_serialisation_and_validation(
            schema_cls,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
        )

    except SchematicValidationError as error:
        assert error.message == (
            "Invalid input for receiver_band! Currently allowed [1,2],"
            "FSPs are too many!Current Limit = 4,Invalid input for fsp_id!,"
            "Invalid input for function_mode,Invalid input for zoom_factor,"
            "frequency_slice_id did not match fsp_id,"
            "frequency_band did not match receiver_band"
        )
