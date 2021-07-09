"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.tmc module.
"""

from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration


def test_tmcconfiguration_equals():
    """
    Verify that TMCConfigurations are considered equal when all attributes are
    equal.
    """
    o = TMCConfiguration(scan_duration=1.23)
    assert o == TMCConfiguration(scan_duration=1.23)
    assert o != TMCConfiguration(scan_duration=4.56)
