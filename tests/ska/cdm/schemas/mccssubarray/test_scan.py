"""
Unit tests for ska.cdm.schemas.mccssubarray.scan module.
"""

from ska.cdm.messages.mccssubarray.scan import ScanRequest
from ska.cdm.schemas.mccssubarray.scan import ScanRequestSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
  "scan_id":1,
  "start_time": 0.0
}
"""

VALID_OBJECT = ScanRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
    scan_id=1,
    start_time=0.0
)


def test_marshal_scanrequest():
    """
    Verify that ScanRequest is marshalled to JSON correctly.
    """
    json_str = ScanRequestSchema().dumps(VALID_OBJECT)
    assert json_is_equal(json_str, VALID_JSON)


def test_unmarshal_scanrequest():
    """
    Verify that JSON can be unmarshalled back to an MCCSAllocate
    object.
    """
    unmarshalled = ScanRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT
