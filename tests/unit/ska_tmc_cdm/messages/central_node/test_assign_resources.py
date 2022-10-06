"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import copy
import itertools

import pytest

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    ExecutionBlockConfuguration,
    FieldConfiguration,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    SDPConfiguration,
    SDPWorkflow,
)


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel])
    sdp_workflow = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    pb_config = ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", sdp_workflow, {}
    )
    sdp_config = SDPConfiguration(
        "sbi-mvp01-20200325-00001",
        100.0,
        [scan_type],
        [pb_config],
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request == AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request != AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=None,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00002",
    )
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(
        1,
        dish_allocation=None,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )


def test_assign_resources_request_mccs_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs = MCCSAllocate(subarray_beam_ids=[1], station_ids=[(1, 2)], channel_blocks=[3])
    request = AssignResourcesRequest(subarray_id=1, mccs=mccs)
    assert request == AssignResourcesRequest(subarray_id=1, mccs=mccs)
    assert request != AssignResourcesRequest(subarray_id=2, mccs=mccs)

    o = copy.deepcopy(mccs)
    o.subarray_beam_ids = [2]
    assert request != AssignResourcesRequest(subarray_id=1, mccs=o)


def test_assign_resources_request_from_mccs():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]
    )
    request = AssignResourcesRequest.from_mccs(subarray_id=1, mccs=mccs_allocate)

    expected = AssignResourcesRequest(
        subarray_id=1,
        mccs=MCCSAllocate(
            list(zip(itertools.count(1, 1), 1 * [2])),
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 6],
        ),
    )
    assert request == expected


def test_assign_resources_request_from_dish():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest.from_dish(1, dish_allocation=dish_allocation)
    assert request == AssignResourcesRequest(1, dish_allocation=dish_allocation)


def test_assign_resources_request_dish_and_mccs_fail():
    """
    Verify that mccs & dish cannot be allocated together
    """
    mccs_allocate = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    )

    with pytest.raises(ValueError):
        dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
        AssignResourcesRequest(dish_allocation=dish_allocation, mccs=mccs_allocate)


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=None
    )
    assert request != 1
    assert request != object()


def test_assign_resources_request_eq_mccs_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    mccs_allocate = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
    request = AssignResourcesRequest(subarray_id=1, mccs=mccs_allocate)
    assert request != 1
    assert request != object()


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    unequal_allocation = DishAllocation(receptor_ids=["b", "aab"])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)

    assert response == AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != AssignResourcesResponse(dish_allocation=DishAllocation())
    assert response != AssignResourcesResponse(dish_allocation=unequal_allocation)


def test_assign_resources_response_eq_with_other_objects():
    """
    Verify that an AssignResourcesRequest response object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != 1
    assert response != object()


def test_assign_resources_request_for_low_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
    request = AssignResourcesRequest(
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
        mccs=mccs_allocate,
        subarray_id=1,
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request == AssignResourcesRequest(
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
        mccs=mccs_allocate,
        subarray_id=1,
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request != AssignResourcesRequest(
        mccs=MCCSAllocate(
            list(zip(itertools.count(1, 1), 1 * [1])),
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        interface="https://schema.skao.int/ska-low-tmc-assignresources/2.0",
        subarray_id=2,
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request != AssignResourcesRequest(
        mccs=MCCSAllocate(
            list(zip(itertools.count(1, 1), 1 * [2])), [3, 4, 5], [1, 2, 3, 4, 5, 6]
        ),
        subarray_id=2,
        interface="https://schema.skao.int/ska-low-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])

    with pytest.raises(ValueError):
        _ = AssignResourcesRequest(mccs=mccs)

    with pytest.raises(ValueError):
        _ = AssignResourcesRequest(dish_allocation=dish_allocation)


# New modified JSO -> PI 16


def test_modified_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        0.368e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel])
    sdp_workflow = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    pb_config = ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", sdp_workflow, {}
    )
    beams = BeamConfiguration("pss1", 1, "pulsar search")
    channels = ChannelConfiguration(
        "vis_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )
    polarisation = PolarisationConfiguration("all", ["XX", "XY", "YY", "YX"])
    fields = FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointing",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )

    execution_block = ExecutionBlockConfuguration(
        "eb-mvp01-20200325-00001",
        100,
        {},
        [beams],
        [channels],
        [polarisation],
        [fields],
    )
    sdp_config = SDPConfiguration(
        "eb-mvp01-20200325-00001",
        100.0,
        [scan_type],
        [pb_config],
        [execution_block],
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request == AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request != AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=None,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00002",
    )
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(
        1,
        dish_allocation=None,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )


def test_modified_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    channel = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        0.368e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel])
    sdp_workflow = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    pb_config = ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", sdp_workflow, {}
    )
    beams = BeamConfiguration("pss1", 1, "pulsar search")
    channels = ChannelConfiguration(
        "vis_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )
    polarisation = PolarisationConfiguration("all", ["XX", "XY", "YY", "YX"])
    fields = FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointing",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )

    execution_block = ExecutionBlockConfuguration(
        "eb-mvp01-20200325-00001",
        100,
        {},
        [beams],
        [channels],
        [polarisation],
        [fields],
    )
    sdp_config = SDPConfiguration(
        "eb-mvp01-20200325-00001",
        100.0,
        [scan_type],
        [pb_config],
        [execution_block],
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=sdp_config
    )
    assert request != 1
    assert request != object()