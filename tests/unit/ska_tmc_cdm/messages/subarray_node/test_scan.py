"""
Unit tests for the ska_tmc_cdm.messages.subarraynode.scan module
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.scan import LOW_SCHEMA, MID_SCHEMA
from tests.unit.ska_tmc_cdm.builder.subarray_node.scan import ScanRequestBuilder

def test_scanrequest_eq():
    """
    Verify that scan requests with the same values are considered equal.
    """

    request = ScanRequestBuilder().set_interface(interface="https://schema.skao.intg/ska-tmc-scan/2.0").set_transaction_id(transaction_id="txn-....-00001").set_scan_id(scan_id=123).set_subarray_id(subarray_id=1).build()
    request1 = ScanRequestBuilder().set_interface(interface="https://schema.skao.intg/ska-tmc-scan/2.0").set_transaction_id(transaction_id="txn-....-00001").set_scan_id(scan_id=123).set_subarray_id(subarray_id=1).build()
    assert request == request1

    request2 = ScanRequestBuilder().set_interface(interface="https://schema.skao.intg/ska-tmc-scan/2.0").set_transaction_id(transaction_id="txn-....-00001").set_scan_id(scan_id=123).set_subarray_id(subarray_id=2)
    assert request2 !=request

def test_scanrequest_not_equal_to_other_objects():
    """
    Verify that ScanRequest objects are not considered equal to objects
    of other types.
    """
    request = ScanRequestBuilder().set_interface(interface="https://schema.skao.intg/ska-tmc-scan/2.0").set_transaction_id(transaction_id="txn-....-00001").set_scan_id(scan_id=123).set_subarray_id(
        subarray_id=1).build()
    assert request != 1
    assert request != object()


@pytest.mark.parametrize(
    "scan_request, expected_interface",

    (
            (ScanRequestBuilder().set_interface("test-interface").set_scan_id(scan_id=1).build(), "test-interface"),
            (ScanRequestBuilder().set_scan_id(scan_id=1).set_subarray_id(subarray_id=1).build(), LOW_SCHEMA),
            (ScanRequestBuilder().set_scan_id(scan_id=1).build(), MID_SCHEMA),
    )
)
def test_scanrequest_default_interface(scan_request, expected_interface):
    """
    Verify that ScanRequest object gets the correct default interface
    """
    assert scan_request.interface == expected_interface
