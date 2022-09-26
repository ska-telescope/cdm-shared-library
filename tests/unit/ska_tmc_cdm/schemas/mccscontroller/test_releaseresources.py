"""
Unit tests for ska_tmc_cdm.schemas.mccscontroller.releaseresources module.
"""

import pytest

from ska_tmc_cdm.messages.mccscontroller.releaseresources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.mccscontroller.releaseresources import (
    ReleaseResourcesRequestSchema,
)
from ska_tmc_cdm.utils import assert_json_is_equal

from .. import utils

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": 1,
  "release_all": true
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": -1,
  "release_all": true
}
"""

VALID_OBJECT = ReleaseResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
    subarray_id=1,
    release_all=True,
)

VALID_JSON_EXPAND_CONTRACT = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": 1,
  "release_all": true,
  "subarray_beam_ids":[1],
  "channels":[[1, 2]]
}
"""

INVALID_JSON_EXPAND_CONTRACT = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
  "subarray_id": -1,
  "release_all": true,
  "subarray_beam_ids":[1],
  "channels":[[1, 2]]
}
"""

VALID_OBJECT_EXPAND_CONTRACT = ReleaseResourcesRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-releaseresources/1.0",
    subarray_id=1,
    release_all=True,
    subarray_beam_ids=[1],
    channels=[[1, 2]],
)


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ReleaseResourcesRequestSchema,
            VALID_OBJECT,
            lambda o: setattr(o, "subarray_id", -1),
            VALID_JSON,
            INVALID_JSON,
        )
    ],
)
def test_releaseresources_serialisation_and_validation(
    schema_cls, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ReleaseResourcesRequestSchema marshals, unmarshals, and
    validates correctly.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls, instance, modifier_fn, valid_json, invalid_json
    )


@pytest.mark.parametrize(
    "instance,valid_json",
    [
        (
            VALID_OBJECT,
            VALID_JSON,
        )
    ],
)
def test_releaseresources_serialisation_and_validation_with_expand_contract(
    instance, valid_json
):
    """
    Verifies that ReleaseResourcesRequestSchema marshals, unmarshals, and
    validates correctly.
    """
    marshalled = CODEC.dumps(instance)
    assert_json_is_equal(marshalled, valid_json)
