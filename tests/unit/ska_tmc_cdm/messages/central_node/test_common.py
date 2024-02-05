"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from tests.unit.ska_tmc_cdm.builder.central_node.common import DishAllocateBuilder


def test_dish_allocation_eq():
    """
    Verify that two DishAllocations with the same allocated receptors are
    considered equal.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    assert (
        dish_allocation
        == DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    assert (
        dish_allocation
        == DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["b", "ac", "aab"]))
        .build()
    )
    assert (
        dish_allocation
        != DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac"]))
        .build()
    )
    assert (
        dish_allocation
        != DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab", "d"]))
        .build()
    )


def test_dish_allocation_eq_with_other_objects():
    """
    Verify that a DishAllocation is considered unequal to objects of other
    types.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    assert dish_allocation != 1
    assert dish_allocation != object()
