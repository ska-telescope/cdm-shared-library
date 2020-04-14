"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""

from ska.cdm.messages.subarray_node.scan import ScanRequest


def test_scan_request_init():
    """
    Create a ScanRequest instance with a scan id of 2 and verify __eq__ behaviour.
    """
    scan_id = 2
    scan_request = ScanRequest(scan_id)
    scan_request_2 = ScanRequest(scan_id)

    empty_object = {}

    assert scan_request.scan_id == scan_id
    assert scan_request != empty_object

    # equal if the contents are identical
    assert scan_request == scan_request_2
