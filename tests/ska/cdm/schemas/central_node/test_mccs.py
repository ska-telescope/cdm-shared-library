"""
Unit tests for ska.cdm.schemas module.
"""

from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska.cdm.utils import json_is_equal


VALID_MCCS_ALLOCATE_REQUEST = """
{
    "subarray_id": 1,
    "station_ids": [1, 2, 3, 4],
    "station_beam_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
"""


def test_marshal_mccs_allocate_resources():
    """
    Verify that MCCSAllocate is marshalled to JSON correctly.
    """
    request = MCCSAllocate(1, [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    json_str = MCCSAllocateSchema().dumps(request)
    assert json_is_equal(json_str, VALID_MCCS_ALLOCATE_REQUEST)


def test_unmarshall_mccs_allocate_resources():
    """
    Verify that JSON can be unmarshalled back to an MCCSAllocate
    object.
    """
    expected = MCCSAllocate(1, [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    request = MCCSAllocateSchema().loads(VALID_MCCS_ALLOCATE_REQUEST)
    assert request == expected
