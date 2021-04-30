"""
Unit tests for ska.cdm.schemas.mccscontroller.releaseresources module.
"""

from ska.cdm.messages.mccscontroller.releaseresources import ReleaseResourcesRequest
from ska.cdm.schemas.mccscontroller.releaseresources import (
    ReleaseResourcesRequestSchema
)
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": 1,
  "release_all": true
}
"""

VALID_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
    subarray_id=1,
    release_all=True
)


def test_marshal_releaseresourcesrequest():
    """
    Verify that ReleaseResourcesRequest is marshalled to JSON correctly.
    """
    json_str = ReleaseResourcesRequestSchema().dumps(VALID_OBJECT)
    assert json_is_equal(json_str, VALID_JSON)


def test_unmarshal_releaseresourcesrequest():
    """
    Verify that JSON can be unmarshalled back to a ReleaseResourcesRequest
    object.
    """
    unmarshalled = ReleaseResourcesRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT
