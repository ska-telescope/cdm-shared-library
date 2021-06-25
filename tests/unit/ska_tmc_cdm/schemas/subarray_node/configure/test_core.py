"""
Unit tests for the ska_tmc_cdm.subarray_node.configure.common module.
"""
import copy

from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    ReceiverBand,
    Target,
)
from ska_tmc_cdm.schemas.subarray_node.configure import (
    DishConfigurationSchema,
    TargetSchema,
)
from ska_tmc_cdm.utils import json_is_equal

VALID_TARGET_JSON = """
{
  "RA": "12:34:56.78",
  "dec": "+12:34:56.78",
  "system": "ICRS",
  "name": "NGC123"
}
"""

VALID_DISH_CONFIGURATION_JSON = '{"receiver_band": "5a"}'


def test_marshall_target_to_json():
    """
    Verify that PointingConfiguration Target is marshalled to JSON correctly.
    """
    target = Target(ra="12h34m56.78s", dec="+12d34m56.78s", name="NGC123")
    expected = VALID_TARGET_JSON
    json_str = TargetSchema().dumps(target)
    assert json_is_equal(json_str, expected)


def test_unmarshall_target_from_json():
    """
    Verify that a Target is unmarshalled correctly from JSON.
    """
    expected = Target(ra="12h34m56.78s", dec="+12d34m56.78s", name="NGC123")
    unmarshalled = TargetSchema().loads(VALID_TARGET_JSON)
    assert unmarshalled == expected


def test_marshall_dish_configuration_to_json():
    """
    Verify that DishConfiguration is marshalled to JSON correctly.
    """
    config = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    json_str = DishConfigurationSchema().dumps(config)
    assert json_str == VALID_DISH_CONFIGURATION_JSON


def test_unmarshall_dish_configuration_from_json():
    """
    Verify that JSON can be unmarshalled to a DishConfiguration
    """
    expected = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    unmarshalled = DishConfigurationSchema().loads(VALID_DISH_CONFIGURATION_JSON)
    assert unmarshalled == expected


def test_marshall_dish_configuration_does_not_modify_original():
    """
    Verify that serialising a DishConfiguration does not change the object.
    """
    config = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    original_config = copy.deepcopy(config)
    DishConfigurationSchema().dumps(config)
    assert config == original_config
