"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.mccs module.
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    MCCSConfigurationBuilder,
    SubarrayBeamConfigurationBuilder,
)

beams_configuration = SubarrayBeamConfigurationBuilder(subarray_beam_id=1)


beams_configuration_after_value_changed = SubarrayBeamConfigurationBuilder(
    subarray_beam_id=2
)


@pytest.mark.parametrize(
    "subarray_beam_ska_coordinates_1, subarray_beam_ska_coordinates_2, is_equal",
    [
        (
            MCCSConfigurationBuilder(
                subarray_beam_configs=[beams_configuration]
            ),
            MCCSConfigurationBuilder(
                subarray_beam_configs=[beams_configuration]
            ),
            True,
        ),
        (
            MCCSConfigurationBuilder(
                subarray_beam_configs=[beams_configuration]
            ),
            MCCSConfigurationBuilder(
                subarray_beam_configs=[beams_configuration_after_value_changed]
            ),
            False,
        ),
    ],
)
def test_subarray_beam_ska_coordinates_equality(
    subarray_beam_ska_coordinates_1: MCCSConfiguration,
    subarray_beam_ska_coordinates_2: MCCSConfiguration,
    is_equal: bool,
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
