"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.central_node.common import DishAllocateBuilder
from tests.unit.ska_tmc_cdm.builder.central_node.release_resources import (
    ReleaseResourcesRequestBuilder,
)

interface = "https://schema.skao.int/ska-tmc-releaseresources/2.1"


def test_release_resources_request_has_interface_set_on_creation():
    request = (
        ReleaseResourcesRequestBuilder()
        .set_interface(interface=interface)
        .set_release_all(release_all=True)
        .build()
    )
    assert request.interface is not None


@pytest.mark.parametrize(
    "subarray_id, dish_allocation, release_all, transaction_id, expected",
    [
        (
            1,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            True,
            "txn-mvp01-20200325-00001",
            True,
        ),
        (
            2,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            True,
            "txn-mvp01-20200325-00001",
            False,
        ),
        (
            1,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            False,
            "tma1",
            False,
        ),
        (
            2,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            False,
            "tma1",
            False,
        ),
        (
            1,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            True,
            "tma1",
            False,
        ),
        (
            1,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
            False,
            "blah",
            False,
        ),
        (
            1,
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build(),
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
    request = (
        ReleaseResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation)
        .set_release_all(release_all)
        .set_transaction_id("txn-mvp01-20200325-00001")
        .build()
    )

    assert (
        request
        == ReleaseResourcesRequestBuilder()
        .set_subarray_id(subarray_id)
        .set_dish_allocation(dish_allocation)
        .set_release_all(release_all)
        .set_transaction_id(transaction_id)
        .build()
    ) == expected


def test_release_resources_request_eq_with_other_objects():
    """
    Verify that a ReleaseResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    request = (
        ReleaseResourcesRequestBuilder()
        .set_subarray_id(1)
        .set_release_all(True)
        .set_dish_allocation(dish_allocation)
        .build()
    )
    assert request != 1
    assert request != object()


def test_deallocate_resources_must_define_resources_if_not_releasing_all():
    """
    Verify that resource argument(s) must be set if the command is not a
    command to release all sub-array resources.
    """
    with pytest.raises(ValueError):
        _ = (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_release_all(False)
            .build()
        )


def test_deallocate_resources_enforces_boolean_release_all_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    with pytest.raises(ValueError):
        _ = (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_release_all(1)
            .build()
        )

    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["0001", "0002"]))
        .build()
    )
    with pytest.raises(ValueError):
        _ = (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_release_all(1)
            .set_dish_allocation(dish_allocation)
            .build()
        )

    with pytest.raises(ValueError):
        _ = (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_release_all(1)
            .build()
        )
