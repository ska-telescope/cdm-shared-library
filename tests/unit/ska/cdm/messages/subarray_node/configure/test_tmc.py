"""
Unit tests for the ska.cdm.messages.subarray_node.configure.tmc module.
"""

from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration


def test_tmcconfiguration_equals():
    """
    Verify that TMCConfigurations are considered equal when all attributes are
    equal.
    """
    o = TMCConfiguration(scan_duration=1.23, is_ska_mid=True)
    assert o == TMCConfiguration(scan_duration=1.23, is_ska_mid=True)

    assert o != TMCConfiguration(scan_duration=4.56, is_ska_mid=True)
    assert o != TMCConfiguration(scan_duration=1.23, is_ska_mid=False)
