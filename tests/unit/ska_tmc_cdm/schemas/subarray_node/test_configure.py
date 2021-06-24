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
    "receiverBand": "1"
  },
  "csp": {
    "interface": "https://schema.skatelescope.org/ska-csp-configure/1.0",
    "subarray": {
      "subarrayName": "science period 23"
    },
    "common": {
      "id": "sbi-mvp01-20200325-00001-science_A",
      "frequencyBand": "1",
      "subarrayID": 1
    },
    "cbf": {
      "fsp": [
        {
          "fspID": 1,
          "functionMode": "CORR",
          "frequencySliceID": 1,
          "integrationTime": 1400,
          "outputLinkMap": [[0,0], [200,1]],
          "corrBandwidth": 0,
          "channelAveragingMap": [[0, 2], [744, 0]],
          "fspChannelOffset": 0
        },
        {
          "fspID": 2,
          "functionMode": "CORR",
          "frequencySliceID": 2,
          "integrationTime": 1400,
          "corrBandwidth": 1,
          "outputLinkMap": [[0,4], [200,5]],
          "channelAveragingMap": [[0, 2], [744, 0]],
          "fspChannelOffset": 744,
          "zoomWindowTuning": 4700000
        }
      ]
    }
  },
  "sdp": {
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
    sdp=SDPConfiguration("science_A"),
    csp=CSPConfiguration(
        interface="https://schema.skatelescope.org/ska-csp-configure/1.0",
        subarray_config=SubarrayConfiguration('science period 23'),
        common_config=CommonConfiguration(
            "sbi-mvp01-20200325-00001-science_A",
            ReceiverBand.BAND_1,
            1
        ),
        cbf_config=CBFConfiguration(
            [
                FSPConfiguration(
                    1,
                    FSPFunctionMode.CORR,
                    1,
                    1400,
                    0,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    fsp_channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    2,
                    FSPFunctionMode.CORR,
                    2,
                    1400,
                    1,
                    channel_averaging_map=[(0, 2), (744, 0)],
                    fsp_channel_offset=744,
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

VALID_MID_CONFIGURE_PRE_ADR18_JSON = """
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
    "receiverBand": "1"
  },
  "csp":{
    "id": "sbi-mvp01-20200325-00001-science_A",
    "frequencyBand": "1",
    "fsp": [
      {
        "fspID": 1,
        "functionMode": "CORR",
        "frequencySliceID": 1,
        "integrationTime": 1400,
        "corrBandwidth": 0,
        "channelAveragingMap": [[0,2], [744,0]],
        "fspChannelOffset": 0,
        "outputLinkMap": [[0,0], [200,1]]
      },
      {
        "fspID": 2,
        "functionMode": "CORR",
        "frequencySliceID": 2,
        "integrationTime": 1400,
        "corrBandwidth": 1,
        "channelAveragingMap": [[0,2], [744,0]],
        "fspChannelOffset": 744,
        "outputLinkMap": [[0,4], [200,5]],
        "zoomWindowTuning": 4700000
      }
    ]
  },
  "sdp": {
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

# CSP had a different format prior to ADR-18
VALID_MID_CONFIGURE_PRE_ADR18_OBJECT = copy.deepcopy(VALID_MID_CONFIGURE_OBJECT)
VALID_MID_CONFIGURE_PRE_ADR18_OBJECT.csp = CSPConfiguration(
    csp_id="sbi-mvp01-20200325-00001-science_A",
    frequency_band=ReceiverBand.BAND_1,
    fsp_configs=[
        FSPConfiguration(
            1,
            FSPFunctionMode.CORR,
            1,
            1400,
            0,
            channel_averaging_map=[(0, 2), (744, 0)],
            fsp_channel_offset=0,
            output_link_map=[(0, 0), (200, 1)],
        ),
        FSPConfiguration(
            2,
            FSPFunctionMode.CORR,
            2,
            1400,
            1,
            channel_averaging_map=[(0, 2), (744, 0)],
            fsp_channel_offset=744,
            output_link_map=[(0, 4), (200, 5)],
            zoom_window_tuning=4700000,
        )
    ]
)

VALID_MID_NO_CSP_CHANAVGMAP_JSON = """
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
    "receiverBand": "1"
  },
  "csp":{
    "id": "sbi-mvp01-20200325-00001-science_A",
    "frequencyBand": "1",
    "fsp": [
      {
        "fspID": 1,
        "functionMode": "CORR",
        "frequencySliceID": 1,
        "integrationTime": 1400,
        "corrBandwidth": 0
      }
    ]
  },
  "sdp": {
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_MID_NO_CSP_CHANAVGMAP_OBJECT = ConfigureRequest(
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
    sdp=SDPConfiguration("science_A"),
    csp=CSPConfiguration(
        csp_id="sbi-mvp01-20200325-00001-science_A",
        frequency_band=ReceiverBand.BAND_1,
        fsp_configs=[
            FSPConfiguration(
                1,
                FSPFunctionMode.CORR,
                1,
                1400,
                0,
                channel_averaging_map=None
            )
        ]
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
        "receiverBand": "1"
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
         VALID_MID_CONFIGURE_OBJECT,
         None,  # no validation on MID
         VALID_MID_CONFIGURE_JSON,
         None),  # no validation on MID
        (ConfigureRequestSchema,
         VALID_MID_CONFIGURE_PRE_ADR18_OBJECT,
         None,  # no validation on MID
         VALID_MID_CONFIGURE_PRE_ADR18_JSON,
         None),  # no validation on MID
        (ConfigureRequestSchema,
         VALID_MID_DISH_ONLY_OBJECT,
         None,  # no validation on MID
         VALID_MID_DISH_ONLY_JSON,
         None),  # no validation on MID
        (ConfigureRequestSchema,
         VALID_MID_NO_CSP_CHANAVGMAP_OBJECT,
         None,  # no validation on MID
         VALID_MID_NO_CSP_CHANAVGMAP_JSON,
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
def test_releaseresources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )
