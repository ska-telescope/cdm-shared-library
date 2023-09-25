"""
Unit tests for the mccscontroller.assignresources module
"""
from ska_tmc_cdm.messages.mccssubarray.assigned_resources import AssignedResources


def test_assignresourcesrequest_object_equality():
    """
    Verify that two AssignResourcesRequest objects with the same allocated elements are
    considered equal.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-assignedresources/2.0",
        subarray_beam_ids=[1],
        station_ids=[1, 2],
        channel_blocks=[3],
    )
    request = AssignedResources(**constructor_args)

    # objects with same property values are considered equal
    other = AssignedResources(**constructor_args)
    assert request == other

    # objects where any property differs are considered unequal
    different_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-assignedresources/99.0",
        subarray_beam_ids=[2],
        station_ids=[1, 2, 3],
        channel_blocks=[4],
    )
    for k, v in different_args.items():
        other_args = dict(constructor_args)
        other_args[k] = v
        assert request != AssignedResources(**other_args)


def test_assignresourcesrequest_equality_with_other_objects():
    """
    Verify that a AssignResourcesRequest is considered unequal to objects of other
    types.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-assignedresources/2.0",
        subarray_beam_ids=[1],
        station_ids=[1, 2],
        channel_blocks=[3],
    )
    request = AssignedResources(**constructor_args)

    assert request != 1
    assert request != object()
