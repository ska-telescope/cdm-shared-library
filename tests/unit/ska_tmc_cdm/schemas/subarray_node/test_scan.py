"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.scan module
"""

import pytest

from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest
from ska_tmc_cdm.schemas.subarray_node.configure.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCBFConfiguration,
)
from ska_tmc_cdm.schemas.subarray_node.scan import ScanRequestSchema

from .. import utils

VALID_MID_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-scan/2.1",
  "transaction_id": "txn-test-00001",
  "scan_id": 1
}
"""

VALID_MID_OBJECT = ScanRequest(
    interface="https://schema.skao.int/ska-tmc-scan/2.1",
    transaction_id="txn-test-00001",
    scan_id=1,
)

VALID_LOW_JSON = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "transaction_id": "txn-test-00001",
    "scan_id": 1
}
"""

VALID_LOW_OBJECT = ScanRequest(
    interface="https://schema.skao.int/ska-low-tmc-scan/2.0",
    transaction_id="txn-test-00001",
    scan_id=1,
)

INVALID_LOW_JSON = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "transaction_id": "txn-test-00001",     
    "scan_id": 1.23
}
"""

VALID_LOW_JSON_PI17 = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "transaction_id": "txn-test-00001",
    "scan_id": 1,
    "csp": {
    "common": {
      "subarray_id": 1
    },
    "lowcbf": {
      "scan_id": 987654321,
      "unix_epoch_seconds": 1616971738,
      "timestamp_ns": 987654321,
      "packet_offset": 123456789,
      "scan_seconds": 30
    }
  }
}
"""

VALID_LOW_OBJECT_PI17 = ScanRequest(
    interface="https://schema.skao.int/ska-low-tmc-scan/2.0",
    transaction_id="txn-test-00001",
    scan_id=1,
    csp=CSPConfiguration(
        common=CommonConfiguration(subarray_id=1),
        lowcbf=LowCBFConfiguration(
            scan_id=987654321,
            unix_epoch_seconds=1616971738,
            timestamp_ns=987654321,
            packet_offset=123456789,
            scan_seconds=30,
        ),
    ),
)

INVALID_LOW_JSON_PI17 = """
{   
    "interface": "https://schema.skao.int/ska-low-tmc-scan/2.0",
    "transaction_id": "txn-test-00001",     
    "scan_id": 1.23,
    "csp": {
    "common": {
      "subarray_id": -1
    },
    "lowcbf": {
      "scan_id": -987654321,
      "unix_epoch_seconds": -1616971738,
      "timestamp_ns": -987654321,
      "packet_offset": -123456789,
      "scan_seconds": -30
    }
  }
}
"""


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ScanRequestSchema,
            VALID_MID_OBJECT,
            None,  # No validation for MID
            VALID_MID_JSON,
            None,
        ),  # no validation for MID
    ],
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


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ScanRequestSchema,
            VALID_LOW_OBJECT_PI17,
            None,  # schema does not impose any constraints so nothing to test
            VALID_LOW_JSON_PI17,
            None,
        )
    ],
)
def test_assigned_resources_serialisation_and_validation_pi17(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ScanRequestSchema marshals, unmarshals, and validates
    correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json, validate=False
    )


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ScanRequestSchema,
            VALID_LOW_OBJECT,
            None,  # schema does not impose any constraints so nothing to test
            VALID_LOW_JSON,
            INVALID_LOW_JSON,
        )
    ],
)
def test_assigned_resources_serialisation_and_validation_invalid_low_json(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ScanRequestSchema marshals, unmarshals, and validates
    correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json, validate=True
    )
