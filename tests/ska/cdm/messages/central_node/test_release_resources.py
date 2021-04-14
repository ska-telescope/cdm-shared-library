"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest

from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest


def test_release_resources_request_eq():
    """
    Verify that two ReleaseResource requests for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(
        1, dish_allocation=dish_allocation, release_all_mid=False
    )

    assert request == ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request != ReleaseResourcesRequest(1, dish_allocation=DishAllocation())
    assert request != ReleaseResourcesRequest(2, dish_allocation=dish_allocation)
    assert request != ReleaseResourcesRequest(
        1, dish_allocation=dish_allocation, release_all_mid=True
    )


def test_release_resources_request_eq_with_other_objects():
    """
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(1, dish_allocation=dish_allocation)
    assert request != 1
    assert request != object()


def test_deallocate_resources_must_define_resources_if_not_releasing_all():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(1, release_all_mid=False)


def test_deallocate_resources_enforces_boolean_release_all_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(1, release_all_mid=1)

    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(1, release_all_mid=1,
                                    dish_allocation=dish_allocation)
