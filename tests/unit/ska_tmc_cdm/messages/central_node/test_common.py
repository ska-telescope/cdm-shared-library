"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from tests.unit.ska_tmc_cdm.builder.central_node.common import DishAllocateBuilder


def dish_allocation_builder(receptor_ids=None):
    """This dish allocation configuration builder is a test data builder for CDM dish allocation configuration"""
    return DishAllocateBuilder().set_receptor_ids(receptor_ids=receptor_ids).build()


def test_dish_allocation_eq():
    """
    Verify that two DishAllocations with the same allocated receptors are
    considered equal.
    """
    dish_allocation = dish_allocation_builder(
        receptor_ids=frozenset(["ac", "b", "aab"])
    )
    assert dish_allocation == dish_allocation_builder(
        receptor_ids=frozenset(["ac", "b", "aab"])
    )
    assert dish_allocation == dish_allocation_builder(
        receptor_ids=frozenset(["b", "ac", "aab"])
    )
    assert dish_allocation != dish_allocation_builder(receptor_ids=frozenset(["ac"]))
    assert dish_allocation != dish_allocation_builder(
        receptor_ids=frozenset(["ac", "b", "aab", "d"])
    )


def test_dish_allocation_eq_with_other_objects():
    """
    Verify that a DishAllocation is considered unequal to objects of other
    types.
    """
    dish_allocation = dish_allocation_builder(
        receptor_ids=frozenset(["ac", "b", "aab"])
    )
    assert dish_allocation != 1
    assert dish_allocation != object()
