"""
Unit tests for ska.cdm.schemas module.
"""
import datetime
import json

import ska.cdm.messages.central_node as cn
import ska.cdm.messages.subarray_node as sn
import ska.cdm.schemas as schemas
from ska.cdm.messages.subarray_node import SDPConfigurationBlock

VALID_ASSIGN_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_ASSIGN_RESOURCES_RESPONSE = '{"dish": {"receptorIDList_success": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = '{"subarrayID": 1, "releaseALL": true}'

# These examples are taken verbatim from the SP-142 ICD
VALID_DISH_CONFIGURATION_JSON = '{"receiverBand": "5a"}'
VALID_TARGET_JSON = """
{
  "RA": "12:34:56.78", 
  "dec": "+12:34:56.78", 
  "system": "ICRS", 
  "name": "NGC123"
}
"""
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
          "numChanels": 372,
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
          "12345": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ]
  }
}
"""

VALID_CONFIGURE_FOR_A_LATER_SCAN_REQUEST = """
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
  "sdp": {
    "configureScan": {
      "scanParameters": {
        "12346": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
  }
}
"""

VALID_SCAN_REQUEST = '{"scan_duration": 10.0}'

VALID_SDP_CONFIGURE = """
{
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
          "numChanels": 372,
          "numPolarisations": 4,
          "freqStartHz": 0.35e9,
          "freqEndHz": 1.05e9,
          "fields": {
            "0": { "system": "ICRS", "name": "NGC6251", "ra": 1.0, "dec": 1.0 }
          }
        },
        "scanParameters": {
          "12345": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ]
}
"""

VALID_SDP_CONFIGURE_SCAN = """
{
    "configureScan": {
      "scanParameters": {
        "12346": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
}
"""

VALID_SDP_CONFIGURE_AND_CONFIGURE_SCAN = """
{
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
          "numChanels": 372,
          "numPolarisations": 4,
          "freqStartHz": 0.35e9,
          "freqEndHz": 1.05e9,
          "fields": {
            "0": { "system": "ICRS", "name": "NGC6251", "ra": 1.0, "dec": 1.0 }
          }
        },
        "scanParameters": {
          "12345": { "fieldId": 0, "intervalMs": 1400 }
        }
      }
    ],
    "configureScan": {
      "scanParameters": {
        "12346": { "fieldId": 0, "intervalMs": 2800 }
      }
    }
}
"""


def json_is_equal(json_a, json_b):
    """
    Utility function to compare two JSON objects
    """
    # key/values in the generated JSON do not necessarily have the same order
    # as the test string, even though they are equivalent JSON objects, e.g.,
    # subarrayID could be defined after dish. Ensure a stable test by
    # comparing the JSON objects themselves.
    return json.loads(json_a) == json.loads(json_b)


def test_upper_cased_field_serialises_to_uppercase():
    """
    Verify that UpperCasedField serialises to uppercase text.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = 'bar'

    obj = TestObject()
    serialised = schemas.UpperCasedField().serialize('attr', obj)
    assert serialised == 'BAR'


def test_upper_cased_field_serialises_none():
    """
    Verify that UpperCasedField serialises None to an empty string.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = None

    obj = TestObject()
    serialised = schemas.UpperCasedField().serialize('attr', obj)
    assert serialised == ''


def test_upper_cased_field_deserialises_to_uppercase():
    """
    Verify that UpperCasedField deserialises to lowercase text.
    """
    deserialised = schemas.UpperCasedField().deserialize('FOO')
    assert deserialised == 'foo'


def test_marshall_assign_resources_request():
    """
    Verify that AssignResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.AssignResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = schemas.AssignResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_REQUEST)


def test_unmarshall_assign_resources_request():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object.
    """
    request = schemas.AssignResourcesRequestSchema().loads(VALID_ASSIGN_RESOURCES_REQUEST)
    expected = cn.AssignResourcesRequest(1, cn.DishAllocation(receptor_ids=['0001', '0002']))
    assert request == expected


def test_marshall_assign_resources_response():
    """
    Verify that AssignResourcesResponse is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    response = cn.AssignResourcesResponse(dish_allocation=dish_allocation)
    json_str = schemas.AssignResourcesResponseSchema().dumps(response)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_RESPONSE)


def test_unmarshall_assign_resources_response():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesResponse
    object.
    """
    response = schemas.AssignResourcesResponseSchema().loads(VALID_ASSIGN_RESOURCES_RESPONSE)
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    expected = cn.AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response == expected


def test_marshall_release_resources():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = schemas.ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_REQUEST)


def test_marshall_release_resources_release_all():
    """
    Verify that ReleaseResourcesRequest with release_all set is marshalled to
    JSON correctly.
    """
    request = cn.ReleaseResourcesRequest(1, release_all=True)
    json_str = schemas.ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_release_resources_ignores_resources_when_release_all_is_specified():
    """
    Verify that other resource statements are excluded when release_all is set
    to True.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.ReleaseResourcesRequest(1, release_all=True, dish_allocation=dish_allocation)
    json_str = schemas.ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_unmarshall_release_resources():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    schema = schemas.ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_REQUEST)
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    expected = cn.ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all is set.
    """
    schema = schemas.ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = cn.ReleaseResourcesRequest(1, release_all=True)
    assert request == expected


def test_marshall_target_to_json():
    """
    Verify that PointingConfiguration Target is marshalled to JSON correctly.
    """
    target = sn.Target(ra='12h34m56.78s', dec='+12d34m56.78s', name='NGC123')
    expected = VALID_TARGET_JSON
    json_str = schemas.TargetSchema().dumps(target)
    assert json_is_equal(json_str, expected)


def test_unmarshall_target_from_json():
    """
    Verify that a Target is unmarshalled correctly from JSON.
    """
    expected = sn.Target(ra='12h34m56.78s', dec='+12d34m56.78s', name='NGC123')
    unmarshalled = schemas.TargetSchema().loads(VALID_TARGET_JSON)
    assert unmarshalled == expected


def test_marshall_dish_configuration_to_json():
    """
    Verify that DishConfiguration is marshalled to JSON correctly.
    """
    config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_5A)
    json_str = schemas.DishConfigurationSchema().dumps(config)
    assert json_str == VALID_DISH_CONFIGURATION_JSON


def test_unmarshall_dish_configuration_from_json():
    """
    Verify that JSON can be unmarshalled to a DishConfiguration
    """
    expected = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_5A)
    unmarshalled = schemas.DishConfigurationSchema().loads(VALID_DISH_CONFIGURATION_JSON)
    assert unmarshalled == expected


def test_marshall_configure_request():
    """
    Verify that ConfigureRequest is marshalled to JSON correctly.
    """
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    sdp_configure = sdp_configure_for_test(target)

    request = sn.ConfigureRequest(123, pointing_config, dish_config, sdp_configure)
    request_json = schemas.ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST)


def sdp_configure_for_test(target):
    """Utility method to create an SDPConfigure request for use in tests"""
    target_list = {"0": target}
    workflow = sn.SDPWorkflow(wf_id="vis_ingest", wf_type="realtime", version="0.1.0")
    parameters = sn.SDPParameters(num_stations=4, num_chanels=372,
                                  num_polarisations=4, freq_start_hz=0.35e9,
                                  freq_end_hz=1.05e9, target_fields=target_list)
    scan = sn.SDPScan(field_id=0, interval_ms=1400)
    scan_list = {"12345": scan}
    sdp_config_block = sn.SDPConfigurationBlock(sb_id='realtime-20190627-0001',
                                                sbi_id='20190627-0001',
                                                workflow=workflow,
                                                parameters=parameters,
                                                scan_parameters=scan_list)
    sdp_configure = sn.SDPConfigure([sdp_config_block])
    return sdp_configure


def sdp_configure_scan_for_test():
    """Utility method to create an SDPConfigureScan request for use in tests"""
    scan = sn.SDPScan(field_id=0, interval_ms=2800)
    scan_list = {"12346": scan}

    scan_parameters = sn.SDPScanParameters(scan_list)
    configure_scan = sn.SDPConfigureScan(scan_parameters)
    return configure_scan


def test_unmarshall_configure_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    sdp_configure = sdp_configure_for_test(target)
    expected = sn.ConfigureRequest(123, pointing_config, dish_config, sdp_configure)

    unmarshalled = schemas.ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST)

    assert unmarshalled == expected


def test_unmarshall_configure_for_later_request_from_json():
    """
    Verify that a ConfigureRequest can be unmarshalled from JSON.
    """
    target = sn.Target(ra='13:29:52.698', dec='+47:11:42.93', name='M51', frame='icrs',
                       unit=('hourangle', 'deg'))
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    sdp_configure_scan = sdp_configure_scan_for_test()
    expected = sn.ConfigureRequest(123, pointing_config, dish_config, sdp_configure_scan)

    unmarshalled = schemas.ConfigureRequestSchema().loads(VALID_CONFIGURE_FOR_A_LATER_SCAN_REQUEST)

    assert unmarshalled == expected


def test_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    codec = schemas.MarshmallowCodec()
    unmarshalled = codec.loads(cn.AssignResourcesRequest, VALID_ASSIGN_RESOURCES_REQUEST)
    expected = cn.AssignResourcesRequest(1, cn.DishAllocation(receptor_ids=['0001', '0002']))
    assert expected == unmarshalled


def test_codec_dumps():
    """
    Verify that the codec marshalls objects to JSON.
    """
    expected = VALID_ASSIGN_RESOURCES_REQUEST
    obj = cn.AssignResourcesRequest(1, cn.DishAllocation(receptor_ids=['0001', '0002']))
    marshalled = schemas.MarshmallowCodec().dumps(obj)
    assert expected == marshalled


def test_marshall_start_scan_request():
    """
    Verify that ScanRequest is marshalled to JSON correctly.
    """
    duration = datetime.timedelta(seconds=10.0)
    scan_request = sn.ScanRequest(duration)
    schema = schemas.ScanRequestSchema()
    result = schema.dumps(scan_request)

    assert json_is_equal(result, VALID_SCAN_REQUEST)


def test_unmarshall_start_scan_request():
    """
    Verify that JSON can be unmarshalled back to a ScanRequest
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.ScanRequest, VALID_SCAN_REQUEST)
    assert result


def test_marshal_sdp_configure_scan():
    """
    Verify that ConfigureScan can be marshalled to JSON correctly
    """
    request = sdp_configure_scan_for_test()
    schema = schemas.SDPConfigureScanSchema()
    result = schema.dumps(request)
    assert json_is_equal(result, VALID_SDP_CONFIGURE_SCAN)


def test_unmarshall_sdp_configure_scan():
    """
    Verify that JSON can be unmarshalled back to a ConfigureScan
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.SDPConfigureScan, VALID_SDP_CONFIGURE_SCAN)
    scan_parameters = result.configure_scan.scan_parameters
    assert '12346' in scan_parameters.keys()


def test_marshal_sdp_configure_request():
    """
    Verify that JSON can be marshalled to JSON correctly
    """
    sb_id = 'realtime-20190627-0001'
    sbi_id = '20190627-0001'
    target = sn.Target(ra=1.0, dec=1.0, name="NGC6251", unit="rad")
    target_list = {"0": target}

    workflow = sn.SDPWorkflow(wf_id="vis_ingest", wf_type="realtime", version="0.1.0")

    parameters = sn.SDPParameters(num_stations=4, num_chanels=372,
                                  num_polarisations=4, freq_start_hz=0.35e9,
                                  freq_end_hz=1.05e9, target_fields=target_list)
    scan = sn.SDPScan(field_id=0, interval_ms=1400)
    scan_list = {"12345": scan}

    sdp_config_block = sn.SDPConfigurationBlock(sb_id=sb_id,
                                                sbi_id=sbi_id,
                                                workflow=workflow,
                                                parameters=parameters,
                                                scan_parameters=scan_list)

    sdp_configure = sn.SDPConfigure([sdp_config_block])
    schema = schemas.SDPConfigureSchema()

    result = schema.dumps(sdp_configure)
    print("Result is ", result)
    assert json_is_equal(result, VALID_SDP_CONFIGURE)


def test_marshal_sdp_configure_scan_request():
    """
    Verify that JSON can be marshalled to JSON correctly
    """
    configure_scan = sdp_configure_scan_for_test()
    schema = schemas.SDPConfigureScanSchema()
    result = schema.dumps(configure_scan)
    assert json_is_equal(result, VALID_SDP_CONFIGURE_SCAN)


def test_unmarshall_sdp_configure_request():
    """
    Verify that JSON can be unmarshalled back to a ScanRequest
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.SDPConfigure, VALID_SDP_CONFIGURE)
    config_block = result.configure[0]
    assert isinstance(config_block, SDPConfigurationBlock)


def test_unmarshall_sdp_configure_scan_request():
    """
    Verify that JSON can be unmarshalled back to a ScanRequest
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.SDPConfigureScan, VALID_SDP_CONFIGURE_SCAN)
    scan_parameters = result.configure_scan.scan_parameters
    assert '12346' in scan_parameters.keys()


def test_unmarshall_both_sdp_configure_and_configure_scan_request():
    """
    Nominal test for documentation - if both configure and confgureScan are
    provided currently the configure will be read into an object but not the
    configureScan as this is considered redundant
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.SDPConfigure, VALID_SDP_CONFIGURE_AND_CONFIGURE_SCAN)
    config_block = result.configure[0]
    assert isinstance(config_block, SDPConfigurationBlock)




def test_unmarshall_empty_sdp_configure_request():
    """
    Nominal test  - more for documentation - since both configure and confgureScan are optional
    it is technically possible to have an sdp configuration that is empty.
    Placeholder for a test if we close this down.
    """
    codec = schemas.MarshmallowCodec()
    result = codec.loads(sn.SDPConfigure, "{}")
    assert result == {}



def test_read_a_file_from_disk():
    """Test for loading a configure request from a JSON file"""
    codec = schemas.MarshmallowCodec()
    result = codec.load_from_file(sn.ConfigureRequest, "./tests/testfile_sample_configure.json")
    assert result.scan_id == 123
