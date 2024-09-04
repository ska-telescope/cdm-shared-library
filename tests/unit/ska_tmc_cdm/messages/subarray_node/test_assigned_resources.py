"""
Unit tests for the TMC Assigned Resources
"""


from ska_tmc_cdm.messages.subarray_node.assigned_resources import (
    SCHEMA,
    AssignedResources,
    MCCSAllocation,
)


def test_mccs_allocation_is_empty():
    """
    Verify that we can detect an empty MCCSAllocation
    """
    mccs_allocation = MCCSAllocation(
        subarray_beam_ids=[], station_ids=[], channel_blocks=[]
    )

    assert mccs_allocation.is_empty()


def test_mccs_allocation_is_not_empty():
    """
    Verify that we can detect an MCCSAllocation is not empty
    """
    mccs_allocation = MCCSAllocation(
        subarray_beam_ids=[1, 2, 3, 4],
        station_ids=[[1, 2, 3, 4, 5]],
        channel_blocks=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
    assert not mccs_allocation.is_empty()


def test_assigned_resources_default_interface():
    """
    Verify the default interface string is used when omitted from
    invocation
    """
    mccs_allocation = MCCSAllocation(
        subarray_beam_ids=[], station_ids=[], channel_blocks=[]
    )
    expected_string = SCHEMA
    assigned_resources = AssignedResources(mccs=mccs_allocation)
    assert assigned_resources.interface == expected_string


def test_assigned_resources_is_empty():
    """
    Verify that we can detect an empty MCCSAllocation
    """
    mccs_allocation = MCCSAllocation(
        subarray_beam_ids=[], station_ids=[], channel_blocks=[]
    )
    assigned_resources = AssignedResources(mccs=mccs_allocation)
    assert assigned_resources.is_empty()


def test_assigned_resources_is_not_empty():
    """
    Verify that we can detect an MCCSAllocation is not empty
    """
    mccs_allocation = MCCSAllocation(
        subarray_beam_ids=[1, 2, 3, 4],
        station_ids=[[1, 2, 3, 4, 5]],
        channel_blocks=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
    assigned_resources = AssignedResources(mccs=mccs_allocation)
    assert not assigned_resources.is_empty()
