"""
Unit tests for ska_tmc_cdm.schemas.mccscontroller.allocate module.
"""

import pytest

from ska_tmc_cdm.messages.mccscontroller.allocate import AllocateRequest
from tests.unit.ska_tmc_cdm.serialisation import serialisation_utils as utils

VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
  "subarray_id": 1,
  "subarray_beam_ids": [1],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

INVALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
  "subarray_id": 1,
  "subarray_beam_ids": [49],
  "station_ids": [[1,2]],
  "channel_blocks": [3]
}
"""

VALID_OBJECT = AllocateRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-assignresources/1.0",
    subarray_id=1,
    subarray_beam_ids=[1],
    station_ids=[[1, 2]],
    channel_blocks=[3],
)


def invalidator_fn(o: AllocateRequest):
    # function to make a valid AllocateRequest invalid
    o.subarray_beam_ids = [49]


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            AllocateRequest,
            VALID_OBJECT,
            invalidator_fn,
            VALID_JSON,
            INVALID_JSON,
        ),
    ],
)
def test_releaseresources_serialisation_and_validation(
    model_class, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_serialisation_and_validation(
        model_class, instance, modifier_fn, valid_json, invalid_json
    )
