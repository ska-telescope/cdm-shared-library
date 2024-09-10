"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # equal
        (
            DishAllocationBuilder(),
            DishAllocationBuilder(),
            True,
        ),
        # equal but different order
        (
            DishAllocationBuilder(receptor_ids=["ac", "b", "aab"]),
            DishAllocationBuilder(receptor_ids=["b", "ac", "aab"]),
            True,
        ),
        # one receptor list is a subset of the other
        (
            DishAllocationBuilder(receptor_ids=["ac", "b", "aab"]),
            DishAllocationBuilder(receptor_ids=["ac"]),
            False,
        ),
        # one list has an additional receptor
        (
            DishAllocationBuilder(receptor_ids=["ac", "b", "aab"]),
            DishAllocationBuilder(receptor_ids=["ac", "b", "aab", "d"]),
            False,
        ),
    ],
)
def test_dish_allocation_equality_check(object1, object2, is_equal):
    """
    Verify that DishAllocation objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object2 != object()
