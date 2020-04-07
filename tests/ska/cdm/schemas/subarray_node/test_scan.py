"""
Unit tests for the ska.cdm.schemas.subarray_node.scan module
"""

from ska.cdm.messages.subarray_node.scan import ScanRequest
from ska.cdm.schemas.subarray_node.scan import ScanRequestSchema
from ..utils import json_is_equal

VALID_SCAN_REQUEST = '{"id": 1}'


def test_marshall_start_scan_request():
    """
    Verify that ScanRequest is marshalled to JSON correctly.
    """
    scan_id = 1
    scan_request = ScanRequest(scan_id)
    schema = ScanRequestSchema()
    result = schema.dumps(scan_request)

    assert json_is_equal(result, VALID_SCAN_REQUEST)


def test_unmarshall_start_scan_request():
    """
    Verify that JSON can be unmarshalled back to a ScanRequest
    """
    schema = ScanRequestSchema()
    result = schema.loads(VALID_SCAN_REQUEST)
    expected = ScanRequest(1)

    assert result.scan_id is not None
    assert result == expected
