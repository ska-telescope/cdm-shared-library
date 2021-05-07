"""
Unit tests for the CentralNode.mccs allocate module.
"""
import copy

import itertools

from ska.cdm.messages.central_node.mccs import MCCSAllocate


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocate objects with the same allocated elements are
    considered equal.
    """
    orig = MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1,2)],
        channel_blocks=[3]
    )

    assert orig == MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1,2)],
        channel_blocks=[3]
    )

    alt_params = dict(
        subarray_beam_ids=[2],
        station_ids=[(1, 2, 3)],
        channel_blocks=[4]
    )

    for k, v, in alt_params.items():
        o = copy.deepcopy(orig)
        setattr(o, k, v)
        assert o != orig


def test_mccs_allocate_eq_with_other_objects():
    """
    Verify that a MCCSAllocate is considered unequal to objects of other
    types.
    """
    o = MCCSAllocate(
        subarray_beam_ids=[1],
        station_ids=[(1,2)],
        channel_blocks=[3]
    )

    assert o != 1
    assert o != object()
