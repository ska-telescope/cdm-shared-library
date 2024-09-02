"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import itertools
from functools import partial

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.central_node.assign_resources import (
    LOW_SCHEMA,
    MID_SCHEMA,
    AssignResourcesRequest,
)
from tests.unit.ska_tmc_cdm.builder.central_node.assign_resources import (
    AssignResourcesRequestBuilder,
    AssignResourcesResponseBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.mccs import (
    MCCSAllocateBuilder,
    SubArrayBeamsConfigurationBuilder,
)

interface = "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"


@pytest.mark.parametrize(
    ("subarray_id", "okay"),
    zip(range(-5, 21), ([False] * 6 + [True] * 16 + [False] * 4)),
)
def test_validation_applies_to_subarray_id(subarray_id: int, okay: bool):
    "subarray_id must be from 1...16, inclusive"
    build = partial(
        AssignResourcesRequest, subarray_id=subarray_id, interface="DUMMY"
    )
    if not okay:
        with pytest.raises(ValidationError):
            build()
    else:
        build()


@pytest.mark.parametrize(
    "assign_request, expected_interface",
    (
        (
            AssignResourcesRequestBuilder(),
            MID_SCHEMA,
        ),
        (
            AssignResourcesRequestBuilder(interface="foo"),
            "foo",
        ),
        (
            AssignResourcesRequestBuilder(
                dish=None, mccs=MCCSAllocateBuilder()
            ),
            LOW_SCHEMA,
        ),
        (
            AssignResourcesRequestBuilder(
                dish=None,
                mccs=MCCSAllocateBuilder(
                    interface=interface,
                    subarray_beams=[SubArrayBeamsConfigurationBuilder()],
                ),
            ),
            LOW_SCHEMA,
        ),
    ),
)
def test_assign_resources_request_has_interface_set_on_creation(
    assign_request, expected_interface
):
    """
    Verify that the interface is set correctly if not provided
    """
    assert assign_request.interface == expected_interface


def test_assign_resources_request_dish_and_mccs_fail():
    """
    Verify that mccs & dish cannot be allocated together
    """
    dish_allocation = DishAllocationBuilder()
    mccs_allocate = MCCSAllocateBuilder()

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(
            dish_allocation=dish_allocation, mccs=mccs_allocate
        )


def test_assign_resources_request_dish_and_mccs_fail_for_4_0_resource():
    """
    Verify that mccs & dish cannot be allocated together
    """
    mccs_allocate = MCCSAllocateBuilder(
        interface=interface,
        subarray_beams=[SubArrayBeamsConfigurationBuilder()],
    )
    dish_allocation = DishAllocationBuilder()

    with pytest.raises(ValueError):

        AssignResourcesRequestBuilder(
            dish_allocation=dish_allocation, mccs=mccs_allocate
        )


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = MCCSAllocateBuilder()
    dish_allocation = DishAllocationBuilder()

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(subarray_id=None, dish=None, mccs=mccs)

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(
            subarray_id=None, dish=dish_allocation, mccs=None
        )


def test_assign_resources_if_no_subarray_id_argument_for_4_0_interface():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = MCCSAllocateBuilder(
        subarray_beams=[SubArrayBeamsConfigurationBuilder()],
    )
    dish_allocation = DishAllocationBuilder(
        receptor_ids=frozenset(["ac", " b", "aab"])
    )

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(subarray_id=None, dish=None, mccs=mccs)

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(
            subarray_id=None, dish=dish_allocation, mccs=None
        )


def test_low_assign_resources_request(
    sdp_allocate,
):
    """
    Verify creation of Low AssignResources request objects
    with both sdp block and check equality
    """

    request1 = AssignResourcesRequestBuilder(
        sdp_config=sdp_allocate,
        mccs=MCCSAllocateBuilder(),
        interface=LOW_SCHEMA,
    )
    request2 = AssignResourcesRequestBuilder(
        sdp_config=sdp_allocate,
        mccs=MCCSAllocateBuilder(),
        interface=LOW_SCHEMA,
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_low_assign_resources_request_for_4_0_interface(
    sdp_allocate,
):
    """
    Verify creation of Low AssignResources request objects
    with both sdp block and check equality
    """

    request1 = AssignResourcesRequestBuilder(
        interface=LOW_SCHEMA,
        dish=None,
        sdp_config=sdp_allocate,
        mccs=MCCSAllocateBuilder(
            subarray_beams=[SubArrayBeamsConfigurationBuilder()],
        ),
    )
    request2 = AssignResourcesRequestBuilder(
        interface=LOW_SCHEMA,
        dish=None,
        sdp_config=sdp_allocate,
        mccs=MCCSAllocateBuilder(
            subarray_beams=[SubArrayBeamsConfigurationBuilder()],
        ),
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_mid_assign_resources_request(
    sdp_allocate,
):
    """
    Verify creation of Mid AssignResources request objects
    with sdp block and equality check
    """
    request1 = AssignResourcesRequestBuilder(
        subarray_id=1,
        dish_allocation=DishAllocationBuilder(),
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequestBuilder(
        subarray_id=1,
        dish_allocation=DishAllocationBuilder(),
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_mid_assign_resource_request_using_from_dish(sdp_allocate):
    """
    Verify that  Mid AssignResource request object created using from_dish is equal.
    """
    request1 = AssignResourcesRequestBuilder(
        subarray_id=1,
        dish_allocation=DishAllocationBuilder(),
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequest.from_dish(
        subarray_id=request1.subarray_id,
        dish_allocation=request1.dish_allocation,
        sdp_config=request1.sdp_config,
        interface=request1.interface,
        transaction_id=request1.transaction_id,
    )

    assert request1 == request2


def test_low_assign_resource_request_using_from_mccs(sdp_allocate):
    """
    Verify that  Low AssignResource request object created using from_mccs is equal.
    """
    mccs_allocate = MCCSAllocateBuilder()

    request1 = AssignResourcesRequestBuilder(
        subarray_id=1,
        dish=None,
        mccs=mccs_allocate,
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequest.from_mccs(
        subarray_id=request1.subarray_id,
        mccs=request1.mccs,
        sdp_config=request1.sdp_config,
        interface=request1.interface,
        transaction_id=request1.transaction_id,
    )

    assert request1 == request2


def test_low_assign_resource_request_using_from_mccs_for_4_0_interface(
    sdp_allocate,
):
    """
    Verify that  Low AssignResource request object created using from_mccs is equal.
    """
    mccs_allocate = MCCSAllocateBuilder(
        subarray_beams=[SubArrayBeamsConfigurationBuilder()],
    )

    request1 = AssignResourcesRequestBuilder(
        subarray_id=1,
        dish=None,
        mccs=mccs_allocate,
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequest.from_mccs(
        subarray_id=request1.subarray_id,
        mccs=request1.mccs,
        sdp_config=request1.sdp_config,
        interface=request1.interface,
        transaction_id=request1.transaction_id,
    )
    assert request1 == request2


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # Case where both responses have the same dish allocation
        (
            AssignResourcesResponseBuilder(),
            AssignResourcesResponseBuilder(),
            True,
        ),
        # Case where responses have different dish allocations
        (
            AssignResourcesResponseBuilder(
                dish_allocation=DishAllocationBuilder(
                    receptor_ids=frozenset(["ac", "b", "aab"])
                )
            ),
            AssignResourcesResponseBuilder(
                dish_allocation=DishAllocationBuilder(
                    receptor_ids=frozenset(["b", "aab"])
                )
            ),
            False,
        ),
        (  # MCCS Equality
            AssignResourcesRequestBuilder(
                dish=None, mccs=MCCSAllocateBuilder()
            ),
            AssignResourcesRequestBuilder(
                dish=None, mccs=MCCSAllocateBuilder()
            ),
            True,
        ),
        (  # MCCS Equality
            AssignResourcesRequestBuilder(
                dish=None,
                mccs=MCCSAllocateBuilder(
                    subarray_beams=[SubArrayBeamsConfigurationBuilder()],
                ),
            ),
            AssignResourcesRequestBuilder(
                dish=None,
                mccs=MCCSAllocateBuilder(
                    subarray_beams=[SubArrayBeamsConfigurationBuilder()],
                ),
            ),
            True,
        ),
        (
            AssignResourcesRequestBuilder(subarray_id=1),
            AssignResourcesRequestBuilder(subarray_id=2),
            False,
        ),
        (  # Dish Equality
            AssignResourcesRequestBuilder(dish=DishAllocationBuilder()),
            AssignResourcesRequestBuilder(dish=DishAllocationBuilder()),
            True,
        ),
        (
            AssignResourcesRequestBuilder(
                dish=DishAllocationBuilder(
                    receptor_ids=frozenset(["ac", "b", "aab"])
                )
            ),
            AssignResourcesRequestBuilder(
                dish=DishAllocationBuilder(
                    receptor_ids=frozenset(["b", "aab"])
                )
            ),
            False,
        ),
    ],
)
def test_assign_resources_equality_check(object1, object2, is_equal):
    """
    Verify that AssignResourcesResponse objects are equal or not equal based on their dish allocations.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()
