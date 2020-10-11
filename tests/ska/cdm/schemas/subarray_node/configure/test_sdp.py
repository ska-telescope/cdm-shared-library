"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.sdp module.
"""

from ska.cdm.messages.subarray_node.configure import SDPConfiguration
from ska.cdm.schemas.subarray_node.configure.sdp import SDPConfigurationSchema
from ska.cdm.utils import json_is_equal

VALID_SDP_SCAN_TYPE = '{"scan_type": "science_A"}'


def test_marshall_sdp_scan_type():
    """
    Verify that JSON can be marshalled to JSON correctly
    """
    scan_type = "science_A"
    sdp_configure = SDPConfiguration(scan_type)
    schema = SDPConfigurationSchema()
    result = schema.dumps(sdp_configure)

    assert json_is_equal(result, VALID_SDP_SCAN_TYPE)


def test_unmarshall_sdp_scan_type():
    """
    Verify that JSON can be unmarshalled to JSON correctly
    """
    schema = SDPConfigurationSchema()
    result = schema.loads(VALID_SDP_SCAN_TYPE)

    scan_type = "science_A"
    expected = SDPConfiguration(scan_type)

    assert isinstance(result.scan_type, str)
    assert expected == result
