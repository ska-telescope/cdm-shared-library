"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.csp module.
"""
import copy

from ska.cdm.messages.subarray_node.configure import CSPConfiguration, FSPConfiguration, FSPFunctionMode
from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.schemas.subarray_node.configure import CSPConfigurationSchema, FSPConfigurationSchema


def test_marshall_fsp_configuration_with_null_optional_parameters():
    """
    Verify that optional FSPConfiguration parameters are removed when null or
    not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    optional_fields = [field.data_key for name, field in schema.fields.items()
                       if field.required == False]
    for field in optional_fields:
        assert field not in marshalled


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
