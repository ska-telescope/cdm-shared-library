"""
Unit tests for the ska_tmc_cdm.messages.subarraynode.scan module
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.scan import LOW_SCHEMA, MID_SCHEMA
from tests.unit.ska_tmc_cdm.builder.subarray_node.scan import ScanRequestBuilder


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # mid equal
            ScanRequestBuilder()
            .set_interface(interface=MID_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=1)
            .build(),
            ScanRequestBuilder()
            .set_interface(interface=MID_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=1)
            .build(),
            True,
        ),
        (  # low equal
            ScanRequestBuilder()
            .set_interface(interface=LOW_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=1)
            .build(),
            ScanRequestBuilder()
            .set_interface(interface=LOW_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=1)
            .build(),
            True,
        ),
        (  # not_equal
            ScanRequestBuilder()
            .set_interface(interface=MID_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=1)
            .build(),
            ScanRequestBuilder()
            .set_interface(interface=MID_SCHEMA)
            .set_transaction_id(transaction_id="txn-....-00001")
            .set_scan_id(scan_id=123)
            .set_subarray_id(subarray_id=2)
            .build(),
            False,
        ),
    ],
)
def test_scan_request_equality(object1, object2, is_equal):
    """
    Verify that Scan Request objects are considered equal if attributes have same value and not equal if they differ.
    """
    assert (object1 == object2) == is_equal
    assert object1 != object()


@pytest.mark.parametrize(
    "scan_request, expected_interface",
    (
        (
            ScanRequestBuilder()
            .set_interface("test-interface")
            .set_scan_id(scan_id=1)
            .build(),
            "test-interface",
        ),
        (
            ScanRequestBuilder()
            .set_scan_id(scan_id=1)
            .set_subarray_id(subarray_id=1)
            .build(),
            LOW_SCHEMA,
        ),
        (ScanRequestBuilder().set_scan_id(scan_id=1).build(), MID_SCHEMA),
    ),
)
def test_scan_request_default_interface(scan_request, expected_interface):
    """
    Verify that ScanRequest object gets the correct default interface
    """
    assert scan_request.interface == expected_interface
