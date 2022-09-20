"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest


def test_new_keyvalues_obj():
    """
    Verify that object can be created with new key-value pair
    along with already declared.
    "subbands": [0.55e9,0.95e9,186] //long,long,int
    :param subbands: min freq, max freq, no of channels
    """
    # expand
    request = ReleaseResourcesRequest(
        transaction_id="tma1",
        subarray_id=1,
        dish_allocation=DishAllocation(receptor_ids=["ac", "b", "aab"]),
        sdp_id="sbi-mvp01-20220919-00001",  # new in this schema
        sdp_max_length=125.40,  # new in this schema
        subbands=[0.55e9, 0.95e9, 186],  # arbitary new key-value captured
        release_all=False,
    )

    # check whether object created with correct values
    assert (
        request.sdp_id == "sbi-mvp01-20220919-00001"
        and request.sdp_max_length == 125.40
        # pylint: disable=E1101(no-member)
        and request.subbands == [0.55e9, 0.95e9, 186]
    )

    # contract
    request2 = ReleaseResourcesRequest(
        transaction_id="tma1",
        subarray_id=1,
        dish_allocation=DishAllocation(receptor_ids=["ac", "b", "aab"]),
        sdp_id="sbi-mvp01-20220919-00001",  # new in this schema
    )

    # check whether both objects are identical
    assert (
        request.transaction_id == request2.transaction_id
        and request.subarray_id == request2.subarray_id
        and request.dish == request2.dish
        and request.sdp_id == request2.sdp_id
    )


def test_release_resources_request_eq():
    """
    Verify that two ReleaseResource requests for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=False,
        transaction_id="tma1",
    )

    assert request == ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=dish_allocation, transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=DishAllocation(), transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=2, dish_allocation=dish_allocation, transaction_id="tma1"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=True,
        transaction_id="tma1",
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=dish_allocation, transaction_id="blah"
    )
    assert request != ReleaseResourcesRequest(
        subarray_id=1, dish_allocation=dish_allocation
    )


def test_release_resources_request_eq_for_low():
    """
    Verify that two ReleaseResource requests for the same sub-array
    are considered equal.
    """

    request = ReleaseResourcesRequest(subarray_id=1, release_all=True)

    assert request == ReleaseResourcesRequest(subarray_id=1, release_all=True)
    assert request != ReleaseResourcesRequest(subarray_id=2, release_all=True)


def test_release_resources_request_eq_with_other_objects():
    """
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = ReleaseResourcesRequest(subarray_id=1, dish_allocation=dish_allocation)
    assert request != 1
    assert request != object()


def test_deallocate_resources_must_define_resources_if_not_releasing_all():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(subarray_id=1, release_all=False)


def test_deallocate_resources_if_not_releasing_all_in_low():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(subarray_id=1, release_all=False)


def test_deallocate_resources_enforces_boolean_release_all_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(subarray_id=1, release_all=1)

    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(
            subarray_id=1, release_all=1, dish_allocation=dish_allocation
        )

    # If release_all is not set as boolean for Low
    with pytest.raises(ValueError):
        _ = ReleaseResourcesRequest(subarray_id=1, release_all=1)
