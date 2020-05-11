"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.csp module.
"""
import copy

from ska.cdm.messages.subarray_node.configure import CSPConfiguration, FSPConfiguration, FSPFunctionMode
from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.schemas.subarray_node.configure import CSPConfigurationSchema, FSPConfigurationSchema


def test_marshall_fsp_configuration_with_null_channel_averaging_map():
    """
    Verify that the ChannelAveragingMap FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert 'channelAveragingMap' not in marshalled


def test_marshall_cspconfiguration_does_not_modify_original():
    """
    Verify that serialising a CspConfiguration does not change the object.
    """
    config = CSPConfiguration(
        'csp ID goes here',
        ReceiverBand.BAND_5A,
        [FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)]
    )
    original_config = copy.deepcopy(config)
    CSPConfigurationSchema().dumps(config)
    assert config == original_config
