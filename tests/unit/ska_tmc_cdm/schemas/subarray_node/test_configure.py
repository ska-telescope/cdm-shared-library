"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure module.
"""

from datetime import timedelta

import pytest

from ska_tmc_cdm.messages.subarray_node.configure import SCHEMA, ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    Target,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    SubarrayConfiguration,
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
from ska_tmc_cdm.utils import assert_json_is_equal

from .. import utils

VALID_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.1",
  "transaction_id": "12345",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "M51",
      "ra": "13:29:52.698",
      "dec": "+47:11:42.93"
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
          "integration_factor": 10,
          "output_link_map": [[0,0], [200,1]],
          "zoom_factor": 0,
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 0
        },
        {
          "fsp_id": 2,
          "function_mode": "CORR",
          "frequency_slice_id": 2,
          "integration_factor": 10,
          "zoom_factor": 1,
          "output_link_map": [[0,4], [200,5]],
          "channel_averaging_map": [[0, 2], [744, 0]],
          "channel_offset": 744,
          "zoom_window_tuning": 4700000
        }
      ]
    }
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.3",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_MID_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.1",
    transaction_id="12345",
    pointing=PointingConfiguration(
        Target(
            ra="13:29:52.698",
            dec="+47:11:42.93",
            target_name="M51",
            reference_frame="icrs",
            unit=("hourangle", "deg"),
        )
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.3", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration("science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(
                    1,
                    FSPFunctionMode.CORR,
                    1,
                    10,
                    0,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    2,
                    FSPFunctionMode.CORR,
                    2,
                    10,
                    1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    channel_offset=744,
                    output_link_map=[(0, 4), (200, 5)],
                    zoom_window_tuning=4700000,
                ),
            ]
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)


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
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band":"1",
      "subarray_id": 1
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
            "dest_ip": [
              "10.22.0.1:2345",
              "10.22.0.3:3456"
            ],
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
      },
      "search_beams": "tbd",
      "zooms": "tbd"
      }
    }
}
"""

VALID_LOW_CONFIGURE_OBJECT_PI17 = ConfigureRequest(
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
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration(subarray_name="science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
        ),
        lowcbf=LowCBFConfiguration(
            stations={
                "stns": [[1, 0], [2, 0], [3, 0], [4, 0]],
                "stn_beams": [
                    {
                        "beam_id": 1,
                        "freq_ids": [64, 65, 66, 67, 68, 68, 70, 71],
                        "boresight_dly_poly": "url",
                    }
                ],
            },
            timing_beams={
                "beams": [
                    {
                        "pst_beam_id": 13,
                        "stn_beam_id": 1,
                        "offset_dly_poly": "url",
                        "stn_weights": [0.9, 1.0, 1.0, 0.9],
                        "jones": "url",
                        "dest_ip": ["10.22.0.1:2345", "10.22.0.3:3456"],
                        "dest_chans": [128, 256],
                        "rfi_enable": [True, True, True],
                        "rfi_static_chans": [1, 206, 997],
                        "rfi_dynamic_chans": [242, 1342],
                        "rfi_weighted": 0.87,
                    }
                ]
            },
            search_beams="tbd",
            zooms="tbd",
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


VALID_MID_CONFIGURE_JSON_PI16 = """
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


VALID_MID_CONFIGURE_OBJECT_PI16 = ConfigureRequest(
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


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ConfigureRequestSchema,
            VALID_MID_CONFIGURE_OBJECT,
            None,  # no validation on MID
            VALID_MID_CONFIGURE_JSON,
            None,
        ),  # no validation on MID
        (
            ConfigureRequestSchema,
            VALID_MID_DISH_ONLY_OBJECT,
            None,  # no validation on MID
            VALID_MID_DISH_ONLY_JSON,
            None,
        ),  # no validation on MID
        (
            ConfigureRequestSchema,
            VALID_NULL_OBJECT,
            None,  # no validation for null object
            VALID_NULL_JSON,
            None,
        ),
    ],
)
def test_configure_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )


def test_configure_serialisation_and_validation_pi16():
    """
    Verifies that the ConfigurationRequest schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls=ConfigureRequestSchema,
        instance=VALID_MID_CONFIGURE_OBJECT_PI16,
        modifier_fn=None,
        valid_json=VALID_MID_CONFIGURE_JSON_PI16,
        invalid_json=None,
    )


def test_configure_serialisation_and_validation_pi17():
    """
    Verifies that the ConfigurationRequest schema marshals, unmarshals, and validates correctly.
    """
    configure_configuration_object = ConfigureRequestSchema().loads(
        VALID_LOW_CONFIGURE_JSON_PI17
    )
    serialized_configure_config = ConfigureRequestSchema().dumps(
        configure_configuration_object
    )
    assert_json_is_equal(VALID_LOW_CONFIGURE_JSON_PI17, serialized_configure_config)
