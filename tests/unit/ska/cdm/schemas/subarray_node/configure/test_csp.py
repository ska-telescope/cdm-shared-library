"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.csp module.
"""
import copy
import inspect

from ska.cdm.messages.subarray_node.configure.csp import (
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
)
from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.schemas.subarray_node.configure import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
)


def test_marshall_fsp_configuration_with_undefined_optional_parameters():
    """
    Verify that optional FSPConfiguration parameters are removed when they are
    left unset.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    optional_fields = [
        field.data_key
        for name, field in schema.fields.items()
        if field.required is False
    ]
    for field in optional_fields:
        assert field not in marshalled


def test_marshall_fsp_configuration_with_optional_parameters_as_none():
    """
    Verify that optional FSPConfiguration parameters are removed when None is
    passed in as their constructor value.
    """
    constructor_signature = inspect.signature(FSPConfiguration.__init__)
    optional_kwarg_names = [
        name
        for name, parameter in constructor_signature.parameters.items()
        if parameter.kind == inspect.Parameter.KEYWORD_ONLY
    ]
    null_kwargs = {name: None for name in optional_kwarg_names}

    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0, **null_kwargs)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    # optional constructor args are optional fields in the schema
    optional_fields = [
        field.data_key
        for name, field in schema.fields.items()
        if field.required is False
    ]
    for field in optional_fields:
        assert field not in marshalled


def test_marshall_cspconfiguration_does_not_modify_original():
    """
    Verify that serialising a CspConfiguration does not change the object.
    """
    config = CSPConfiguration(
        "csp ID goes here",
        ReceiverBand.BAND_5A,
        [FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1400, 0)],
    )
    original_config = copy.deepcopy(config)
    CSPConfigurationSchema().dumps(config)
    assert config == original_config
