"""
Unit tests for the CentralNode.mccs allocate module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.mccs import (
    MCCSAllocateBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # equal
        (
            MCCSAllocateBuilder()
            .set_subarray_beam_ids([1])
            .set_station_ids([[1, 2]])
            .set_channel_blocks([3])
            .build(),
            MCCSAllocateBuilder()
            .set_subarray_beam_ids([1])
            .set_station_ids([[1, 2]])
            .set_channel_blocks([3])
            .build(),
            True,
        ),
        # not equal
        (
            MCCSAllocateBuilder()
            .set_subarray_beam_ids([1])
            .set_station_ids([[1, 2]])
            .set_channel_blocks([3])
            .build(),
            MCCSAllocateBuilder()
            .set_subarray_beam_ids([2])
            .set_station_ids([[1, 2, 3]])  # different station id
            .set_channel_blocks([4])
            .build(),
            False,
        ),
    ],
)
def test_mccs_allocate_eq(object1, object2, is_equal):
    """
    Verify  object  of MCCS Allocate with same properties are equal
    And with different properties are different and also check equality with different object
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()
