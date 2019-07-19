"""
Unit tests for ska.cdm.schemas module.
"""
import json
import datetime

import ska.cdm.messages.central_node as cn
import ska.cdm.messages.subarray_node as sn
import ska.cdm.schemas as schemas

VALID_ASSIGN_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_ASSIGN_RESOURCES_RESPONSE = '{"dish": {"receptorIDList_success": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = '{"subarrayID": 1, "releaseALL": true}'

# These examples are taken verbatim from the SP-142 ICD
VALID_DISH_CONFIGURATION_JSON = '{"receiverBand": "5a"}'
VALID_TARGET_JSON = '{"RA": 0.5, "dec": 1.0, "system": "ICRS", "name": "NGC123"}'
VALID_CONFIGURE_REQUEST = """
{
  "pointing": {
    "target": {
      "system": "ICRS",
      "name": "NGC6251",
      "RA": 1.0,       
      "dec": 0.5      
    }
  },
  "dish": {
    "receiverBand": "1"
  }
}
"""
VALID_SCAN_REQUEST = '{"scan_duration": 10.0}'


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
    target = sn.Target(0.5, 1, name='NGC123')
    expected = VALID_TARGET_JSON
    json_str = schemas.TargetSchema().dumps(target)
    assert json_is_equal(json_str, expected)


def test_unmarshall_target_from_json():
    """
    Verify that a Target is unmarshalled correctly from JSON.
    """
    expected = sn.Target(0.5, 1.0, name='NGC123')
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
    target = sn.Target(ra=1, dec=0.5, name='NGC6251', frame='icrs')
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)

    request = sn.ConfigureRequest(pointing_config, dish_config)
    request_json = schemas.ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_REQUEST)


def test_unmarshall_configure_request_from_json():
    """
    Verify that a COnfigureRequest can be unmarshalled from JSON.
    """
    target = sn.Target(ra=1, dec=0.5, name='NGC6251', frame='icrs')
    pointing_config = sn.PointingConfiguration(target)
    dish_config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_1)
    expected = sn.ConfigureRequest(pointing_config, dish_config)

    unmarshalled = schemas.ConfigureRequestSchema().loads(VALID_CONFIGURE_REQUEST)

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
    unmarshalled = codec.loads(sn.ScanRequest, VALID_SCAN_REQUEST)

    duration = datetime.timedelta(seconds=10.0)
    expected = sn.ScanRequest(duration)

    assert unmarshalled == expected
