"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas.central_node.release_resources import ReleaseResourcesRequestSchema
from .. import utils

VALID_MID_PARTIAL_RELEASE_JSON = """
{
     "subarrayID": 1,
     "dish": {"receptorIDList": ["0001", "0002"]}
}
"""

VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"])
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "subarrayID": 1,
    "releaseALL": true
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    subarray_id=1,
    release_all=True
)

# mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    subarray_id=1,
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"])
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": 1,
    "release_all": true
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    subarray_id=1,
    release_all=True
)

INVALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skatelescope.org/ska-low-tmc-releaseresources/1.0",
    "subarray_id": -1,
    "release_all": true
}
"""


def low_invalidator_fn(o: ReleaseResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.subarray_id = -1


@pytest.mark.xfail(reason="The Telescope Model library is not updated with ADR-35 hence, JSON schema validation will "
                          "be failed")
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
