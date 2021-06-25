"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.csp module.
"""
import copy
import inspect

from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration
)
from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.schemas.subarray_node.configure import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
)


def test_marshall_fsp_configuration_with_undefined_optional_parameters():
    """
    Verify that optional FSPConfiguration parameters are removed when they are
    left unset.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
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

    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0, **null_kwargs)
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
        interface="interface",
        subarray_config=SubarrayConfiguration(
            subarray_name="subarray name"
        ),
        common_config=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
            ]
        ),
        pss_config=None,
        pst_config=None,
    )
    copied = copy.deepcopy(config)
    CSPConfigurationSchema().dumps(config)

    assert config.interface == copied.interface
    assert config.subarray_config == copied.subarray_config
    assert config.common_config == copied.common_config
    assert config.cbf_config == copied.cbf_config
    assert config.pss_config == copied.pss_config
    assert config.pst_config == copied.pst_config

    assert config == copied
