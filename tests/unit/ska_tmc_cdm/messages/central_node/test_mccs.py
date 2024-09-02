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
            MCCSAllocateBuilder(),
            MCCSAllocateBuilder(),
            True,
        ),
        # not equal
        (
            MCCSAllocateBuilder(station_ids=[[1, 2]]),
            MCCSAllocateBuilder(
                station_ids=[[1, 2, 3]]
            ),  # different station id
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
