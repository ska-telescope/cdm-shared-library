"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.common module.
"""

from typing import NamedTuple, Optional

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    FK5Target,
    PointingConfiguration,
    ReceiverBand,
    Target,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import (
    PointingConfigurationBuilder,
    TargetBuilder,
)


def test_target_defaults():
    """
    Verify Target default arguments.
    """
    target_1 = Target(ra=1, dec=0.5)
    target_2 = Target(
        ra=1,
        dec=0.5,
        target_name="",
        reference_frame="icrs",
        unit=("hourangle", "deg"),
    )
    assert target_1 == target_2


TARGET_EQ_CASES = (
    (
        FK5Target(
            ra=1,
            dec=2,
            target_name="a source",
            reference_frame="fk5",
            unit="deg",
        ),
        FK5Target(
            ra=1,
            dec=2,
            target_name="a source",
            reference_frame="fk5",
            unit="deg",
        ),
        True,
    ),
    (
        Target(ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        Target(ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        True,
    ),
    (
        Target(
            target_name="target A", ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1
        ),
        Target(
            target_name="target B", ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1
        ),
        False,
    ),
    (
        Target(ra=2, dec=1, ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        Target(ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        False,
    ),
    (
        Target(ra=1, dec=1),
        FK5Target(
            ra=1,
            dec=2,
            target_name="a source",
            reference_frame="fk5",
            unit="deg",
        ),
        False,
    ),
    (
        Target(ra=1, dec=1, ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        Target(ra=1, dec=1),
        False,
    ),
    (
        Target(ra=1, dec=1, ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        Target(ra=1, dec=1, ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        True,
    ),
    (
        Target(ra=1, dec=1, ca_offset_arcsec=-1.1, ie_offset_arcsec=1.1),
        Target(
            ra=1,
            dec=1,
            ca_offset_arcsec=-1.10000000000000000000000001,
            ie_offset_arcsec=1.09999999999999999999999999,
        ),
        True,
    ),
    (
        Target(ra=1, dec=1),
        object(),
        False,
    ),
)


@pytest.mark.parametrize(("targetA, targetB, expected_equal"), TARGET_EQ_CASES)
def test_target_eq(targetA, targetB, expected_equal):
    """
    Verify that Target objects are considered equal when:

      - they have the same target name
      - they point to the same place on the sky
      - they use the same co-ordinate reference frame
      - they use the same co-ordinate units
      - they have the same offset parameters
    """
    if expected_equal:
        assert targetA == targetB
    else:
        assert targetA != targetB


class ValidationCase(NamedTuple):
    args: dict
    expected_error: Optional[Exception]


TARGET_VALIDATION_CASES = (
    ValidationCase(
        args={},
        expected_error=ValueError,
    ),
    ValidationCase(
        args={"ra": 10, "dec": -50},
        expected_error=None,
    ),
    ValidationCase(
        args={
            "ra": 1,
            "dec": 2,
            "target_name": "a source",
            "reference_frame": "fk5",
            "unit": "deg",
        },
        # error expected because this tries to set an ICRS target to FK5
        # reference frame
        expected_error=ValidationError,
    ),
    ValidationCase(
        args={"ca_offset_arcsec": -1, "ie_offset_arcsec": 1},
        expected_error=None,
    ),
    ValidationCase(
        args={"ra": 0, "dec": 0},
        expected_error=None,
    ),
    ValidationCase(
        args={"ra": 0, "dec": 10},
        expected_error=None,
    ),
    ValidationCase(
        args={
            "ra": None,
            "dec": None,
            "ca_offset_arcsec": 0,
            "ie_offset_arcsec": 0,
        },
        expected_error=ValueError,
    ),
    ValidationCase(
        args={"ra": 5, "dec": None},
        expected_error=ValueError,
    ),
    ValidationCase(
        args={"ra": None, "dec": 0},
        expected_error=ValueError,
    ),
)


@pytest.mark.parametrize(("args, expected_error"), TARGET_VALIDATION_CASES)
def test_target_validation(args, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            Target(**args)
    else:
        Target(**args)


def test_target_repr():
    """
    Verify the repr representation of a Target.
    """
    target = Target(
        ra=30.0,
        dec=-3600.0,
        target_name="target name",
        reference_frame="icrs",
        unit=("deg", "arcsec"),
    )
    expected = "ICRSTarget(ra=np.float64(30.0), dec=np.float64(-1.0), target_name='target name', reference_frame='icrs', unit=('deg', 'deg'), ca_offset_arcsec=0.0, ie_offset_arcsec=0.0)"
    assert expected == repr(target)


def test_target_str():
    """
    Verify the string representation of a Target.
    """
    target = Target(
        ra=30,
        dec="0",
        target_name="target name",
        reference_frame="icrs",
        unit=("deg", "rad"),
    )
    expected = "<Target: 'target name' (02h00m00s +00d00m00s icrs)>"
    assert expected == str(target)


def test_pointing_configuration_eq():
    """
    Verify that PointingConfiguration objects are considered equal when:
      - they point to the same target
    """
    target_1 = TargetBuilder(target_name="a source")
    target_2 = TargetBuilder(target_name="a source")
    target_3 = TargetBuilder(target_name="foobar")

    config_1 = PointingConfiguration(target=target_1)
    config_2 = PointingConfiguration(target=target_2)
    config_3 = PointingConfiguration(target=target_3)
    assert config_1 == config_2
    assert config_1 != config_3


def test_pointing_configuration_is_not_equal_to_other_objects():
    """
    Verify that PointingConfiguration is not considered equal to
    non-PointingConfiguration objects.
    """
    config = PointingConfigurationBuilder()
    assert config != object


def test_dish_configuration_eq():
    """
    Verify that DishConfiguration objects are considered equal when:
      - they use the same receiver band
    """
    config_1 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    config_2 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    config_3 = DishConfiguration(receiver_band=ReceiverBand.BAND_2)
    assert config_1 == config_2
    assert config_1 != config_3


def test_dish_configuration_is_not_equal_to_other_objects():
    """
    Verify that DishConfiguration is considered unequal to
    non-DishConfiguration objects.
    """
    config_1 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    assert config_1 != TargetBuilder()
    assert config_1 != object
