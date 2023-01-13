"""
Unit tests for the ska_tmc_cdm.messages.subarraynode.scan module
"""

from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CommonConfiguration,
    LowCBFConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest

CSP_CONSTRUCTOR_ARGS = dict(
    common_config=CommonConfiguration(
        subarray_id=1,
    ),
    cbf=LowCBFConfiguration(
        scan_id=987654321,
        unix_epoch_seconds=1616971738,
        timestamp_ns=987654321,
        packet_offset=123456789,
        scan_seconds=30,
    ),
)

CONSTRUCTOR_ARGS = dict(
    interface="interface",
    transaction_id="transaction ID",
    scan_id=123,
    csp=CSP_CONSTRUCTOR_ARGS,
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
