"""
Unit tests for the ska.cdm.schemas.subarray_node.configure module.
"""
import copy

import pytest
from datetime import timedelta

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
    PointingConfiguration,
    Target,
)
from ska.cdm.messages.subarray_node.configure.csp import (
    CommonConfiguration,
    CBFConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
)
from ska.cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget
)
from ska.cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.schemas.subarray_node.configure import ConfigureRequestSchema
from ska.cdm.utils import json_is_equal

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
    "scanDuration": 10.0
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
    "scanDuration": 10.0
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
    "scanDuration": 10.0
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


@pytest.mark.parametrize('instance, expected', [
    (VALID_MID_CONFIGURE_OBJECT, VALID_MID_CONFIGURE_JSON),
    (VALID_MID_CONFIGURE_PRE_ADR18_OBJECT, VALID_MID_CONFIGURE_PRE_ADR18_JSON),
    (VALID_MID_NO_CSP_CHANAVGMAP_OBJECT, VALID_MID_NO_CSP_CHANAVGMAP_JSON),
    (VALID_LOW_CONFIGURE_OBJECT, VALID_LOW_CONFIGURE_JSON),
    (VALID_MID_DISH_ONLY_OBJECT, VALID_MID_DISH_ONLY_JSON),
    (VALID_NULL_OBJECT, VALID_NULL_JSON)
])
def test_marshal(instance, expected):
    """
    Verify that ConfigureRequest is marshaled to JSON correctly.
    """
    schema = ConfigureRequestSchema()
    marshaled = schema.dumps(instance)
    assert json_is_equal(marshaled, expected)


@pytest.mark.parametrize('json_str,expected', [
    (VALID_MID_CONFIGURE_JSON, VALID_MID_CONFIGURE_OBJECT),
    (VALID_MID_CONFIGURE_PRE_ADR18_JSON, VALID_MID_CONFIGURE_PRE_ADR18_OBJECT),
    (VALID_MID_NO_CSP_CHANAVGMAP_JSON, VALID_MID_NO_CSP_CHANAVGMAP_OBJECT),
    (VALID_LOW_CONFIGURE_JSON, VALID_LOW_CONFIGURE_OBJECT),
    (VALID_MID_DISH_ONLY_JSON, VALID_MID_DISH_ONLY_OBJECT),
    (VALID_NULL_JSON, VALID_NULL_OBJECT)
])
def test_unmarshal(json_str, expected):
    """
    Verify that JSON is marshaled to a ConfigureRequest correctly.
    """
    schema = ConfigureRequestSchema()
    unmarshaled = schema.loads(json_str)
    assert unmarshaled == expected


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_LOW_CONFIGURE_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_LOW_CONFIGURE_OBJECT)
    o.mccs.subarray_beam_configs[0].subarray_beam_id = -1

    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_object_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = ConfigureRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_LOW_CONFIGURE_OBJECT)
