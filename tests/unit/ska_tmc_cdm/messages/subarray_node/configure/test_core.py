"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.common module.
"""

from typing import NamedTuple, Optional, Type

import pytest

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import (
    DishConfigurationBuilder,
    PointingConfigurationBuilder,
    TargetBuilder,
)


def test_target_defaults():
    """
    Verify Target default arguments using TargetBuilder.
    """
    target_1 = TargetBuilder().set_ra(1).set_dec(0.5).build()

    target_2 = (
        TargetBuilder()
        .set_ra(1)
        .set_dec(0.5)
        .set_target_name("")
        .set_reference_frame("icrs")
        .set_unit(("hourangle", "deg"))
        .build()
    )

    assert target_1 == target_2


TARGET_EQ_CASES = [
    (
        TargetBuilder()
        .set_ra(1)
        .set_dec(2)
        .set_target_name("a source")
        .set_reference_frame("fk5")
        .set_unit(("deg", "deg"))
        .build(),
        TargetBuilder()
        .set_ra(1)
        .set_dec(2)
        .set_target_name("a source")
        .set_reference_frame("fk5")
        .set_unit(("deg", "deg"))
        .build(),
        True,
    ),
    (
        TargetBuilder()
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder()
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        True,
    ),
    (
        TargetBuilder()
        .set_target_name("target A")
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder()
        .set_target_name("target B")
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        False,
    ),
    (
        TargetBuilder()
        .set_ra(2)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder()
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        False,
    ),
    (
        TargetBuilder().set_ra(1).set_dec(1).build(),
        TargetBuilder()
        .set_ra(1)
        .set_dec(2)
        .set_target_name("a source")
        .set_reference_frame("fk5")
        .set_unit(("deg", "deg"))
        .build(),
        False,
    ),
    (
        TargetBuilder()
        .set_ra(1)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder().set_ra(1).set_dec(1).build(),
        False,
    ),
    (
        TargetBuilder()
        .set_ra(1)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder()
        .set_ra(1)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        True,
    ),
    (
        TargetBuilder()
        .set_ra(1)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.1)
        .set_ie_offset_arcsec(1.1)
        .build(),
        TargetBuilder()
        .set_ra(1)
        .set_dec(1)
        .set_ca_offset_arcsec(-1.10000000000000000000000001)
        .set_ie_offset_arcsec(1.09999999999999999999999999)
        .build(),
        True,
    ),
    (
        TargetBuilder().set_ra(1).set_dec(1).build(),
        object(),
        False,
    ),
]


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
    builder: TargetBuilder
    expected_error: Optional[Type[Exception]]


# Create instances of TargetBuilder for each test case directly.
TARGET_VALIDATION_CASES = [
    ValidationCase(
        builder=TargetBuilder(),
        expected_error=ValueError,
    ),
    ValidationCase(
        builder=TargetBuilder().set_ra(10).set_dec(-50),
        expected_error=None,
    ),
    ValidationCase(
        builder=TargetBuilder()
        .set_ra(1)
        .set_dec(2)
        .set_target_name("a source")
        .set_reference_frame("fk5")
        .set_unit(("deg", "deg")),
        expected_error=None,
    ),
    ValidationCase(
        builder=TargetBuilder()
        .set_ca_offset_arcsec(-1)
        .set_ie_offset_arcsec(1),
        expected_error=None,
    ),
    ValidationCase(
        builder=TargetBuilder()
        .set_ca_offset_arcsec(0)
        .set_ie_offset_arcsec(0),
        expected_error=ValueError,
    ),
    ValidationCase(
        builder=TargetBuilder().set_ra(5),  # no dec error
        expected_error=TypeError,
    ),
]


@pytest.mark.parametrize("case", TARGET_VALIDATION_CASES)
def test_target_validation(case: ValidationCase):
    """
    Verify that Target objects are validated correctly.
    """
    if case.expected_error:
        with pytest.raises(case.expected_error):
            case.builder.build()
    else:
        assert case.builder.build() is not None


def test_target_repr():
    """
    Verify the repr representation of a Target using TargetBuilder in one line.
    """
    target = (
        TargetBuilder()
        .set_ra(30)
        .set_dec(-3600)
        .set_target_name("target name")
        .set_reference_frame("icrs")
        .set_unit(("deg", "arcsec"))
        .build()
    )
    expected = "Target(ra=30.0, dec=-1.0, target_name='target name', reference_frame='icrs', unit=('deg', 'deg'), ca_offset_arcsec=0.0, ie_offset_arcsec=0.0)"
    assert expected == repr(target)


def test_target_str():
    """
    Verify the string representation of a Target using TargetBuilder in one line.
    """
    target = (
        TargetBuilder()
        .set_ra(30)
        .set_dec("0")
        .set_target_name("target name")
        .set_reference_frame("icrs")
        .set_unit(("deg", "rad"))
        .build()
    )
    expected = "<Target: 'target name' (02h00m00s +00d00m00s icrs)>"
    assert expected == str(target)


@pytest.mark.parametrize(
    "pointing_configuration_setup_1, pointing_configuration_setup_2, expected_equality",
    [
        (
            PointingConfigurationBuilder()
            .set_target(
                TargetBuilder()
                .set_ra(1)
                .set_dec(2)
                .set_target_name("a source")
                .set_reference_frame("fk5")
                .set_unit("deg")
                .build()
            )
            .build(),
            PointingConfigurationBuilder()
            .set_target(
                TargetBuilder()
                .set_ra(1)
                .set_dec(2)
                .set_target_name("a source")
                .set_reference_frame("fk5")
                .set_unit("deg")
                .build()
            )
            .build(),
            True,
        ),
        (
            PointingConfigurationBuilder()
            .set_target(
                TargetBuilder()
                .set_ra(1)
                .set_dec(2)
                .set_target_name("a source")
                .set_reference_frame("fk5")
                .set_unit("deg")
                .build()
            )
            .build(),
            PointingConfigurationBuilder()
            .set_target(
                TargetBuilder()
                .set_ra(1)
                .set_dec(2)
                .set_target_name("foobar")
                .set_reference_frame("fk4")
                .set_unit("deg")
                .build()
            )
            .build(),
            False,
        ),
    ],
)
def test_pointing_configuration_eq(
    pointing_configuration_setup_1,
    pointing_configuration_setup_2,
    expected_equality,
):
    """
    Verify that PointingConfiguration objects are considered equal when they point to the same target, not equal for different value
    And PointingConfiguration is not considered equal to
    non-PointingConfiguration objects.
    """
    assert (
        pointing_configuration_setup_1 == pointing_configuration_setup_2
    ) == expected_equality
    assert pointing_configuration_setup_1 != 1
    assert pointing_configuration_setup_1 != object


@pytest.mark.parametrize(
    "dish_configuration_setup_1, dish_configuration_setup_2, expected_equality",
    [
        (
            DishConfigurationBuilder()
            .set_receiver_band(ReceiverBand.BAND_1)
            .build(),
            DishConfigurationBuilder()
            .set_receiver_band(ReceiverBand.BAND_1)
            .build(),
            True,
        ),
        (
            DishConfigurationBuilder()
            .set_receiver_band(ReceiverBand.BAND_1)
            .build(),
            DishConfigurationBuilder()
            .set_receiver_band(ReceiverBand.BAND_2)
            .build(),
            False,
        ),
    ],
)
def test_dish_configuration_eq(
    dish_configuration_setup_1, dish_configuration_setup_2, expected_equality
):
    """
    Verify that DishConfiguration objects are considered equal when they use the same receiver band., not equal for different value
    And DishConfiguration is not considered equal to
    non-DishConfiguration objects.
    """
    assert (
        dish_configuration_setup_1 == dish_configuration_setup_2
    ) == expected_equality
    assert dish_configuration_setup_1 != 1
    assert dish_configuration_setup_1 != object
