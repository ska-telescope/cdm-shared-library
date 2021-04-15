
from ska.cdm.messages.subarray_node.assigned_resources import MCCSAllocation
from ska.cdm.messages.subarray_node.assigned_resources import AssignedResources
from ska.cdm.schemas.subarray_node.assigned_resources import AssignedResourcesSchema
from ska.cdm.schemas.subarray_node.assigned_resources import MCCSAllocationSchema
from ska.cdm.utils import json_is_equal


VALID_MCCS_ALLOCATION_REQUEST = """
{
    "subarray_beam_ids": [ 1, 2, 3, 4 ],
    "station_ids": [ [  1,  2, 3, 4, 5 ] ],
    "channel_blocks": [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
}
"""

VALID_ASSIGNED_RESOURCES = """
{
  "interface": "https://schema.skatelescope.org/ska-low-tmc-assignedresources/1.0",
  "mccs": {
    "subarray_beam_ids": [ 1, 2, 3, 4 ],
    "station_ids": [ [  1,  2, 3, 4, 5 ] ],
    "channel_blocks": [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
  }
}
"""


def test_marshal_mccs_allocation_resources():
    """
    Verify that MCCSAllocation is marshalled to JSON correctly.
    """
    request = MCCSAllocation(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    json_str = MCCSAllocationSchema().dumps(request)
    assert json_is_equal(json_str, VALID_MCCS_ALLOCATION_REQUEST)


def test_unmarshall_mccs_allocation_resources():
    """
    Verify that JSON can be unmarshalled back to an MCCSAllocation
    object.
    """
    expected = MCCSAllocation(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    request = MCCSAllocationSchema().loads(VALID_MCCS_ALLOCATION_REQUEST)
    assert request == expected


def test_marshall_assigned_resources():
    """
    Verify that AssignedResources is marshalled to JSON correctly.
    """
    request = AssignedResources(MCCSAllocation(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ))
    json_str = AssignedResourcesSchema().dumps(request)
    assert json_is_equal(json_str, VALID_ASSIGNED_RESOURCES)


def test_unmarshall_assigned_resources():
    """
    Verify that JSON can be unmarshalled back to an AssignedResources
    object.
    """
    mccs_allocation = MCCSAllocation(
        [1, 2, 3, 4], [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    expected = AssignedResources(mccs_allocation)
    request = AssignedResourcesSchema().loads(VALID_ASSIGNED_RESOURCES)
    assert request == expected
