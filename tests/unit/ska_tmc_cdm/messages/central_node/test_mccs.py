"""
Unit tests for the CentralNode.mccs allocate module.
"""
import copy

from tests.unit.ska_tmc_cdm.builder_pattern.central_node.mccs import MCCSAllocateBuilder


def mccs_allocate(subarray_beam_ids, station_ids, channel_blocks):
    mccs = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=subarray_beam_ids)
        .set_station_ids(station_ids=station_ids)
        .set_channel_blocks(channel_blocks=channel_blocks)
        .build()
    )
    return mccs


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocate objects with the same allocated elements are
    considered equal.
    """
    mccs = mccs_allocate(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    mccs1 = mccs_allocate(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )

    assert mccs == mccs1

    alt_params = dict(
        subarray_beam_ids=[2], station_ids=[(1, 2, 3)], channel_blocks=[4]
    )

    for (
        k,
        v,
    ) in alt_params.items():
        o = copy.deepcopy(mccs)
        setattr(o, k, v)
        assert o != mccs


def test_mccs_allocate_eq_with_other_objects():
    """
    Verify that a MCCSAllocate is considered unequal to objects of other
    types.
    """
    o = mccs_allocate(subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3])
    assert o != 1
    assert o != object()
