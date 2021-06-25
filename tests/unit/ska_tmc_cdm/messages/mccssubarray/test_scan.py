"""
Unit tests for the mccssubarray.scan module
"""
from ska_tmc_cdm.messages.mccssubarray.scan import ScanRequest


def test_releaseresourcesrequest_object_equality():
    """
    Verify that two ScanRequest objects with the same allocated elements are
    considered equal.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-scan/1.0",
        scan_id=1,
        start_time=0.0
    )
    request = ScanRequest(**constructor_args)

    # objects with same property values are considered equal
    other = ScanRequest(**constructor_args)
    assert request == other

    # objects where any property differs are considered unequal
    different_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-scan/2.0",
        scan_id=2,
        start_time=1.0
    )
    for k, v in different_args.items():
        other_args = dict(constructor_args)
        other_args[k] = v
        assert request != ScanRequest(**other_args)


def test_releaseresourcesrequest_equality_with_other_objects():
    """
    Verify that a ScansRequest is considered unequal to objects of other
    types.
    """
    constructor_args = dict(
        interface="https://schema.skao.int/ska-low-mccs-scan/1.0",
        scan_id=1,
        start_time=0.0
    )
    request = ScanRequest(**constructor_args)

    assert request != 1
    assert request != object()
