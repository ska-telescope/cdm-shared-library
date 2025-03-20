"""
Unit tests for the ska_tmc_cdm.subarray_node.configure.common module.
"""
import json
from typing import NamedTuple, Optional

import pytest
from pydantic import ValidationError

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


class TargetCase(NamedTuple):
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
    TargetCase(
        Target(ra="12h34m56.78s", dec="+12d34m56.78s", target_name="NGC123"),
        VALID_TARGET_JSON,
    ),
    TargetCase(
        Target(
            ra="12h34m56.78s",
            dec="+12d34m56.78s",
            target_name="NGC123",
            ca_offset_arcsec=0,  # Zero offsets omitted from output....
            ie_offset_arcsec=0,
        ),
        VALID_TARGET_JSON,
    ),
    TargetCase(
        Target(
            ra="12h34m56.78s",
            dec="+12d34m56.78s",
            target_name="NGC123",
            ca_offset_arcsec=25.0,
            ie_offset_arcsec=-25.0,
        ),
        OFFSET_TARGET_JSON,
    ),
    TargetCase(
        SpecialTarget(target_name=SolarSystemObject.SUN),
        NON_SIDEREAL_TARGET_JSON,
    ),
)


class WrapSectorCase(NamedTuple):
    wrap_sector: Optional[int]
    json: str


VALID_WRAP_SECTOR_JSON_PAIRS = (
    WrapSectorCase(0, '{"wrap_sector": 0}'),
    WrapSectorCase(-1, '{"wrap_sector": -1}'),
    WrapSectorCase(None, "{}"),
)

INVALID_WRAP_SECTOR_JSON_PAIRS = (
    WrapSectorCase(-2, '{"wrap_sector": -2}'),
    WrapSectorCase(2, '{"wrap_sector": 2}'),
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


@pytest.mark.parametrize(
    "wrap_sector,jsonable_dict", VALID_WRAP_SECTOR_JSON_PAIRS
)
def test_marshall_pointing_configuration_with_wrap_sector_to_json(
    wrap_sector, jsonable_dict
):
    """
    Verify that the wrap_sector attribute in the PointingParameters marshals correctly
    to JSON
    """

    pointing_configuration = PointingConfiguration(wrap_sector=wrap_sector)
    json_str = CODEC.dumps(pointing_configuration)
    assert json_str == jsonable_dict


@pytest.mark.parametrize("wrap_sector", INVALID_WRAP_SECTOR_JSON_PAIRS)
def test_marshall_pointing_configuration_with_invalid_wrap_sector_fails(
    wrap_sector,
):
    """
    Verify it's not possible to set the wrap_sector attribute to a value other than 0 and -1
    """

    with pytest.raises(ValidationError):
        pointing_configuration = PointingConfiguration(wrap_sector=wrap_sector)
        CODEC.dumps(pointing_configuration)


def test_marshall_pointing_configuration_with_wrap_sector_eq_none_to_json():
    """
    Verify that wrap_sector attribute in the PointingParameters marshals correctly
    to JSON when set to None. This should result in wrap_sector being omitted from the resulting JSON.
    """

    target = SpecialTarget(target_name=SolarSystemObject.SUN)
    pointing_configuration = PointingConfiguration(
        target=target, wrap_sector=None
    )

    json_str = CODEC.dumps(pointing_configuration)
    assert (
        json_str
        == '{"target": {"reference_frame": "special", "target_name": "Sun"}}'
    )


def test_unmarshall_pointing_configuration_json_with_wrap_sector_eq_none_to_instance():
    """
    Verify that if the wrap_sector attribute is not set in the JSON, it will
    be set to None when unmarshalling to a PointingConfiguration instance
    """

    target_json = (
        '{"target": {"reference_frame": "special", "target_name": "Sun"}}'
    )
    assert CODEC.loads(PointingConfiguration, target_json).wrap_sector is None
