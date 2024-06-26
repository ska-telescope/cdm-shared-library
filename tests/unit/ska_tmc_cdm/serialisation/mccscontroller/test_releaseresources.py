"""
Unit tests for ska_tmc_cdm.schemas.mccscontroller.releaseresources module.
"""

import pytest

from ska_tmc_cdm.messages.mccscontroller.releaseresources import (
    ReleaseResourcesRequest,
)

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


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json",
    [
        (
            ReleaseResourcesRequest,
            VALID_OBJECT,
            lambda o: setattr(o, "subarray_id", -1),
            VALID_JSON,
            INVALID_JSON,
        )
    ],
)
def test_releaseresources_serialisation_and_validation(
    model_class, instance, modifier_fn, valid_json, invalid_json
):
    """
    Verifies that ReleaseResourcesRequest marshals, unmarshals, and
    validates correctly.
    """
    utils.test_serialisation_and_validation(
        model_class, instance, modifier_fn, valid_json, invalid_json
    )
