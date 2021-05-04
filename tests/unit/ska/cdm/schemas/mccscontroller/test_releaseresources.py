"""
Unit tests for ska.cdm.schemas.mccscontroller.releaseresources module.
"""
import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.mccscontroller.releaseresources import ReleaseResourcesRequest
from ska.cdm.schemas.mccscontroller.releaseresources import ReleaseResourcesRequestSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": 1,
  "release_all": true
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": -1,
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


def test_deserialising_invalid_json_raises_exception_when_strict():
    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    o = copy.deepcopy(VALID_OBJECT)
    o.subarray_id = -1

    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_object_does_not_raise_exception_when_strict():
    schema = ReleaseResourcesRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_OBJECT)
