"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.sdp module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.sdp import SDPConfigurationBuilder


@pytest.mark.parametrize(
    "sdp_config_a,sdp_config_b,is_equal",
    [
        (
            SDPConfigurationBuilder().set_scan_type("calibration_A").build(),
            SDPConfigurationBuilder().set_scan_type("calibration_A").build(),
            True,
        ),
        (
            SDPConfigurationBuilder().set_scan_type("calibration_A").build(),
            SDPConfigurationBuilder().set_scan_type("calibration_B").build(),
            False,
        ),
    ],
)
def test_sdp_configuration_equality(sdp_config_a, sdp_config_b, is_equal):
    """
    Verify that SDP configuration objects are equal when they have the same value, not equal for different value
    And that SDP configuration objects are not considered equal to objects of
    other types.
    """
    assert (sdp_config_a == sdp_config_b) == is_equal
    assert sdp_config_a != 1
    assert sdp_config_b != object
