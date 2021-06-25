"""
Unit tests for ska_tmc_cdm.schemas.mccssubarray.scan module.
"""

import pytest

from ska_tmc_cdm.messages.mccssubarray.scan import ScanRequest
from ska_tmc_cdm.schemas.mccssubarray.scan import ScanRequestSchema
from .. import utils

VALID_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-scan/1.0",
  "scan_id":1,
  "start_time": 0.0
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-mccs-scan/1.0",
  "scan_id": "foo",
  "start_time": -1.0
}
"""

VALID_OBJECT = ScanRequest(
    interface="https://schema.skao.int/ska-low-mccs-scan/1.0",
    scan_id=1,
    start_time=0.0
)


def invalidator_fn(o: ScanRequest):
    # function to make a valid ScanRequest invalid
    o.start_time = -1.0


@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (ScanRequestSchema,
         VALID_OBJECT,
         invalidator_fn,
         VALID_JSON,
         INVALID_JSON),
    ]
)
def test_releaseresources_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )
