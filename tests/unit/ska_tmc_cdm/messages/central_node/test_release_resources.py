"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.release_resources import (
    ReleaseResourcesRequestBuilder,
)
from tests.unit.ska_tmc_cdm.messages.central_node.test_common import (
    dish_allocation_builder,
)


def release_resources_request_builder(
    transaction_id=None,
    subarray_id=None,
    release_all=True,
    dish_allocation=None,
):
    """ReleaseResourcesRequestBuilder is a test data builder for CDM ReleaseResourcesRequest objects."""
    return (
        ReleaseResourcesRequestBuilder()
        .set_transaction_id(transaction_id=transaction_id)
        .set_subarray_id(subarray_id=subarray_id)
        .set_release_all(release_all=release_all)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .build()
    )


interface = "https://schema.skao.int/ska-tmc-releaseresources/2.1"


def test_release_resources_request_has_interface_set_on_creation():
    request = ReleaseResourcesRequestBuilder().set_interface(interface=interface)
    assert request.interface is not None


@pytest.mark.parametrize(
    "subarray_id, dish_allocation, release_all, transaction_id, expected",
    [
        (
            1,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            True,
            "txn-mvp01-20200325-00001",
            True,
        ),
        (
            2,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            True,
            "txn-mvp01-20200325-00001",
            False,
        ),
        (
            1,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            False,
            "tma1",
            False,
        ),
        (
            2,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            False,
            "tma1",
            False,
        ),
        (
            1,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            True,
            "tma1",
            False,
        ),
        (
            1,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            False,
            "blah",
            False,
        ),
        (
            1,
            dish_allocation_builder(receptor_ids=frozenset(["ac", "b", "aab"])),
            False,
            None,
            False,
        ),
    ],
)
def test_release_resources_request_eq(
    subarray_id, dish_allocation, release_all, transaction_id, expected
):
    """
    Verify that two ReleaseResource requests for the same sub-array and
    dish allocation are considered equal.
    """
    request = release_resources_request_builder(
        subarray_id=1,
        dish_allocation=dish_allocation,
        release_all=release_all,
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert (
        request
        == release_resources_request_builder(
            subarray_id=subarray_id,
            dish_allocation=dish_allocation,
            transaction_id=transaction_id,
        )
    ) == expected


def test_release_resources_request_eq_with_other_objects():
    """
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = dish_allocation_builder(
        receptor_ids=frozenset(["ac", "b", "aab"])
    )
    request = release_resources_request_builder(
        subarray_id=1, dish_allocation=dish_allocation
    )
    assert request != 1
    assert request != object()


def test_deallocate_resources_must_define_resources_if_not_releasing_all():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = release_resources_request_builder(subarray_id=1, release_all=False)


def test_deallocate_resources_enforces_boolean_release_all_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = release_resources_request_builder(subarray_id=1, release_all=1)

    dish_allocation = dish_allocation_builder(receptor_ids=frozenset(["0001", "0002"]))
    with pytest.raises(ValueError):
        _ = release_resources_request_builder(
            subarray_id=1, release_all=1, dish_allocation=dish_allocation
        )

    # If release_all is not set as boolean for Low
    with pytest.raises(ValueError):
        _ = release_resources_request_builder(subarray_id=1, release_all=1)
