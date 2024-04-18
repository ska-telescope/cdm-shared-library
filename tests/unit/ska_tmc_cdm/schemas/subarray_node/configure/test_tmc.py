"""
Unit tests for the ska_tmc_cdm.subarray_node.configure.tmc module.
"""
import copy
from datetime import timedelta

import pytest

from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska_tmc_cdm.schemas.subarray_node.configure.tmc import (
    TMCConfigurationSchema,
)

from ... import utils

VALID_JSON = """
{
  "scan_duration": 123.45
}
"""

VALID_OBJECT = TMCConfiguration(scan_duration=timedelta(seconds=123.45))


def test_marshall_tmcconfiguration_does_not_modify_original():
    """
    Verify that serialising a TMCConfiguration does not change the object.
    """
    dt = timedelta(seconds=123.45)
    config = TMCConfiguration(scan_duration=dt)
    original_config = copy.deepcopy(config)
    TMCConfigurationSchema().dumps(config)
    assert config == original_config


@pytest.mark.parametrize(
    "schema_cls,instance,modifier_fn,valid_json,invalid_json",
    [
        (TMCConfigurationSchema, VALID_OBJECT, None, VALID_JSON, None),
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
