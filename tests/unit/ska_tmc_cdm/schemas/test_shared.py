"""
Unit tests for the ska_tmc_cdm.schemas.shared module.
"""
import pytest

import ska_tmc_cdm.schemas.shared as shared
from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest
from ska_tmc_cdm.schemas.subarray_node.scan import ScanRequestSchema

from . import utils


def test_upper_cased_field_serialises_to_uppercase():
    """
    Verify that UpperCasedField serialises to uppercase text.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = "bar"

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == "BAR"


def test_upper_cased_field_serialises_none():
    """
    Verify that UpperCasedField serialises None to an empty string.
    """

    class TestObject:  # pylint: disable=too-few-public-methods
        """
        Simple test object to hold an attribute.
        """

        def __init__(self):
            self.attr = None

    obj = TestObject()
    serialised = shared.UpperCasedField().serialize("attr", obj)
    assert serialised == ""


def test_upper_cased_field_deserialises_to_uppercase():
    """
    Verify that UpperCasedField deserialises to lowercase text.
    """
    deserialised = shared.UpperCasedField().deserialize("FOO")
    assert deserialised == "foo"


SCAN_VALID_MID_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-scan/2.1",
  "transaction_id": "txn-test-00001",
  "scan_id": 1
}
"""

SCAN_VALID_MID_OBJECT = ScanRequest(
    interface="https://schema.skao.int/ska-tmc-scan/2.1",
    transaction_id="txn-test-00001",
    scan_id=1,
)


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ScanRequestSchema,
            SCAN_VALID_MID_OBJECT,
            None,
            SCAN_VALID_MID_JSON,
            None,
            True,
        ),
    ],
)
def test_assignresources_serialisation_and_validation(
    schema_cls,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls,
        instance,
        modifier_fn,
        valid_json,
        invalid_json,
        is_validate,
    )
