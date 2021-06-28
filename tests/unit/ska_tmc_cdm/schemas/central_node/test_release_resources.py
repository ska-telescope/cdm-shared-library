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
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "transaction_id": "txn-blah-blah-00001",
    "subarray_id": 1, 
    "receptor_ids": ["0001", "0002"]
}
"""

VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    transaction_id="txn-blah-blah-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "subarray_id": 1,
    "release_all": true
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
)

# mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    "subarray_id": 1,
    "release_all": true
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
)

INVALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    "subarray_id": -1,
    "release_all": true
}
"""


def low_invalidator_fn(o: ReleaseResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.subarray_id = -1


# TODO remove xfail before merging AT2-855
@pytest.mark.xfail(reason="The Telescope Model library is not updated with "
                          "ADR-35 hence JSON schema validation will fail")
@pytest.mark.parametrize(
    'schema_cls,instance,modifier_fn,valid_json,invalid_json',
    [
        (ReleaseResourcesRequestSchema,
         VALID_MID_FULL_RELEASE_OBJECT,
         None,  # no validation for MID
         VALID_MID_FULL_RELEASE_JSON,
         None),  # no validation for MID
        (ReleaseResourcesRequestSchema,
         VALID_MID_PARTIAL_RELEASE_OBJECT,
         None,  # no validation for MID
         VALID_MID_PARTIAL_RELEASE_JSON,
         None),  # no validation for MID
        (ReleaseResourcesRequestSchema,
         VALID_MID_MIXED_ARGS_OBJECT,
         None,  # no validation for MID
         VALID_MID_FULL_RELEASE_JSON,  # expect partial spec to be ignored
         None),  # no validation for MID
        (ReleaseResourcesRequestSchema,
         VALID_LOW_FULL_RELEASE_OBJECT,
         low_invalidator_fn,
         VALID_LOW_FULL_RELEASE_JSON,
         INVALID_LOW_FULL_RELEASE_JSON),
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
