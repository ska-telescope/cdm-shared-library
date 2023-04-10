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

VALID_MID_PARTIAL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-blah-blah-00001",
    "subarray_id": 1,
    "release_all":false,
    "receptor_ids": ["0001", "0002"]
}
"""


VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    transaction_id="txn-blah-blah-00001",
    subarray_id=1,
    release_all=False,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "subarray_id": 1,
    "transaction_id": "txn-blah-blah-00001",
    "release_all": true,
    "receptor_ids":[]        
}
"""
# added receptor id in both object and json
VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    subarray_id=1,
    transaction_id="txn-blah-blah-00001",
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=[]),
)

# # mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    subarray_id=1,
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    "subarray_id": 1,
    "release_all": true,
    "transaction_id": "txn-blah-blah-00001"
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-releaseresources/3.0",
    subarray_id=1,
    release_all=True,
    transaction_id="txn-blah-blah-00001",
)

INVALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "subarray_id": -1,
    "release_all": true,
    "transaction_id": "txn-blah-blah-00001",
    "receptor_ids" : []    
}
"""


def mid_invalidator_fn(o: ReleaseResourcesRequest):
    # function to make a valid MID AssignedResourcesRequest invalid
    o.subarray_id = -1


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ReleaseResourcesRequestSchema,
            VALID_MID_FULL_RELEASE_OBJECT,
            mid_invalidator_fn,
            VALID_MID_FULL_RELEASE_JSON,
            INVALID_MID_FULL_RELEASE_JSON,
            True,
        ),
        (
            ReleaseResourcesRequestSchema,
            VALID_MID_PARTIAL_RELEASE_OBJECT,
            None,
            VALID_MID_PARTIAL_RELEASE_JSON,
            None,
            True,
        ),
        (
            ReleaseResourcesRequestSchema,
            VALID_LOW_FULL_RELEASE_OBJECT,
            None,
            VALID_LOW_FULL_RELEASE_JSON,
            None,
            True,
        ),
    ],
)
def test_releaseresources_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json, is_validate
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json, is_validate
    )
