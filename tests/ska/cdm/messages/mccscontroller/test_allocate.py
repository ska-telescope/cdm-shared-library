"""
Unit tests for the mccscontroller.allocate module
"""
from ska.cdm.messages.mccscontroller.allocate import AllocateRequest


def test_allocaterequest_object_equality():
    """
    Verify that two AllocateRequest objects with the same allocated elements are
    considered equal.
    """
    constructor_args = dict(
        interface="https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
        subarray_id=1,
        subarray_beam_ids=[1],
        station_ids=[[1, 2]],
        channel_blocks=[3],
    )
    request = AllocateRequest(**constructor_args)

    # objects with same property values are considered equal
    other = AllocateRequest(**constructor_args)
    assert request == other

    # objects where any property differs are considered unequal
    different_args = dict(
        interface="https://schema.skatelescope.org/ska-low-mccs-assignresources/2.0",
        subarray_id=2,
        subarray_beam_ids=[2],
        station_ids=[[1, 2, 3]],
        channel_blocks=[4],
    )
    for k, v in different_args.items():
        other_args = dict(constructor_args)
        other_args[k] = v
        assert request != AllocateRequest(**other_args)


def test_allocaterequest_equality_with_other_objects():
    """
    Verify that an AllocateRequest is considered unequal to objects of other
    types.
    """
    constructor_args = dict(
        interface="https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
        subarray_id=1,
        subarray_beam_ids=[1],
        station_ids=[[1, 2]],
        channel_blocks=[3],
    )
    request = AllocateRequest(**constructor_args)

    assert request != 1
    assert request != object()
