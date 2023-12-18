"""
Unit tests for the ska_tmc_cdm.messages.subarraynode.scan module
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.scan import LOW_SCHEMA, MID_SCHEMA, ScanRequest

CONSTRUCTOR_ARGS = dict(
    interface="interface", transaction_id="transaction ID", scan_id=123, subarray_id=1
)


def test_scanrequest_eq():
    """
    Verify that scan requests with the same values are considered equal.
    """
    # objects with same property values are considered equal
    request = ScanRequest(**CONSTRUCTOR_ARGS)
    other = ScanRequest(**CONSTRUCTOR_ARGS)
    assert request == other

    alternate_args = dict(interface="foo", transaction_id="foo", scan_id=99999)
    for k, v in alternate_args.items():
        other_args = dict(CONSTRUCTOR_ARGS)
        other_args[k] = v
        assert request != ScanRequest(**other_args)


def test_scanrequest_not_equal_to_other_objects():
    """
    Verify that ScanRequest objects are not considered equal to objects
    of other types.
    """
    request = ScanRequest(**CONSTRUCTOR_ARGS)
    assert request != 1
    assert request != object()


@pytest.mark.parametrize(
    "scan_request, expected_interface",
    (
        (ScanRequest(interface="test-interface", scan_id=1), "test-interface"),
        (ScanRequest(scan_id=1, subarray_id=1), LOW_SCHEMA),
        (ScanRequest(scan_id=1), MID_SCHEMA),
    ),
)
def test_scanrequest_default_interface(scan_request, expected_interface):
    """
    Verify that ScanRequest object gets the correct default interface
    """
    assert scan_request.interface == expected_interface
