"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure module.
"""
import copy

import pytest
from datetime import timedelta

from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
    PointingConfiguration,
    Target,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CommonConfiguration,
    CBFConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget
)
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska_tmc_cdm.schemas.subarray_node.configure import ConfigureRequestSchema
from .. import utils

VALID_MID_CONFIGURE_JSON = """
{
  "pointing": {
    "target": {
      "system": "ICRS",
      "name": "M51",
      "RA": "13:29:52.698",
      "dec": "+47:11:42.93"
    }
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
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
    "interface": "https://schema.skao.int/ska-sdp-configure/1.0",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_MID_CONFIGURE_OBJECT = ConfigureRequest(
    pointing=PointingConfiguration(
        Target(
            ra="13:29:52.698",
            dec="+47:11:42.93",
            name="M51",
            frame="icrs",
            unit=("hourangle", "deg"),
        )
    ),
    dish=DishConfiguration(
        receiver_band=ReceiverBand.BAND_1
    ),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/1.0",
        scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skatelescope.org/ska-csp-configure/1.0",
        subarray_config=SubarrayConfiguration('science period 23'),
        common_config=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            [
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
                )
            ]
        )
    ),
    tmc=TMCConfiguration(
        scan_duration=timedelta(seconds=10)
    )
)


VALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-configure/1.0",
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
          "system": "horizon",
          "name": "DriftScan",
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
    interface="https://schema.skatelescope.org/ska-low-tmc-configure/1.0",
    mccs=MCCSConfiguration(
        station_configs=[
            StnConfiguration(1),
            StnConfiguration(2)
        ],
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                station_ids=[1, 2],
                channels=[
                    [0, 8, 1, 1],
                    [8, 8, 2, 1],
                    [24, 16, 2, 1]
                ],
                update_rate=0.0,
                target=SubarrayBeamTarget(180.0, 45.0, "DriftScan", "horizon"),
                antenna_weights=[1.0, 1.0, 1.0],
                phase_centre=[0.0, 0.0]
            )
        ]
    ),
    tmc=TMCConfiguration(
        scan_duration=timedelta(seconds=10)
    )
)

INVALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-configure/1.0",
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
              "system": "horizon",
              "name": "DriftScan",
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

VALID_MID_DISH_ONLY_JSON = """
{
    "dish": {
        "receiver_band": "1"
    }
}
"""

VALID_MID_DISH_ONLY_OBJECT = ConfigureRequest(
    dish=DishConfiguration(ReceiverBand.BAND_1)
)

VALID_NULL_JSON = "{}"

VALID_NULL_OBJECT = ConfigureRequest()


def low_invalidator(o: ConfigureRequest):
    # function to make a valid LOW ConfigureRequest invalid
    o.mccs.subarray_beam_configs[0].subarray_beam_id = -1


@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (ConfigureRequestSchema,
         VALID_MID_DISH_ONLY_OBJECT,
         None,  # no validation on MID
         VALID_MID_DISH_ONLY_JSON,
         None),  # no validation on MID
        (ConfigureRequestSchema,
         VALID_NULL_OBJECT,
         None,  # no validation for null object
         VALID_NULL_JSON,
         None),  # no validation for null object
        (ConfigureRequestSchema,
         VALID_LOW_CONFIGURE_OBJECT,
         low_invalidator,  # no validation on MID
         VALID_LOW_CONFIGURE_JSON,
         INVALID_LOW_CONFIGURE_JSON),  # no validation on MID
    ]
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


# TODO put test back in above before merging AT2-855
@pytest.mark.xfail
@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (ConfigureRequestSchema,
         VALID_MID_CONFIGURE_OBJECT,
         None,  # no validation on MID
         VALID_MID_CONFIGURE_JSON,
         None),  # no validation on MID
    ]
)
def test_configure_fails_validation_due_to_outdated_telescope_model(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Placeholder for tests that should pass again once ADR-35 Telescope Model
    is released.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )
