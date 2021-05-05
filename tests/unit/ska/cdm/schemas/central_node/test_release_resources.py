"""
Unit tests for ska.cdm.schemas module.
"""

from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska.cdm.schemas.central_node.release_resources import ReleaseResourcesRequestSchema
from ska.cdm.utils import json_is_equal

VALID_RELEASE_RESOURCES_REQUEST = """
{
     "subarrayID": 1,
     "dish": {"receptorIDList": ["0001", "0002"]}
}
"""

VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = """
{
    "subarrayID": 1,
    "releaseALL": true
}
"""

VALID_LOW_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": 1,
    "release_all": true
}
"""

INVALID_LOW_RELEASE_RESOURCES_RELEASE_ALL_REQUEST = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": -1,
    "release_all": true
}
"""


def test_marshall_release_resources():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    request = ReleaseResourcesRequest(subarray_id_mid=1, dish_allocation=dish_allocation)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_REQUEST)


def test_marshall_release_resources_release_all():
    """
    Verify that ReleaseResourcesRequest with release_all_mid set is marshalled to
    JSON correctly.
    """
    request = ReleaseResourcesRequest(subarray_id_mid=1, release_all_mid=True)
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_marshall_release_resources_release_all_for_low():
    """
    Verify that ReleaseResourcesRequest with release_all_low set is marshalled to
    JSON correctly.
    """
    request = ReleaseResourcesRequest(
        interface='https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0',
        subarray_id_low=1,
        release_all_low=True
    )
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_LOW_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_release_resources_ignores_resources_when_release_all_is_specified():
    """
    Verify that other resource statements are excluded when release_all_mid is set
    to True.
    """
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    request = ReleaseResourcesRequest(
        subarray_id_mid=1, release_all_mid=True, dish_allocation=dish_allocation
    )
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)


def test_unmarshall_release_resources():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_REQUEST)
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    expected = ReleaseResourcesRequest(
        subarray_id_mid=1,
        dish_allocation=dish_allocation
    )
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all_mid is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = ReleaseResourcesRequest(subarray_id_mid=1, release_all_mid=True)
    assert request == expected


def test_unmarshall_release_resources_with_release_all_set_for_low():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all_low is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_LOW_RELEASE_RESOURCES_RELEASE_ALL_REQUEST)
    expected = ReleaseResourcesRequest(subarray_id_low=1, release_all_low=True,
                                       interface="https://schema.skatelescope.org/"
                                                 "ska-low-tmc-releaseresources/1.0"
                                       )
    assert request == expected
