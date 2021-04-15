"""
Unit tests for the ska.cdm.schemas.subarray_node.configure module.
"""

from datetime import timedelta

from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska.cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import StnConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import SubarrayBeamConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import SubarrayBeamTarget
from ska.cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from ska.cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
)
from ska.cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
    PointingConfiguration,
    Target,
)
from ska.cdm.schemas.subarray_node.configure import ConfigureRequestSchema
from ska.cdm.utils import json_is_equal

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
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    # TODO refactor this as a builder, consolidate duplicate code
    fsp_config_1 = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)],
    )
    fsp_config_2 = FSPConfiguration(
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
    csp_config = CSPConfiguration(
        csp_id, ReceiverBand.BAND_1, [fsp_config_1, fsp_config_2]
    )
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
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
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config_1 = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)],
    )
    fsp_config_2 = FSPConfiguration(
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
    csp_config = CSPConfiguration(
        csp_id, ReceiverBand.BAND_1, [fsp_config_1, fsp_config_2]
    )
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
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
    fsp_config_1 = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_averaging_map=[(0, 2), (744, 0)],
        fsp_channel_offset=0,
        output_link_map=[(0, 0), (200, 1)],
    )
    fsp_config_2 = FSPConfiguration(
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
    csp_config = CSPConfiguration(
        csp_id, ReceiverBand.BAND_1, [fsp_config_1, fsp_config_2]
    )
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST)

    assert expected.sdp == unmarshalled.sdp

    assert unmarshalled == expected


VALID_CONFIGURE_REQUEST_NO_CAM = """
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


def test_marshall_configure_request_no_cam():
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
    channel_avg_map = None
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST_NO_CAM)


def test_unmarshall_configure_request_from_json_no_cam():
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
    channel_avg_map = None
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_NO_CAM)

    assert unmarshalled == expected


def test_unmarshall_configure_for_later_request_from_json_no_cam():
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
    channel_avg_map = None
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_NO_CAM)

    assert expected.sdp == unmarshalled.sdp

    assert unmarshalled == expected


VALID_CONFIGURE_REQUEST_OLM = """
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
        "outputLinkMap": [[1,0], [201,1]]
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


def test_marshall_configure_request_olm():
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
    channel_avg_map = None
    output_link_map = [(1, 0), (201, 1)]
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        output_link_map=output_link_map,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST_OLM)


def test_unmarshall_configure_request_from_json_olm():
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
    channel_avg_map = None
    output_link_map = [(1, 0), (201, 1)]
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        output_link_map=output_link_map,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_OLM)

    assert unmarshalled == expected


def test_unmarshall_configure_for_later_request_from_json_olm():
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
    channel_avg_map = None
    output_link_map = [(1, 0), (201, 1)]
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        output_link_map=output_link_map,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_OLM)

    assert expected.sdp == unmarshalled.sdp

    assert unmarshalled == expected


VALID_CONFIGURE_REQUEST_OCO = """
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
        "fspChannelOffset": 12
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


def test_marshall_configure_request_oco():
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
    channel_avg_map = None
    fsp_channel_offset = 12
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        fsp_channel_offset=fsp_channel_offset,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST_OCO)


def test_unmarshall_configure_request_from_json_oco():
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
    channel_avg_map = None
    fsp_channel_offset = 12
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        fsp_channel_offset=fsp_channel_offset,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_OCO)

    assert unmarshalled == expected


VALID_CONFIGURE_REQUEST_ZOOM = """
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


def test_marshall_configure_request_zoom():
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
    channel_avg_map = None
    zoom_window_tuning = 4700000
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        zoom_window_tuning=zoom_window_tuning,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    request = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST_ZOOM)


def test_unmarshall_configure_request_from_json_zoom():
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
    channel_avg_map = None
    zoom_window_tuning = 4700000
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(
        1,
        FSPFunctionMode.CORR,
        1,
        1400,
        0,
        channel_avg_map,
        zoom_window_tuning=zoom_window_tuning,
    )
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    tmc_config = TMCConfiguration(scan_duration)

    expected = ConfigureRequest(
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
        tmc=tmc_config,
    )
    unmarshalled = ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST_ZOOM)

    assert unmarshalled == expected


def test_optional_configurations_are_omitted_when_null():
    """
    Verify that 'null' JSON values corresponding to optional undefined
    ConfigureRequest values (CSP, SDP, DISH, etc.) are stripped.
    """
    request = ConfigureRequest()
    request_json = ConfigureRequestSchema().dumps(request)

    expected = "{}"
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


def test_configure_request_can_be_created_when_only_mccs_present():
    """
    Verify that a ConfigureRequest object can be unmarshalled from JSON when
    only the required attributes are present.
    """
    serialised = """{
      "mccs": {
        "stations":[
          {
            "station_id": 1
          }
        ],
        "subarray_beams": [
          {
            "subarray_beam_id":1,
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
    }"""
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "horizon")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration([station_config], [station_beam_config])
    expected = ConfigureRequest(mccs=mccs_config)
    unmarshalled = ConfigureRequestSchema().loads(serialised)
    assert expected == unmarshalled
