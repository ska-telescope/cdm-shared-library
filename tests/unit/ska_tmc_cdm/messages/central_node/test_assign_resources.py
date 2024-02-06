"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import itertools

import pytest

from ska_tmc_cdm.messages.central_node.assign_resources import LOW_SCHEMA, MID_SCHEMA
from tests.unit.ska_tmc_cdm.builder.central_node.assign_resources import (
    AssignResourcesRequestBuilder,
    AssignResourcesResponseBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.common import DishAllocateBuilder
from tests.unit.ska_tmc_cdm.builder.central_node.mccs import MCCSAllocateBuilder
from tests.unit.ska_tmc_cdm.builder.central_node.sdp import (
    ExecutionBlockConfigurationBuilder,
    SDPConfigurationBuilder,
)


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


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    unequal_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["b", "aab"]))
        .build()
    )

    response = (
        AssignResourcesResponseBuilder()
        .set_dish(dish_allocation=dish_allocation)
        .build()
    )
    assert (
        response
        == AssignResourcesResponseBuilder()
        .set_dish(dish_allocation=dish_allocation)
        .build()
    )
    assert (
        response
        != AssignResourcesResponseBuilder()
        .set_dish(dish_allocation=unequal_allocation)
        .build()
    )
    assert response != object()
    assert response != 1


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
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


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # MCCS
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
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
        (  # Dish
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
def test_assign_resource_eq_check(object1, object2, is_equal):
    """
    Verify  object  of Assign Resource with same Dish and MCCS properties are equal
    And with different properties are different and also check equality with different object
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


def test_low_assign_resources_request(
    eb_scan_type,
    scan_type,
    processing_block,
    beams,
    channels,
    polarisatrion_config,
    field_config,
):
    """
    Verify creation of Low AssignResources request objects
    with both sdp block and check equality
    """

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisatrion_config])
        .set_fields(fields=[field_config])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    sdp1 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=[scan_type])
        .set_processing_blocks(processing_blocks=[processing_block])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_mid_assign_resources_request(
    eb_scan_type,
    scan_type,
    processing_block,
    beams,
    channels,
    polarisatrion_config,
    field_config,
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

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=3600)
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisatrion_config])
        .set_fields(fields=[field_config])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    sdp1 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=[scan_type])
        .set_processing_blocks(processing_blocks=[processing_block])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()
