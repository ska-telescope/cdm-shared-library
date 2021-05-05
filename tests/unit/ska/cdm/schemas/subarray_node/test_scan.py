"""
Unit tests for the ska.cdm.schemas.subarray_node.scan module
"""

import copy

import pytest

from ska.cdm.exceptions import JsonValidationError
from ska.cdm.messages.subarray_node.scan import ScanRequest
from ska.cdm.schemas.shared import ValidatingSchema
from ska.cdm.schemas.subarray_node.scan import ScanRequestSchema
from ska.cdm.utils import json_is_equal

VALID_MID_SCANREQUEST_JSON = """
{
    "id": 1
}
"""

VALID_MID_SCANREQUEST_OBJECT = ScanRequest(
    scan_id=1
)

VALID_LOW_SCANREQUEST_JSON = """
{   
    "interface": "https://schema.skatelescope.org/ska-low-tmc-scan/1.0",
    "scan_id": 1
}
"""

VALID_LOW_SCANREQUEST_OBJECT = ScanRequest(
    interface="https://schema.skatelescope.org/ska-low-tmc-scan/1.0",
    scan_id=1
)

INVALID_LOW_SCANREQUEST_JSON = """
{   
    "interface": "https://schema.skatelescope.org/ska-low-tmc-scan/1.0",
    "scan_id": -1.3
}
"""


@pytest.mark.parametrize('instance, expected', [
    (VALID_MID_SCANREQUEST_OBJECT, VALID_MID_SCANREQUEST_JSON),
    (VALID_LOW_SCANREQUEST_OBJECT, VALID_LOW_SCANREQUEST_JSON)
])
def test_marshal(instance, expected):
    """
    Verify that objects are marshaled to JSON correctly.
    """
    schema = ScanRequestSchema()
    json_str = schema.dumps(instance)
    assert json_is_equal(json_str, expected)


@pytest.mark.parametrize('json_str, expected', [
    (VALID_MID_SCANREQUEST_JSON, VALID_MID_SCANREQUEST_OBJECT),
    (VALID_LOW_SCANREQUEST_JSON, VALID_LOW_SCANREQUEST_OBJECT)
])
def test_unmarshal(json_str, expected):
    """
    Verify that JSON can be unmarshaled back to objects.
    """
    schema = ScanRequestSchema()
    unmarshaled = schema.loads(json_str)
    assert unmarshaled == expected


def test_deserialising_invalid_json_raises_exception_when_strict():
    """
    Verify that an exception is raised when invalid JSON is deserialised in
    strict mode.
    """
    schema = ScanRequestSchema()
    schema.context[ValidatingSchema.VALIDATE] = True
    schema.context[ValidatingSchema.VALIDATION_STRICTNESS] = 2

    with pytest.raises(JsonValidationError):
        _ = schema.loads(INVALID_LOW_SCANREQUEST_JSON)


@pytest.mark.xfail(strict=True)
def test_serialising_invalid_object_raises_exception_when_strict():
    """
    Verify that an exception is raised when an invalid object is serialised in
    strict mode.

    This test is xfailed as the telescope model schema for SubArrayNode.Scan
    does not impose any constraints.
    """
    o = copy.deepcopy(VALID_LOW_SCANREQUEST_OBJECT)
    o.scan_id = -1

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

    _ = schema.dumps(VALID_LOW_SCANREQUEST_OBJECT)
