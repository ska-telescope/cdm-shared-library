"""
Unit tests for ska.cdm.schemas module.
"""
import itertools

from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska.cdm.utils import json_is_equal

VALID_MCCS_ALLOCATE_REQUEST = """
{
    "station_ids": [[1, 2]],
    "channel_blocks": [1, 2, 3, 4, 5],
    "station_beam_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
"""


def test_marshal_mccs_allocate_resources():
    """
    Verify that MCCSAllocate is marshalled to JSON correctly.
    """
    request = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])), [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    json_str = MCCSAllocateSchema().dumps(request)
    assert json_is_equal(json_str, VALID_MCCS_ALLOCATE_REQUEST)


def test_unmarshall_mccs_allocate_resources():
    """
    Verify that JSON can be unmarshalled back to an MCCSAllocate
    object.
    """
    expected = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])), [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    request = MCCSAllocateSchema().loads(VALID_MCCS_ALLOCATE_REQUEST)
    assert request == expected
