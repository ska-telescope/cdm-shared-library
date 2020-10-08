"""
Unit tests for the ska.cdm.subarray_node.configure.tmc module.
"""
import copy
from datetime import timedelta

from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska.cdm.schemas.subarray_node.configure.tmc import TMCConfigurationSchema
from ska.cdm.utils import json_is_equal

VALID_TMCCONFIGURATION_JSON = """
{
  "scanDuration": 123.45 
}
"""


def test_marshall_tmconfiguration_to_json():
    """
    Verify that TMCConfiguration is marshalled to JSON correctly.
    """
    dt = timedelta(seconds=123.45)
    config = TMCConfiguration(scan_duration=dt)
    expected = VALID_TMCCONFIGURATION_JSON
    json_str = TMCConfigurationSchema().dumps(config)
    assert json_is_equal(json_str, expected)


def test_unmarshall_tmconfiguration_from_json():
    """
    Verify that a TMCConfiguration is unmarshalled correctly from JSON.
    """
    dt = timedelta(seconds=123.45)
    expected = TMCConfiguration(scan_duration=dt)
    unmarshalled = TMCConfigurationSchema().loads(VALID_TMCCONFIGURATION_JSON)
    assert unmarshalled == expected


def test_marshall_tmcconfiguration_does_not_modify_original():
    """
    Verify that serialising a DishConfiguration does not change the object.
    """
    dt = timedelta(seconds=123.45)
    config = TMCConfiguration(scan_duration=dt)
    original_config = copy.deepcopy(config)
    TMCConfigurationSchema().dumps(config)
    assert config == original_config
