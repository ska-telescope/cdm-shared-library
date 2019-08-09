"""
Unit tests for the ska.cdm.schemas.subarray_node.configure module.
"""
import itertools

import ska.cdm.messages.subarray_node as sn
import ska.cdm.schemas.subarray_node as schemas
from tests.ska.cdm.schemas.subarray_node.configure.test_sdp import \
    get_sdp_scan_configuration_for_test
from tests.ska.cdm.schemas.utils import json_is_equal

VALID_CONFIGURE_REQUEST = """
{
  "scanID": 123,
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
    "configure": [
      {
        "id": "realtime-20190627-0001",
        "sbiId": "20190627-0001",
        "workflow": {
          "id": "vis_ingest",
          "type": "realtime",
          "version": "0.1.0"
        },
        "parameters": {
          "numStations": 4,
          "numChannels": 372,
          "numPolarisations": 4,
          "freqStartHz": 0.35e9,
          "freqEndHz": 1.05e9,
          "fields": {
            "0": { 
            "system": "ICRS",
             "name": "M51", 
             "ra": 3.5337607188635975, 
             "dec": 0.8237126492459581 
             }
          }
        },
        "scanParameters": {
          "123": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ]
  }
}
"""

VALID_CONFIGURE_FOR_A_LATER_SCAN_REQUEST = """
{
  "scanID": 456,
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
    "configureScan": {
      "scanParameters": {
        "456": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
  }
}
"""


def sdp_configure_for_test(target, scan_id):
    """
    Utility method to create an SDPConfiguration for use in unit test
    """
    target_list = {'0': target}
    workflow = sn.SDPWorkflow(workflow_id='vis_ingest', workflow_type='realtime', version='0.1.0')
    parameters = sn.SDPParameters(num_stations=4, num_channels=372,
                                  num_polarisations=4, freq_start_hz=0.35e9,
                                  freq_end_hz=1.05e9, target_fields=target_list)
    scan = sn.SDPScan(field_id=0, interval_ms=1400)
    scan_list = {str(scan_id): scan}
    pb_config = sn.ProcessingBlockConfiguration(sb_id='realtime-20190627-0001',
                                                sbi_id='20190627-0001',
                                                workflow=workflow,
                                                parameters=parameters,
                                                scan_parameters=scan_list)
    sdp_configure = sn.SDPConfiguration(configure=[pb_config])
    return sdp_configure


def test_marshall_configure_request():
    """
    Verify that ConfigureRequest is marshalled to JSON correctly.
    """
    scan_id = 123
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    sdp_config = sdp_configure_for_test(target, scan_id)
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = sn.FSPConfiguration(1, sn.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = sn.CSPConfiguration(sn.ReceiverBand.BAND_1, [fsp_config])

    request = sn.ConfigureRequest(scan_id, pointing_config, dish_config, sdp_config, csp_config)
    request_json = schemas.ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST)


def test_unmarshall_configure_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    scan_id = 123
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    sdp_configure = sdp_configure_for_test(target, scan_id)
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = sn.FSPConfiguration(1, sn.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = sn.CSPConfiguration(sn.ReceiverBand.BAND_1, [fsp_config])

    expected = sn.ConfigureRequest(scan_id, pointing=pointing_config, dish=dish_config,
                                   sdp=sdp_configure, csp=csp_config)
    unmarshalled = schemas.ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST)

    assert unmarshalled == expected


def test_unmarshall_configure_for_later_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    scan_id = 456
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)

    sdp_configure_scan = get_sdp_scan_configuration_for_test(scan_id)

    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    fsp_config = sn.FSPConfiguration(1, sn.FSPFunctionMode.CORR, 1, 1400, 0, channel_avg_map)
    csp_config = sn.CSPConfiguration(sn.ReceiverBand.BAND_1, [fsp_config])

    expected = sn.ConfigureRequest(scan_id, pointing=pointing_config, dish=dish_config,
                                   sdp=sdp_configure_scan, csp=csp_config)
    unmarshalled = schemas.ConfigureRequestSchema().loads(VALID_CONFIGURE_FOR_A_LATER_SCAN_REQUEST)

    assert expected.sdp == unmarshalled.sdp

    assert unmarshalled == expected
