"""
Unit tests for ska_tmc_cdm.schemas module.
"""

import pytest

from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.utils import assert_json_is_equal

VALID_MID_PARTIAL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "transaction_id": "txn-blah-blah-00001",
    "subarray_id": 1, 
    "receptor_ids": ["0001", "0002"],
    "sdp_id": "sbi-mvp01-20220919-00001",
    "sdp_max_length" : 125.40
}
"""

VALID_MID_PARTIAL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    transaction_id="txn-blah-blah-00001",
    subarray_id=1,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
    sdp_id="sbi-mvp01-20220919-00001",
    sdp_max_length=125.40,
)

VALID_MID_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-tmc-releaseresources/2.0",
    "subarray_id": 1,
    "release_all": true,
    "sdp_id": "sbi-mvp01-20220919-00001",
    "sdp_max_length" : 125.40
}
"""

VALID_MID_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
    sdp_id="sbi-mvp01-20220919-00001",
    sdp_max_length=125.40,
)

# mixed partial / full request, used to test which params are ignored
VALID_MID_MIXED_ARGS_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
    dish_allocation=DishAllocation(receptor_ids=["0001", "0002"]),
    sdp_id="sbi-mvp01-20220919-00001",
    sdp_max_length=125.40,
)

VALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    "subarray_id": 1,
    "release_all": true,
    "sdp_id": "sbi-mvp01-20220919-00001",
    "sdp_max_length" : 125.40
}
"""

VALID_LOW_FULL_RELEASE_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    subarray_id=1,
    release_all=True,
    sdp_id="sbi-mvp01-20220919-00001",
    sdp_max_length=125.40,
)

INVALID_LOW_FULL_RELEASE_JSON = """
{
    "interface": "https://schema.skao.int/ska-low-tmc-releaseresources/2.0",
    "subarray_id": -1,
    "release_all": true,
    "sdp_id": "sbi-mvp01-20220919-00001",
    "sdp_max_length" : 125.40
}
"""


def low_invalidator_fn(o: ReleaseResourcesRequest):
    # function to make a valid LOW AssignedResourcesRequest invalid
    o.subarray_id = -1


@pytest.mark.parametrize(
    "instance,valid_json",
    [
        (
            VALID_MID_FULL_RELEASE_OBJECT,
            VALID_MID_FULL_RELEASE_JSON,
        ),  # no validation for MID
        (
            VALID_MID_PARTIAL_RELEASE_OBJECT,
            VALID_MID_PARTIAL_RELEASE_JSON,
        ),  # no validation for MID
        (
            VALID_MID_MIXED_ARGS_OBJECT,
            VALID_MID_FULL_RELEASE_JSON,  # expect partial spec to be ignored
        ),  # no validation for MID
        (VALID_LOW_FULL_RELEASE_OBJECT, VALID_LOW_FULL_RELEASE_JSON),
    ],
)
def test_releaseresources_serialisation_and_validation(instance, valid_json):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """

    marshalled = CODEC.dumps(instance)
    assert_json_is_equal(marshalled, valid_json)
