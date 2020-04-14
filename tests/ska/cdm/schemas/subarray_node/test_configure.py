"""
Unit tests for the ska.cdm.schemas.subarray_node.configure module.
"""
import itertools

from datetime import timedelta

from ska.cdm.messages.subarray_node.configure import (
    ConfigureRequest,
    CSPConfiguration,
    DishConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    PointingConfiguration,
    ReceiverBand,
    SDPConfiguration,
    TMCConfiguration,
    Target,
)
from ska.cdm.schemas.subarray_node.configure import ConfigureRequestSchema
from tests.ska.cdm.schemas.utils import json_is_equal

VALID_CONFIGURE_REQUEST = """
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
        "channelAveragingMap": [
          [1,2], [745,0], [1489,0], [2233,0], [2977,0], [3721,0], [4465,0],
          [5209,0], [5953,0], [6697,0], [7441,0], [8185,0], [8929,0], [9673,0],
          [10417,0], [11161,0], [11905,0], [12649,0], [13393,0], [14137,0]
        ]
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


def test_marshall_configure_request():
    """
    Verify that ConfigureRequest is marshalled to JSON correctly.
    """
    scan_duration = timedelta(seconds=10)
    target = Target(
        ra="13:29:52.698",
        dec="+47:11:42.93",
        name="M51",
        frame="icrs",
        unit=("hourangle", "deg"),
    )
    pointing_config = PointingConfiguration(target)
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration("science_A")
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing_config, dish_config, sdp_config, csp_config, tmc_config
    )
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST)



def test_unmarshall_configure_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    scan_duration = timedelta(seconds=10)
    target = Target(
        ra="13:29:52.698",
        dec="+47:11:42.93",
        name="M51",
        frame="icrs",
        unit=("hourangle", "deg"),
    )
    pointing_config = PointingConfiguration(target)
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration("science_A")
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST)

    assert unmarshalled == expected


def test_unmarshall_configure_for_later_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    scan_duration = timedelta(seconds=10)
    target = Target(
        ra="13:29:52.698",
        dec="+47:11:42.93",
        name="M51",
        frame="icrs",
        unit=("hourangle", "deg"),
    )
    pointing_config = PointingConfiguration(target)
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)

    sdp_config = SDPConfiguration("science_A")

    csp_id = "sbi-mvp01-20200325-00001-science_A"
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config
    )
    unmarshalled = ConfigureRequestSchema().loads(
        VALID_CONFIGURE_REQUEST
    )

    assert expected.sdp == unmarshalled.sdp

    assert unmarshalled == expected


def test_optional_configurations_are_omitted_when_null():
    """
    Verify that 'null' JSON values corresponding to optional undefined
    ConfigureRequest values (CSP, SDP, DISH, etc.) are stripped.
    """
    request = ConfigureRequest()
    request_json = ConfigureRequestSchema().dumps(request)

    expected = '{}'
    assert json_is_equal(request_json, expected)


def test_configure_request_can_be_created_when_only_required_args_present():
    """
    Verify that a ConfigureRequest object can be unmarshalled from JSON when
    only the required attributes are present.
    """
    serialised = '{"dish": {"receiverBand": "1"} }'
    expected = ConfigureRequest(dish=DishConfiguration(ReceiverBand.BAND_1))
    unmarshalled = ConfigureRequestSchema().loads(serialised)
    assert expected == unmarshalled
