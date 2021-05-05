import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.subarray_node.assigned_resources import AssignedResources
from ska.cdm.messages.subarray_node.assigned_resources import MCCSAllocation
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.schemas.subarray_node.assigned_resources import AssignedResourcesSchema
from ska.cdm.schemas.subarray_node.assigned_resources import MCCSAllocationSchema
from ska.cdm.utils import json_is_equal

VALID_MCCSALLOCATION_JSON = """
{
    "subarray_beam_ids": [1],
    "station_ids": [ [1,2] ],
    "channel_blocks": [3]
}
"""

VALID_MCCSALLOCATION_OBJECT = MCCSAllocation(
    subarray_beam_ids=[1],
    station_ids=[[1, 2]],
    channel_blocks=[3]
)

VALID_ASSIGNEDRESOURCES_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-assignedresources/1.0",
  "mccs": """ + VALID_MCCSALLOCATION_JSON + """
}
"""

VALID_ASSIGNEDRESOURCES_OBJECT = AssignedResources(
    interface="https://schema.skatelescope.org/ska-low-tmc-assignedresources/1.0",
    mccs=VALID_MCCSALLOCATION_OBJECT
)

INVALID_ASSIGNEDRESOURCES_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-assignedresources/1.0",
  "mccs": {
    "subarray_beam_ids": [-1],
    "station_ids": [ [1,2] ],
    "channel_blocks": [3]
  }
}
"""


@pytest.mark.parametrize('schema_cls, instance, expected', [
    (MCCSAllocationSchema, VALID_MCCSALLOCATION_OBJECT, VALID_MCCSALLOCATION_JSON),
    (AssignedResourcesSchema, VALID_ASSIGNEDRESOURCES_OBJECT, VALID_ASSIGNEDRESOURCES_JSON)
])
def test_marshal(schema_cls, instance, expected):
    """
    Verify that objects are marshaled to JSON correctly.
    """
    schema = schema_cls()
    json_str = schema.dumps(instance)
    assert json_is_equal(json_str, expected)


@pytest.mark.parametrize('schema_cls, json_str, expected', [
    (MCCSAllocationSchema, VALID_MCCSALLOCATION_JSON, VALID_MCCSALLOCATION_OBJECT),
    (AssignedResourcesSchema, VALID_ASSIGNEDRESOURCES_JSON, VALID_ASSIGNEDRESOURCES_OBJECT)
])
def test_unmarshal(schema_cls, json_str, expected):
    """
    Verify that JSON can be unmarshaled back to objects.
    """
    schema = schema_cls()
    unmarshaled = schema.loads(json_str)
    assert unmarshaled == expected


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = AssignedResourcesSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_ASSIGNEDRESOURCES_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.
    """
    o = copy.deepcopy(VALID_ASSIGNEDRESOURCES_OBJECT)
    o.mccs.subarray_beam_ids = [-1]

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

    _ = schema.dumps(VALID_ASSIGNEDRESOURCES_OBJECT)
