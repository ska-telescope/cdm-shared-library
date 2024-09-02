"""
Unit tests for the CentralNode.ReleaseResources request/response mapper
module.
"""
import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.central_node.release_resources import SCHEMA
from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.release_resources import (
    ReleaseResourcesRequestBuilder,
)


@pytest.mark.parametrize(
    ("subarray_id", "okay"),
    zip(range(-5, 21), ([False] * 6 + [True] * 16 + [False] * 4)),
)
def test_validation_applies_to_subarray_id(subarray_id: int, okay: bool):
    "subarray_id must be from 1...16, inclusive"
    builder = (
        ReleaseResourcesRequestBuilder()
        .set_release_all(release_all=True)
        .set_subarray_id(subarray_id)
    )
    if not okay:
        with pytest.raises(ValidationError):
            builder.build()
    else:
        builder.build()


def test_release_resources_request_has_interface_set_on_creation():
    request = (
        ReleaseResourcesRequestBuilder()
        .set_interface(interface=SCHEMA)
        .set_release_all(release_all=True)
        .build()
    )
    assert request.interface is not None


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # Case where both objects are the same
        (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_dish_allocation(DishAllocationBuilder())
            .set_release_all(True)
            .set_transaction_id("txn-mvp01-20200325-00001")
            .build(),
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_dish_allocation(DishAllocationBuilder())
            .set_release_all(True)
            .set_transaction_id("txn-mvp01-20200325-00001")
            .build(),
            True,
        ),
        # Case where objects differ by subarray_id
        (
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(1)
            .set_dish_allocation(DishAllocationBuilder())
            .set_release_all(True)
            .set_transaction_id("txn-mvp01-20200325-00001")
            .build(),
            ReleaseResourcesRequestBuilder()
            .set_subarray_id(2)
            .set_dish_allocation(DishAllocationBuilder())
            .set_release_all(True)
            .set_transaction_id("txn-mvp01-20200325-00001")
            .build(),
            False,
        ),
    ],
)
def test_release_resources_request_eq_check(object1, object2, is_equal):
    """
    Verify that ReleaseResourcesRequest objects are equal or not equal based on their attributes.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


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

    dish_allocation = DishAllocationBuilder()

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
