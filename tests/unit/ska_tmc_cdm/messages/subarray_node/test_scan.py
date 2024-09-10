"""
Unit tests for the ska_tmc_cdm.messages.subarraynode.scan module
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.scan import LOW_SCHEMA, MID_SCHEMA
from tests.unit.ska_tmc_cdm.builder.subarray_node.scan import (
    ScanRequestBuilder,
)


@pytest.mark.parametrize(
    "object1, object2, is_equal",
    [
        (  # mid equal
            ScanRequestBuilder(),
            ScanRequestBuilder(),
            True,
        ),
        (  # low equal
            ScanRequestBuilder(interface=LOW_SCHEMA),
            ScanRequestBuilder(interface=LOW_SCHEMA),
            True,
        ),
        (  # not_equal
            ScanRequestBuilder(subarray_id=1),
            ScanRequestBuilder(subarray_id=2),
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
            ScanRequestBuilder(interface="test-interface"),
            "test-interface",
        ),
        (
            ScanRequestBuilder(interface=LOW_SCHEMA),
            LOW_SCHEMA,
        ),
        (ScanRequestBuilder(), MID_SCHEMA),
    ),
)
def test_scan_request_default_interface(scan_request, expected_interface):
    """
    Verify that ScanRequest object gets the correct default interface
    """
    assert scan_request.interface == expected_interface
