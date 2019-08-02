"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.common module.
"""
import ska.cdm.messages.subarray_node as sn
import ska.cdm.schemas.subarray_node.configure as schemas
from ...utils import json_is_equal

VALID_TARGET_JSON = """
{
  "RA": "12:34:56.78", 
  "dec": "+12:34:56.78", 
  "system": "ICRS", 
  "name": "NGC123"
}
"""

VALID_DISH_CONFIGURATION_JSON = '{"receiverBand": "5a"}'


def test_marshall_target_to_json():
    """
    Verify that PointingConfiguration Target is marshalled to JSON correctly.
    """
    target = sn.Target(ra='12h34m56.78s', dec='+12d34m56.78s', name='NGC123')
    expected = VALID_TARGET_JSON
    json_str = schemas.TargetSchema().dumps(target)
    assert json_is_equal(json_str, expected)


def test_unmarshall_target_from_json():
    """
    Verify that a Target is unmarshalled correctly from JSON.
    """
    expected = sn.Target(ra='12h34m56.78s', dec='+12d34m56.78s', name='NGC123')
    unmarshalled = schemas.TargetSchema().loads(VALID_TARGET_JSON)
    assert unmarshalled == expected


def test_marshall_dish_configuration_to_json():
    """
    Verify that DishConfiguration is marshalled to JSON correctly.
    """
    config = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_5A)
    json_str = schemas.DishConfigurationSchema().dumps(config)
    assert json_str == VALID_DISH_CONFIGURATION_JSON


def test_unmarshall_dish_configuration_from_json():
    """
    Verify that JSON can be unmarshalled to a DishConfiguration
    """
    expected = sn.DishConfiguration(receiver_band=sn.ReceiverBand.BAND_5A)
    unmarshalled = schemas.DishConfigurationSchema().loads(VALID_DISH_CONFIGURATION_JSON)
    assert unmarshalled == expected
