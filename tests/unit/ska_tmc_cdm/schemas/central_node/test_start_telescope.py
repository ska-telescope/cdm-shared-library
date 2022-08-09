"""
Unit tests for ska_tmc_cdm.schemas.central_node.telescope_start module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescopeRequest
from ska_tmc_cdm.schemas.central_node.telescope_start import StartTelescopeRequestSchema

from .. import utils

# sample valid json, object for telescope start ...
VALID_TELESCSTART_JSON = """
{
  "subarray_id": 1,
  "interface": "https://schema.skao.int/ska-tmc-telescopestart/1.0",
  "transaction_id":"txn-ts01-20220803-00004"  
}
"""
VALID_TELESCSTART_OBJECT = StartTelescopeRequest(
    subarray_id=1,
    interface="https://schema.skao.int/ska-tmc-telescopestart/1.0",  # dummy interface url
    transaction_id="txn-ts01-20220803-00004",
)

# checking ...


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            StartTelescopeRequestSchema,
            VALID_TELESCSTART_OBJECT,
            None,  # no validation on subschema
            VALID_TELESCSTART_JSON,
            None,
        ),  # no validation on subschema
    ],
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
