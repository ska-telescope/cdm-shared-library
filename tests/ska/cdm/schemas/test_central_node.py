"""
Unit tests for ska.cdm.schemas module.
"""

import ska.cdm.messages.central_node as cn
from ska.cdm.schemas.central_node import AssignResourcesRequestSchema
from ska.cdm.schemas.central_node import AssignResourcesResponseSchema
from ska.cdm.schemas.central_node import ReleaseResourcesRequestSchema
from .utils import json_is_equal

VALID_ASSIGN_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_ASSIGN_RESOURCES_RESPONSE = '{"dish": {"receptorIDList_success": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_REQUEST = '{"subarrayID": 1, "dish": {"receptorIDList": ["0001", "0002"]}}'
VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = '{"subarrayID": 1, "releaseALL": true}'


def test_marshall_assign_resources_request():
    """
    Verify that AssignResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.AssignResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = AssignResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_REQUEST)


def test_unmarshall_assign_resources_request():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesRequest
    object.
    """
    request = AssignResourcesRequestSchema().loads(VALID_ASSIGN_RESOURCES_REQUEST)
    expected = cn.AssignResourcesRequest(1, cn.DishAllocation(receptor_ids=['0001', '0002']))
    assert request == expected


def test_marshall_assign_resources_response():
    """
    Verify that AssignResourcesResponse is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    response = cn.AssignResourcesResponse(dish_allocation=dish_allocation)
    json_str = AssignResourcesResponseSchema().dumps(response)
    assert json_is_equal(json_str, VALID_ASSIGN_RESOURCES_RESPONSE)


def test_unmarshall_assign_resources_response():
    """
    Verify that JSON can be unmarshalled back to an AssignResourcesResponse
    object.
    """
    response = AssignResourcesResponseSchema().loads(VALID_ASSIGN_RESOURCES_RESPONSE)
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    expected = cn.AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response == expected


def test_marshall_release_resources():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_REQUEST)


def test_marshall_release_resources_release_all():
    """
    Verify that ReleaseResourcesRequest with release_all set is marshalled to
    JSON correctly.
    """
    request = cn.ReleaseResourcesRequest(1, release_all=True)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_release_resources_ignores_resources_when_release_all_is_specified():
    """
    Verify that other resource statements are excluded when release_all is set
    to True.
    """
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    request = cn.ReleaseResourcesRequest(1, release_all=True, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_unmarshall_release_resources():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_REQUEST)
    dish_allocation = cn.DishAllocation(receptor_ids=['0001', '0002'])
    expected = cn.ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = cn.ReleaseResourcesRequest(1, release_all=True)
    assert request == expected
