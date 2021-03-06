"""
Unit tests for the ska.cdm.messages.subarray_node.configure.sdp module.
"""
from ska.cdm.messages.subarray_node.configure.sdp import SDPConfiguration


def test_sdp_configuration_equals():
    """
    Verify that SDP configuration objects are equal when they have the same value
    """
    sdp_config_a = SDPConfiguration('calibration_A')
    sdp_config_b = SDPConfiguration('calibration_A')

    assert sdp_config_a == sdp_config_b

    assert sdp_config_a != SDPConfiguration('science_B')
    assert sdp_config_b != SDPConfiguration('science_B')


def test_sdp_config_not_equal_to_other_objects():
    """
    Verify that SDP configuration objects are not considered equal to objects of
    other types.
    """
    sdp_config = SDPConfiguration('calibration_A')
    assert sdp_config != 1
