"""
Unit tests for ska.cdm.schemas.mccscontroller.allocate module.
"""
import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.mccscontroller.allocate import AllocateRequest
from ska.cdm.schemas.mccscontroller.allocate import AllocateRequestSchema
from ska.cdm.utils import json_is_equal
from ska.cdm.schemas.shared import ValidatingSchema

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
  "subarray_id": 1,
  "subarray_beam_ids": [1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
  "subarray_id": 1,
  "subarray_beam_ids": [49],
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


def test_deserialising_invalid_json_raises_exception_when_strict():
    schema = AllocateRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_JSON)


def test_serialising_invalid_object_raises_exception_when_strict():
    o = copy.deepcopy(VALID_OBJECT)
    o.subarray_beam_ids = [49]

    schema = AllocateRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_unmarshall_allocaterequest():
    """
    Verify that JSON can be unmarshalled back to an AllocateRequest object.
    """
    unmarshalled = AllocateRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT
