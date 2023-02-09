"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas.central_node.release_resources import (
    ReleaseResourcesRequestSchema,
)

from .. import utils

VALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-....-00001",
    "subarray_id": 1,
    "release_all": true
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    release_all=True,
)

# mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-....-00001",
    "subarray_id": 1,
    "release_all": false,
    "receptor_ids": ["0001", "0002"]
}
"""

VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    transaction_id="txn-....-00001",
    subarray_id=1,
    release_all=False,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
)


VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    "subarray_id": 1,
    "release_all": true,
    "transaction_id": "txn-....-00001"
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    subarray_id=1,
    release_all=True,
    transaction_id="txn-....-00001",
)

INVALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    "subarray_id": -1,
    "release_all": true,
    "transaction_id": "txn-....-00001"
}
"""


def low_invalidator_fn(o: ReleaseResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.subarray_id = -1


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ReleaseResourcesRequestSchema,
            VALID_MID_FULL_RELEASE_OBJECT,
            None,  # no validation for MID
            VALID_MID_FULL_RELEASE_JSON,
            None,
        ),  # no validation for MID
        (
            ReleaseResourcesRequestSchema,
            VALID_MID_MIXED_ARGS_OBJECT,
            None,  # no validation for MID
            VALID_MID_MIXED_ARGS_JSON,
            None,
        ),  # no validation for MID
        (
            ReleaseResourcesRequestSchema,
            VALID_LOW_FULL_RELEASE_OBJECT,
            None,  # TODO- replace None with low_invalidator_fn to the test  invalid case when low schemas are available in telemodel library
            VALID_LOW_FULL_RELEASE_JSON,
            None,  # TODO- replace None with INVALID_LOW_FULL_RELEASE_JSON to test invalid case when low schemas are available in telemodel library
        ),
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
