"""
Unit tests for ska.cdm.schemas.mccssubarray.assigned_resources module.
"""

import pytest

from ska.cdm.messages.mccssubarray.assigned_resources import AssignedResources
from ska.cdm.schemas.mccssubarray.assigned_resources import AssignedResourcesSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignedresources/1.0",
  "subarray_beam_ids": [1],
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
