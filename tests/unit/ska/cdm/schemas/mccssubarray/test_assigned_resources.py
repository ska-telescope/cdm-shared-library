"""
Unit tests for ska.cdm.schemas.mccssubarray.assigned_resources module.
"""

import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.mccssubarray.assigned_resources import AssignedResources
from ska.cdm.schemas.mccssubarray.assigned_resources import AssignedResourcesSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [-1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

VALID_EMPTY_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [],
  "station_ids": [],
  "channel_blocks": []
}
"""

VALID_OBJECT = AssignedResources(
    interface="https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
    subarray_beam_ids=[1],
    station_ids=[[1, 2]],
    channel_blocks=[3]
)

VALID_EMPTY_OBJECT = AssignedResources(
    interface="https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
    subarray_beam_ids=[],
    station_ids=[],
    channel_blocks=[]
)


@pytest.mark.parametrize('instance,expected', [
    (VALID_OBJECT, VALID_JSON),
    (VALID_EMPTY_OBJECT, VALID_EMPTY_JSON)
])
def test_marshal_assigned_resources(instance, expected):
    """
    Verify that AssignedResources is marshalled to JSON correctly.
    """
    json_str = AssignedResourcesSchema().dumps(instance)
    assert json_is_equal(json_str, expected)


@pytest.mark.parametrize('expected,json_str', [
    (VALID_OBJECT, VALID_JSON),
    (VALID_EMPTY_OBJECT, VALID_EMPTY_JSON)
])
def test_unmarshal_assigned_resources(expected, json_str):
    """
    Verify that JSON can be unmarshalled back to an AssignedResources object.
    """
    unmarshalled = AssignedResourcesSchema().loads(json_str)
    assert unmarshalled == expected


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = AssignedResourcesSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_OBJECT)
    o.subarray_beam_ids = [-1]

    schema = AssignedResourcesSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_object_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = AssignedResourcesSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_OBJECT)
