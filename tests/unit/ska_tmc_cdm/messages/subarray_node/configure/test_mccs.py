"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.mccs module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    SubarrayBeamSkyCoordinatesBuilder,
)


@pytest.mark.parametrize(
    "subarray_beam_ska_coordinates_1, subarray_beam_ska_coordinates_2, is_equal",
    [
        (
            SubarrayBeamSkyCoordinatesBuilder()
            .set_timestamp("value")
            .set_reference_frame("HORIZON")
            .set_c1(180.0)
            .set_c1_rate(0.0)
            .set_c2(90.0)
            .set_c2_rate(0.0)
            .build(),
            SubarrayBeamSkyCoordinatesBuilder()
            .set_timestamp("value")
            .set_reference_frame("HORIZON")
            .set_c1(180.0)
            .set_c1_rate(0.0)
            .set_c2(90.0)
            .set_c2_rate(0.0)
            .build(),
            True,
        ),
        (
            SubarrayBeamSkyCoordinatesBuilder()
            .set_timestamp("value")
            .set_reference_frame("HORIZON")
            .set_c1(180.0)
            .set_c1_rate(0.0)
            .set_c2(90.0)
            .set_c2_rate(0.0)
            .build(),
            SubarrayBeamSkyCoordinatesBuilder()
            .set_timestamp("value")
            .set_reference_frame("frame")
            .set_c1(180.0)
            .set_c1_rate(0.0)
            .set_c2(80.0)
            .set_c2_rate(0.0)
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
