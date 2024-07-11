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
    DishAllocateBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.mccs import (
    ApertureConfigurationBuilder,
    MCCSAllocateBuilder,
    SubArrayBeamsConfigurationBuilder,
)


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
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
                .build()
            )
            .build(),
            MID_SCHEMA,
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_interface(interface="foo")
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
                .build()
            )
            .build(),
            "foo",
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .set_interface(
                    "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
                )
                .set_subarray_beams(
                    [
                        SubArrayBeamsConfigurationBuilder()
                        .set_subarray_beam_id(1)
                        .set_apertures(
                            [
                                ApertureConfigurationBuilder()
                                .set_aperture_id("AP001.01")
                                .set_station_id(1)
                                .build()
                            ]
                        )
                        .set_number_of_channels(8)
                        .build()
                    ]
                )
                .build()
            )
            .build(),
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
    mccs_allocate = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
        .set_interface(
            "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
        )
        .set_subarray_beams(
            [
                SubArrayBeamsConfigurationBuilder()
                .set_subarray_beam_id(1)
                .set_apertures(
                    [
                        ApertureConfigurationBuilder()
                        .set_aperture_id("AP001.01")
                        .set_station_id(1)
                        .build()
                    ]
                )
                .set_number_of_channels(8)
                .build()
            ]
        )
        .build()
    )

    with pytest.raises(ValueError):
        dish_allocation = (
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build()
        )
        AssignResourcesRequestBuilder().set_dish_allocation(
            dish_allocation=dish_allocation
        ).set_mccs(mccs=mccs_allocate).build()


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
        .set_interface(
            "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
        )
        .set_subarray_beams(
            [
                SubArrayBeamsConfigurationBuilder()
                .set_subarray_beam_id(1)
                .set_apertures(
                    [
                        ApertureConfigurationBuilder()
                        .set_aperture_id("AP001.01")
                        .set_station_id(1)
                        .build()
                    ]
                )
                .set_number_of_channels(8)
                .build()
            ]
        )
        .build()
    )
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", " b", "aab"]))
        .build()
    )

    with pytest.raises(ValueError):
        _ = AssignResourcesRequestBuilder().set_mccs(mccs=mccs).build()

    with pytest.raises(ValueError):
        _ = (
            AssignResourcesRequestBuilder()
            .set_dish_allocation(dish_allocation=dish_allocation)
            .build()
        )


def test_low_assign_resources_request(
    sdp_allocate,
):
    """
    Verify creation of Low AssignResources request objects
    with both sdp block and check equality
    """

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_mccs(
            MCCSAllocateBuilder()
            .set_subarray_beam_ids(subarray_beam_ids=[1])
            .set_station_ids(station_ids=[[1, 2]])
            .set_channel_blocks(channel_blocks=[3])
            .set_interface(
                "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
            )
            .set_subarray_beams(
                [
                    SubArrayBeamsConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_apertures(
                        [
                            ApertureConfigurationBuilder()
                            .set_aperture_id("AP001.01")
                            .set_station_id(1)
                            .build()
                        ]
                    )
                    .set_number_of_channels(8)
                    .build()
                ]
            )
            .build()
        )
        .set_interface(MID_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_mccs(
            MCCSAllocateBuilder()
            .set_subarray_beam_ids(subarray_beam_ids=[1])
            .set_station_ids(station_ids=[[1, 2]])
            .set_channel_blocks(channel_blocks=[3])
            .set_interface(
                "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
            )
            .set_subarray_beams(
                [
                    SubArrayBeamsConfigurationBuilder()
                    .set_subarray_beam_id(1)
                    .set_apertures(
                        [
                            ApertureConfigurationBuilder()
                            .set_aperture_id("AP001.01")
                            .set_station_id(1)
                            .build()
                        ]
                    )
                    .set_number_of_channels(8)
                    .build()
                ]
            )
            .build()
        )
        .set_interface(MID_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
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

    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_interface(MID_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_interface(MID_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_mid_assign_resource_request_using_from_dish(sdp_allocate):
    """
    Verify that  Mid AssignResource request object created using from_dish is equal.
    """

    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
        .build()
    )
    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_interface(MID_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    request2 = AssignResourcesRequestBuilder.from_dish(
        subarray_id=1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_allocate,
        interface=MID_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    ).build()

    assert request1 == request2


def test_low_assign_resource_request_using_from_mccs(sdp_allocate):
    """
    Verify that  Low AssignResource request object created using from_mccs is equal.
    """
    mccs_allocate = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1])
        .set_station_ids(station_ids=[[1, 2]])
        .set_channel_blocks(channel_blocks=[3])
        .set_interface(
            "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
        )
        .set_subarray_beams(
            [
                SubArrayBeamsConfigurationBuilder()
                .set_subarray_beam_id(1)
                .set_apertures(
                    [
                        ApertureConfigurationBuilder()
                        .set_aperture_id("AP001.01")
                        .set_station_id(1)
                        .build()
                    ]
                )
                .set_number_of_channels(8)
                .build()
            ]
        )
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp_allocate)
        .set_mccs(mccs=mccs_allocate)
        .set_interface(interface=LOW_SCHEMA)
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    request2 = AssignResourcesRequestBuilder.from_mccs(
        subarray_id=1,
        sdp_config=sdp_allocate,
        mccs=mccs_allocate,
        interface=LOW_SCHEMA,
        transaction_id="txn-mvp01-20200325-00001",
    ).build()

    assert request1 == request2


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        # Case where both responses have the same dish allocation
        (
            AssignResourcesResponseBuilder()
            .set_dish(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            AssignResourcesResponseBuilder()
            .set_dish(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            True,
        ),
        # Case where responses have different dish allocations
        (
            AssignResourcesResponseBuilder()
            .set_dish(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            AssignResourcesResponseBuilder()
            .set_dish(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(frozenset(["b", "aab"]))
                .build()
            )
            .build(),
            False,
        ),
        (  # MCCS Equality
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .set_interface(
                    "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
                )
                .set_subarray_beams(
                    [
                        SubArrayBeamsConfigurationBuilder()
                        .set_subarray_beam_id(1)
                        .set_apertures(
                            [
                                ApertureConfigurationBuilder()
                                .set_aperture_id("AP001.01")
                                .set_station_id(1)
                                .build()
                            ]
                        )
                        .set_number_of_channels(8)
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .set_interface(
                    "https://schema.skao.int/ska-low-mccs-controller-allocate/3.0"
                )
                .set_subarray_beams(
                    [
                        SubArrayBeamsConfigurationBuilder()
                        .set_subarray_beam_id(1)
                        .set_apertures(
                            [
                                ApertureConfigurationBuilder()
                                .set_aperture_id("AP001.01")
                                .set_station_id(1)
                                .build()
                            ]
                        )
                        .set_number_of_channels(8)
                        .build()
                    ]
                )
                .build()
            )
            .build(),
            True,
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .build(),
            )
            .build(),
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=2)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .build(),
            )
            .build(),
            False,
        ),
        (  # Dish Equality
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            True,
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
                .build()
            )
            .build(),
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["b", "aab"]))
                .build()
            )
            .build(),
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
