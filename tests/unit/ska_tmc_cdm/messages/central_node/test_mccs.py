"""
Unit tests for the CentralNode.mccs allocate module.
"""
import copy

from polyfactory.factories import DataclassFactory

from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate


class MCCSAllocateFactory(DataclassFactory[MCCSAllocate]):
    __model__ = MCCSAllocate


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocate objects with the same allocated elements are
    considered equal.
    """
    mccs = MCCSAllocateFactory.build()
    mccs1 = MCCSAllocateFactory.build(
        subarray_beam_ids=mccs.subarray_beam_ids,
        station_ids=mccs.station_ids,
        channel_blocks=mccs.channel_blocks,
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
    o = MCCSAllocateFactory.build()
    assert o != 1
    assert o != object()
