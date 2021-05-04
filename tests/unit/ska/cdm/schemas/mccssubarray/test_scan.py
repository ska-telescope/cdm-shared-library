"""
Unit tests for ska.cdm.schemas.mccssubarray.scan module.
"""

import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.mccssubarray.scan import ScanRequest
from ska.cdm.schemas.mccssubarray.scan import ScanRequestSchema
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.utils import json_is_equal

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
  "scan_id":1,
  "start_time": 0.0
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
  "scan_id": "foo",
  "start_time": -1.0
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
    Verify that JSON can be unmarshalled back to an ScanRequest
    object.
    """
    unmarshalled = ScanRequestSchema().loads(VALID_JSON)
    assert unmarshalled == VALID_OBJECT


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = ScanRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_JSON)


@pytest.mark.xfail(strict=True)
def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.

    This test is currently xfailed as the MCCSSubarray.Scan Telescope Model
    schema does not have any range validation to test.
    """
    o = copy.deepcopy(VALID_OBJECT)
    o.start_time = -1.0

    schema = ScanRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.dumps(o)


def test_serialising_valid_object_does_not_raise_exception_when_strict():
    """
    Verify that an exception is not raised when a valid object is serialised
    in strict mode.
    """
    schema = ScanRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    _ = schema.dumps(VALID_OBJECT)
