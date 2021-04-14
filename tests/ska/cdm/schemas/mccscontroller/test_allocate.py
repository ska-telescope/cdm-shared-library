"""
Unit tests for ska.cdm.schemas.mccscontroller.allocate module.
"""

from ska.cdm.messages.mccscontroller.allocate import AllocateRequest
from ska.cdm.schemas.mccscontroller.allocate import AllocateRequestSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
  "subarray_id": 1,
  "subarray_beam_ids": [1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

VALID_OBJECT = AllocateRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
    subarray_id=1,
    subarray_beam_ids=[1],
    station_ids=[[1, 2]],
    channel_blocks=[3]
)


def test_marshal_allocaterequest():
    """
    Verify that AllocateRequest is marshalled to JSON correctly.
    """
    json_str = AllocateRequestSchema().dumps(VALID_OBJECT)
    assert json_is_equal(json_str, VALID_JSON)


def test_unmarshall_allocaterequest():
    """
    Verify that JSON can be unmarshalled back to an AllocateRequest object.
    """
    unmarshalled = AllocateRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT
