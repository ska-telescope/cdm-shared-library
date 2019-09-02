"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.csp module.
"""
from ska.cdm.messages.subarray_node.configure import FSPConfiguration, FSPFunctionMode
from ska.cdm.schemas.subarray_node.configure import FSPConfigurationSchema


def test_marshall_fsp_configuration_with_null_channel_averaging_map():
    """
    Verify that the ChannelAveragingMap FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert 'channelAveragingMap' not in marshalled
