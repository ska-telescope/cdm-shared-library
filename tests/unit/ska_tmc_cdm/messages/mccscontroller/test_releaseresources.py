"""
Unit tests for the mccscontroller.releaseresources module
"""
from ska_tmc_cdm.messages.mccscontroller.releaseresources import (
    ReleaseResourcesRequest,
)


def test_releaseresourcesrequest_object_equality():
    """
    Verify that two ReleaseResourcesRequest objects with the same allocated elements are
    considered equal.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-releaseresources/2.0",
        subarray_id=1,
        release_all=True,
    )
    request = ReleaseResourcesRequest(**constructor_args)

    # objects with same property values are considered equal
    other = ReleaseResourcesRequest(**constructor_args)
    assert request == other

    # objects where any property differs are considered unequal
    different_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-releaseresources/999.0",
        subarray_id=2,
        release_all=False,
    )
    for k, v in different_args.items():
        other_args = dict(constructor_args)
        other_args[k] = v
        assert request != ReleaseResourcesRequest(**other_args)


def test_releaseresourcesrequest_equality_with_other_objects():
    """
    Verify that a ReleaseResourcesRequest is considered unequal to objects of other
    types.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-releaseresources/2.0",
        subarray_id=1,
        release_all=True,
    )
    request = ReleaseResourcesRequest(**constructor_args)

    assert request != 1
    assert request != object()
