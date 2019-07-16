"""
Unit tests for ska.cdm.schemas module.
"""
import json

from ska.cdm.messages.central_node import AssignResourcesRequest, AssignResourcesResponse, \
    DishAllocation, ReleaseResourcesRequest
from ska.cdm.messages.subarray_node import PointingConfiguration, DishConfiguration,ConfigureRequest, ScanRequest
from ska.cdm.schemas import AssignResourcesRequestSchema, AssignResourcesResponseSchema, \
    ReleaseResourcesRequestSchema, ConfigureRequestSchema, MarshmallowCodec, ScanRequestSchema, ScanDurationSchema
from astropy.coordinates import SkyCoord
import datetime
from datetime import timedelta

VALID_ASSIGN_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = '{"subarrayID": 1, "releaseALL": true}'
VALID_ASSIGN_RESOURCES_RESPONSE = '{"dish": {"receptorIDList_success": ["0001", "0002"]}}'
VALID_ASSIGN_STARTSCAN_REQUEST = '{"scan_duration": 10.0}'

VALID_CONFIGURE_RESOURCES_REQUEST ='{"dish": {"receiverBand": "5a"}, "pointing": {"target": \
{"dec": 0.05235987755982989, "ra": 0.017453292519943295, "frame": "icrs", "name": "NGC123"}}}'

def json_is_equal(json_a, json_b):
    """
    Utility function to compare two JSON objects
    """
    # key/values in the generated JSON do not necessarily have the same order
    # as the test string, even though they are equivalent JSON objects, e.g.,
    # subarrayID could be defined after dish. Ensure a stable test by
    # comparing the JSON objects themselves.
    return json.loads(json_a) == json.loads(json_b)


def test_marshall_assign_resources_request():
    """
    Verify that AssignResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    request = AssignResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = AssignResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_REQUEST)


def test_unmarshall_assign_resources_request():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object.
    """
    request = AssignResourcesRequestSchema().loads(VALID_ASSIGN_RESOURCES_REQUEST)
    expected = AssignResourcesRequest(1, DishAllocation(receptor_ids=['0001', '0002']))
    assert request == expected


def test_marshall_assign_resources_response():
    """
    Verify that AssignResourcesResponse is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    json_str = AssignResourcesResponseSchema().dumps(response)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_RESPONSE)


def test_unmarshall_assign_resources_response():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesResponse
    object.
    """
    response = AssignResourcesResponseSchema().loads(VALID_ASSIGN_RESOURCES_RESPONSE)
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    expected = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response == expected


def test_marshall_release_resources():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    request = ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_REQUEST)


def test_marshall_release_resources_release_all():
    """
    Verify that ReleaseResourcesRequest with release_all set is marshalled to
    JSON correctly.
    """
    request = ReleaseResourcesRequest(1, release_all=True)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_release_resources_ignores_resources_when_release_all_is_specified():
    """
    Verify that other resource statements are excluded when release_all is set
    to True.
    """
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    request = ReleaseResourcesRequest(1, release_all=True, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_unmarshall_release_resources():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    request = ReleaseResourcesRequestSchema().loads(VALID_RELEASE_RESOURCES_REQUEST)
    dish_allocation = DishAllocation(receptor_ids=['0001', '0002'])
    expected = ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all is set.
    """
    request = ReleaseResourcesRequestSchema().loads(VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = ReleaseResourcesRequest(1, release_all=True)
    assert request == expected

def test_marshall_configure_subarray_request():
    """
    Verify that ConfigureRequest is marshalled to JSON correctly.
    """
    sky_coord = SkyCoord(ra=1, dec=3, unit='deg')
    sky_coord.info.name = 'NGC123'

    pointing_config = PointingConfiguration(sky_coord)
    dish_config = DishConfiguration('5a')

    request = ConfigureRequest(pointing_config, dish_config)
    request_json = ConfigureRequestSchema().dumps(request)

    assert json_is_equal(request_json, VALID_CONFIGURE_RESOURCES_REQUEST)

def test_marshall_start_scan_request():
    """
    Verify that StartScan is marshalled to JSON correctly.
    """

    first_date = '2019-01-01 08:00:00.000000'
    first_date_obj = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S.%f')

    second_date = '2019-01-01 08:00:10.000000'
    second_date_obj = datetime.datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S.%f')

    t = second_date_obj - first_date_obj

    scan_request = ScanRequest(t)
    ScanJson = ScanDurationSchema()

    result = ScanJson.dumps(scan_request)

    # TODO check why json_is_equal doesn't work properly with this JSON
    assert json_is_equal(result,VALID_ASSIGN_STARTSCAN_REQUEST)
    #assert result == VALID_ASSIGN_STARTSCAN_REQUEST1

def test_unmarshall_start_scan_request():
    """
    Verify that JSON can be unmarshalled back to a ScanDurationSchema
    object when ScanDuration is set.
    """

    first_date = '2019-01-01 08:00:00.000000'
    first_date_obj = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S.%f')

    second_date = '2019-01-01 08:00:10.000000'
    second_date_obj = datetime.datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S.%f')

    t = second_date_obj - first_date_obj

    request = ScanDurationSchema().loads(VALID_ASSIGN_STARTSCAN_REQUEST)


    expected = ScanRequest(t)
    assert request == expected
