"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.scan module
"""

import pytest

from ska_tmc_cdm.exceptions import JsonValidationError
from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest
from ska_tmc_cdm.schemas.shared import ValidatingSchema
from ska_tmc_cdm.schemas.subarray_node.scan import ScanRequestSchema
from ska_tmc_cdm.utils import json_is_equal
from .. import utils

VALID_MID_SCANREQUEST_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-scan/2.0",
  "scan_id": 1,
  "transaction_id": "txn-test-00001",
}
"""

VALID_MID_SCANREQUEST_OBJECT = ScanRequest(
    interface = "https://schema.skao.int/ska-tmc-scan/2.0",
    scan_id = 1,
    transaction_id = "txn-test-00001",
)

VALID_LOW_SCANREQUEST_JSON = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "scan_id": 1
}
"""

VALID_LOW_SCANREQUEST_OBJECT = ScanRequest(
    interface="https://schema.skao.int/ska-low-tmc-scan/2.0",
    scan_id=1
)

INVALID_LOW_SCANREQUEST_JSON = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "scan_id": -1.3
}
"""


@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        #(ScanRequestSchema,
        # VALID_MID_SCANREQUEST_OBJECT,
        # None,  # No validation for MID
        # VALID_MID_SCANREQUEST_JSON,
        # None),  # no validation for MID
        (ScanRequestSchema,
         VALID_LOW_SCANREQUEST_OBJECT,
         None,  # schema does not impose any constraints so nothing to test
         VALID_LOW_SCANREQUEST_JSON,
         INVALID_LOW_SCANREQUEST_JSON),
    ]
)
def test_assigned_resources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ScanRequestSchema marshals, unmarshals, and validates
    correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )
