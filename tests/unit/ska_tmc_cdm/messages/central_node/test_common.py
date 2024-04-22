"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocateBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # equal
        (
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab"]))
            .build(),
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab"]))
            .build(),
            True,
        ),
        # equal but different order
        (
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab"]))
            .build(),
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["b", "ac", "aab"]))
            .build(),
            True,
        ),
        # one receptor list is a subset of the other
        (
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab"]))
            .build(),
            DishAllocateBuilder().set_receptor_ids(frozenset(["ac"])).build(),
            False,
        ),
        # one list has an additional receptor
        (
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab"]))
            .build(),
            DishAllocateBuilder()
            .set_receptor_ids(frozenset(["ac", "b", "aab", "d"]))
            .build(),
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
