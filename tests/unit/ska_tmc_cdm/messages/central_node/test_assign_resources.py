"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
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

)
from tests.unit.ska_tmc_cdm.builder.central_node.common import (
    DishAllocationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.mccs import (
    MCCSAllocateBuilder,
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


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that subarray_id is required.
    """
    mccs = MCCSAllocateBuilder()
    dish_allocation = DishAllocationBuilder()

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(subarray_id=None, dish=None, mccs=mccs)

    with pytest.raises(ValueError):
        AssignResourcesRequestBuilder(
            subarray_id=None, dish=dish_allocation, mccs=None
        )


def test_mid_assign_resource_request_using_from_dish():
    """
    Verify that  Mid AssignResource request object created using from_dish is equal.
    """
    expected = AssignResourcesRequestBuilder(
        dish=DishAllocationBuilder(),
        mccs=None,
    )

    request = AssignResourcesRequest.from_dish(
        subarray_id=expected.subarray_id,
        dish_allocation=expected.dish,
        sdp_config=expected.sdp_config,
        interface=expected.interface,
        transaction_id=expected.transaction_id,
    )

    assert request == expected


def test_low_assign_resource_request_using_from_mccs():
    """
    Verify that  Low AssignResource request object created using from_mccs is equal.
    """
    expected = AssignResourcesRequestBuilder(
        dish=None,
        mccs=MCCSAllocateBuilder(),
    )

    request = AssignResourcesRequest.from_mccs(
        subarray_id=expected.subarray_id,
        mccs=expected.mccs,
        sdp_config=expected.sdp_config,
        interface=expected.interface,
        transaction_id=expected.transaction_id,
    )

    assert request == expected
