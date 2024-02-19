"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.tmc module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.tmc import (
    TMCConfigurationBuilder,
)


@pytest.mark.parametrize(
    "tmc_config_a,tmc_config_b,is_equal",
    [
        (
            TMCConfigurationBuilder().set_scan_duration(1.23).build(),
            TMCConfigurationBuilder().set_scan_duration(1.23).build(),
            True,
        ),
        (
            TMCConfigurationBuilder().set_scan_duration(1.23).build(),
            TMCConfigurationBuilder().set_scan_duration(4.56).build(),
            False,
        ),
    ],
)
def test_tmc_configuration_equality(tmc_config_a, tmc_config_b, is_equal):
    """
    Verify that TMC configuration objects are equal when they have the same value,not equal for different value
    And that TMC configuration objects are not considered equal to objects of
    other types.
    """
    assert (tmc_config_a == tmc_config_b) == is_equal
    assert tmc_config_a != 1
    assert tmc_config_b != object
