"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import (
    ReleaseResourcesRequest,
)

from tests.unit.ska_tmc_cdm.serialisation import serialisation_utils as utils


VALID_MID_PARTIAL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "transaction_id": "txn-blah-blah-00001",
    "subarray_id": 1,
    "release_all":false,
    "receptor_ids": ["SKA001", "SKA002"]
}
"""

VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    transaction_id="txn-blah-blah-00001",
    subarray_id=1,
    release_all=False,
    dish_allocation=DishAllocation(receptor_ids=["SKA001", "SKA002"]),
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.1",
    "subarray_id": 1,
    "transaction_id": "txn-blah-blah-00001",
    "release_all": true
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    subarray_id=1,
    transaction_id="txn-blah-blah-00001",
    release_all=True,
)

# # mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.1",
    subarray_id=1,
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=["SKA001", "SKA002"]),
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
    "transaction_id": "txn-blah-blah-00001"
}
"""


def mid_invalidator_fn(obj: ReleaseResourcesRequest):
    # function to make a valid MID AssignedResourcesRequest invalid
    obj.subarray_id = -1


@pytest.mark.parametrize(
    "cdm_class,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ReleaseResourcesRequest,
            VALID_MID_FULL_RELEASE_OBJECT,
            mid_invalidator_fn,
            VALID_MID_FULL_RELEASE_JSON,
            INVALID_MID_FULL_RELEASE_JSON,
        ),
        (
            ReleaseResourcesRequest,
            VALID_MID_PARTIAL_RELEASE_OBJECT,
            None,
            VALID_MID_PARTIAL_RELEASE_JSON,
            None,
        ),
        (
            ReleaseResourcesRequest,
            VALID_LOW_FULL_RELEASE_OBJECT,
            None,
            VALID_LOW_FULL_RELEASE_JSON,
            None,
        ),
    ],
)
def test_releaseresources_serialisation_and_validation(
    cdm_class, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_serialisation_and_validation(
        cdm_class,
        instance,
        modifier_fn,
        valid_json,
        invalid_json,
    )
