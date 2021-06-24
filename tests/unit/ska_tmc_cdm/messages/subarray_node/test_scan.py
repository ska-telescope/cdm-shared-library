"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""

import pytest

from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest

MID_SDP_INTERFACE = "https://schema.skatelescope.org/ska-mid-sdp-scan/1.0"
LOW_TMC_INTERFACE = "https://schema.skatelescope.org/ska-low-tmc-scan/1.0"


@pytest.mark.xfail
def test_scan_request_init():
    """
    Create a ScanRequest instance with a scan id of 2 and verify __eq__ behaviour.
    """
    scan_id = 2
    scan_request = ScanRequest(
        interface = MID_SDP_INTERFACE,
        scan_id = scan_id,
    )
    scan_request_2 = ScanRequest(
        interface = MID_SDP_INTERFACE,
        scan_id = scan_id,
    )

    empty_object = {}

    assert scan_request.scan_id == scan_id
    assert scan_request != empty_object

    # equal if the contents are identical
    assert scan_request == scan_request_2


def test_scan_request_init_for_low():
    """
    Create a ScanRequest instance with a scan id of 2 and verify __eq__ behaviour.
    """
    scan_id = 2
    scan_request = ScanRequest(
        interface=LOW_TMC_INTERFACE,
        scan_id=scan_id,
    )
    scan_request_2 = ScanRequest(
        scan_id=scan_id,
        interface=LOW_TMC_INTERFACE
    )

    empty_object = {}

    assert scan_request.scan_id == scan_id
    assert scan_request != empty_object

    # equal if the contents are identical
    assert scan_request == scan_request_2