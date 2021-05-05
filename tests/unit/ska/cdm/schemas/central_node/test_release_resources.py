"""
Unit tests for ska.cdm.schemas module.
"""

import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska.cdm.schemas.central_node.release_resources import ReleaseResourcesRequestSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_MID_PARTIAL_RELEASE_JSON = """
{
     "subarrayID": 1,
     "dish": {"receptorIDList": ["0001", "0002"]}
}
"""

VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    subarray_id_mid=1,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"])
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "subarrayID": 1,
    "releaseALL": true
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    subarray_id_mid=1,
    release_all_mid=True
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": 1,
    "release_all": true
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    subarray_id_low=1,
    release_all_low=True
)

INVALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": -1,
    "release_all": true
}
"""


def test_marshal_mid_partial_release():
    """
    Verify that a SKA MID ReleaseResourcesRequest is marshaled to JSON correctly.
    """
    schema = ReleaseResourcesRequestSchema()
    json_str = schema.dumps(VALID_MID_PARTIAL_RELEASE_OBJECT)
    assert json_is_equal(json_str, VALID_MID_PARTIAL_RELEASE_JSON)


def test_marshal_mid_full_release():
    """
    Verify that MID ReleaseResourcesRequest with release_all_mid set is marshaled to
    JSON correctly.
    """
    schema = ReleaseResourcesRequestSchema()
    json_str = schema.dumps(VALID_MID_FULL_RELEASE_OBJECT)
    assert json_is_equal(json_str, VALID_MID_FULL_RELEASE_JSON)


def test_marshal_low_full_release():
    """
    Verify that ReleaseResourcesRequest with release_all_low set is marshaled to
    JSON correctly.
    """
    request = ReleaseResourcesRequest(
        interface='https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0',
        subarray_id_low=1,
        release_all_low=True
    )
    json_str = ReleaseResourcesRequestSchema().dumps(request)
    assert json_is_equal(json_str, VALID_LOW_FULL_RELEASE_JSON)


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
    assert json_is_equal(json_str, VALID_MID_FULL_RELEASE_JSON)


def test_unmarshal_mid_partial_release():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_MID_PARTIAL_RELEASE_JSON)
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    expected = ReleaseResourcesRequest(
        subarray_id_mid=1,
        dish_allocation=dish_allocation
    )
    assert request == expected


def test_unmarshal_mid_full_release():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all_mid is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_MID_FULL_RELEASE_JSON)
    expected = ReleaseResourcesRequest(subarray_id_mid=1, release_all_mid=True)
    assert request == expected


def test_unmarshal_low_full_release():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object when release_all_low is set.
    """
    schema = ReleaseResourcesRequestSchema()
    request = schema.loads(VALID_LOW_FULL_RELEASE_JSON)
    expected = ReleaseResourcesRequest(
        interface="https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
        subarray_id_low=1,
        release_all_low=True,
    )
    assert request == expected


def test_deserialising_invalid_low_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_LOW_FULL_RELEASE_JSON)


def test_serialising_invalid_low_allocation_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_LOW_FULL_RELEASE_OBJECT)
    o.subarray_id_low = -1

    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_low_allocation_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_LOW_FULL_RELEASE_JSON)
