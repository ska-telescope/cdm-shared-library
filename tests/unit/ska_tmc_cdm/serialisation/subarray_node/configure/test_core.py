"""
Unit tests for the ska_tmc_cdm.subarray_node.configure.common module.
"""
import json
from typing import NamedTuple

import pytest

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    SolarSystemObject,
    SpecialTarget,
    Target,
    TargetUnion,
)
from tests.utils import assert_json_is_equal


class Case(NamedTuple):
    target: TargetUnion
    json: str


VALID_TARGET_JSON = {
    "ra": "12:34:56.78",
    "dec": "+12:34:56.78",
    "reference_frame": "ICRS",
    "target_name": "NGC123",
}


OFFSET_TARGET_JSON = {
    "ra": "12:34:56.78",
    "dec": "+12:34:56.78",
    "reference_frame": "ICRS",
    "target_name": "NGC123",
    "ca_offset_arcsec": 25.0,
    "ie_offset_arcsec": -25.0,
}


NON_SIDEREAL_TARGET_JSON = {"target_name": "Sun", "reference_frame": "special"}

VALID_DISH_CONFIGURATION_JSON = '{"receiver_band": "5a"}'

TARGET_PAIRS = (
    Case(
        Target(ra="12h34m56.78s", dec="+12d34m56.78s", target_name="NGC123"),
        VALID_TARGET_JSON,
    ),
    Case(
        Target(
            ra="12h34m56.78s",
            dec="+12d34m56.78s",
            target_name="NGC123",
            ca_offset_arcsec=0,  # Zero offsets omitted from output....
            ie_offset_arcsec=0,
        ),
        VALID_TARGET_JSON,
    ),
    Case(
        Target(
            ra="12h34m56.78s",
            dec="+12d34m56.78s",
            target_name="NGC123",
            ca_offset_arcsec=25.0,
            ie_offset_arcsec=-25.0,
        ),
        OFFSET_TARGET_JSON,
    ),
    Case(
        SpecialTarget(target_name=SolarSystemObject.SUN),
        NON_SIDEREAL_TARGET_JSON,
    ),
)


@pytest.mark.parametrize("target,expected", TARGET_PAIRS)
def test_marshall_target_to_json(target, expected):
    """
    Verify that PointingConfiguration Target is marshalled to JSON correctly.
    """
    json_str = CODEC.dumps(target)
    assert_json_is_equal(json_str, json.dumps(expected))


@pytest.mark.parametrize("target,jsonable_dict", TARGET_PAIRS)
def test_unmarshall_target_from_json(target, jsonable_dict):
    """
    Verify that a Target is unmarshalled correctly from JSON.
    """
    unmarshalled = CODEC.loads(target.__class__, json.dumps(jsonable_dict))
    assert unmarshalled == target


@pytest.mark.parametrize("target,jsonable_dict", TARGET_PAIRS)
def test_unmarshall_pointing_parameters(target, jsonable_dict):
    """
    Verify that PointingParameters unmarshall correctly from JSON
    and the right Target class is resolved.
    """
    pointing_configuration = PointingConfiguration(target=target)
    json_str = json.dumps({"target": jsonable_dict})
    unmarshalled = CODEC.loads(PointingConfiguration, json_str)
    assert unmarshalled == pointing_configuration


def test_marshall_dish_configuration_to_json():
    """
    Verify that DishConfiguration is marshalled to JSON correctly.
    """
    config = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    json_str = CODEC.dumps(config)
    assert json_str == VALID_DISH_CONFIGURATION_JSON


def test_unmarshall_dish_configuration_from_json():
    """
    Verify that JSON can be unmarshalled to a DishConfiguration
    """
    expected = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    unmarshalled = CODEC.loads(
        DishConfiguration, VALID_DISH_CONFIGURATION_JSON
    )
    assert unmarshalled == expected


def test_marshall_dish_configuration_does_not_modify_original():
    """
    Verify that serialising a DishConfiguration does not change the object.
    """
    config = DishConfiguration(receiver_band=ReceiverBand.BAND_5A)
    original_config = config.model_copy(deep=True)
    CODEC.dumps(config)
    assert config == original_config
