"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.mccs module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    MCCSConfigurationBuilder,
    SubarrayBeamApertureBuilder,
    SubarrayBeamConfigurationBuilder,
    SubarrayBeamLogicalbandsBuilder,
    SubarrayBeamSkyCoordinatesBuilder,
)

beams_configuration = SubarrayBeamConfigurationBuilder(
    subarray_beam_id=1,
    update_rate=1.0,
    logical_bands=SubarrayBeamLogicalbandsBuilder(
        start_channel=80,
        number_of_channels=16,
    ),
    apertures=SubarrayBeamApertureBuilder(
        aperture_id="AP001.01",
        weighting_key_ref="aperture2",
    ),
    sky_coordinates=SubarrayBeamSkyCoordinatesBuilder(
        reference_frame="HORIZON", c1=180.0, c2=90.0
    ),
)

beams_configuration_after_value_changed = (
    SubarrayBeamConfigurationBuilder()
    .set_subarray_beam_id(2)
    .set_update_rate(1.0)
    .set_logical_bands(
        SubarrayBeamLogicalbandsBuilder()
        .set_start_channel(80)
        .set_number_of_channels(16)
    )
    .set_apertures(
        SubarrayBeamApertureBuilder()
        .set_aperture_id("AP001.01")
        .set_weighting_key_ref("aperture2")
    )
    .set_sky_coordinates(
        SubarrayBeamSkyCoordinatesBuilder()
        .set_reference_frame("HORIZON")
        .set_c1(180.0)
        .set_c2(90.0)
    )
    .build()
)


@pytest.mark.parametrize(
    "subarray_beam_ska_coordinates_1, subarray_beam_ska_coordinates_2, is_equal",
    [
        (
            MCCSConfigurationBuilder()
            .set_subarray_beam_config(
                subarray_beam_configs=[beams_configuration]
            )
            .build(),
            MCCSConfigurationBuilder()
            .set_subarray_beam_config(
                subarray_beam_configs=[beams_configuration]
            )
            .build(),
            True,
        ),
        (
            MCCSConfigurationBuilder()
            .set_subarray_beam_config(
                subarray_beam_configs=[beams_configuration]
            )
            .build(),
            MCCSConfigurationBuilder()
            .set_subarray_beam_config(
                subarray_beam_configs=[beams_configuration_after_value_changed]
            )
            .build(),
            False,
        ),
    ],
)
def test_subarray_beam_ska_coordinates_equality(
    subarray_beam_ska_coordinates_1, subarray_beam_ska_coordinates_2, is_equal
):
    """
    Verify that SubarrayBeamTarget objects are equal when they have the same values, not equal for different value
    and not equal when any attribute differs.
    """
    assert (
        subarray_beam_ska_coordinates_1 == subarray_beam_ska_coordinates_2
    ) == is_equal
    assert subarray_beam_ska_coordinates_1 != 1
    assert subarray_beam_ska_coordinates_2 != object
