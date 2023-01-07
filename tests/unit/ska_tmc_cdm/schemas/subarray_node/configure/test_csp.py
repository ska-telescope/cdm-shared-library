"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.csp module.
"""
import copy
import inspect

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
    LOWCBFConfiguration
)
from ska_tmc_cdm.schemas.subarray_node.configure import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
)

from ... import utils

VALID_CSP_JSON_PI16 = """{
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
        "subarray_name": "science period 23"
    },
    "common": {
        "config_id": "sbi-mvp01-20200325-00001-science_A",
        "frequency_band": "1",
        "subarray_id": 1
    },
    "cbf": {
        "fsp": [
            {
                "fsp_id": 1,
                "function_mode": "CORR",
                "frequency_slice_id": 1,
                "integration_factor": 1,
                "zoom_factor": 0,
                "channel_averaging_map": [
                    [
                        0,
                        2
                    ],
                    [
                        744,
                        0
                    ]
                ],
                "channel_offset": 0,
                "output_link_map": [
                    [
                        0,
                        0
                    ],
                    [
                        200,
                        1
                    ]
                ]
            },
            {
                "fsp_id": 2,
                "function_mode": "CORR",
                "frequency_slice_id": 2,
                "integration_factor": 1,
                "zoom_factor": 1,
                "channel_averaging_map": [
                    [
                        0,
                        2
                    ],
                    [
                        744,
                        0
                    ]
                ],
                "channel_offset": 744,
                "output_link_map": [
                    [
                        0,
                        4
                    ],
                    [
                        200,
                        5
                    ]
                ],
                "zoom_window_tuning": 650000
            }
        ],
        "vlbi": {

        }
    },
    "pss": {

    },
    "pst": {

    }
}"""

CSP_CONFIGURATION_OBJECT_PI16 = CSPConfiguration(
    interface="https://schema.skao.int/ska-csp-configure/2.0",
    subarray_config=SubarrayConfiguration("science period 23"),
    common_config=CommonConfiguration(
        config_id="sbi-mvp01-20200325-00001-science_A",
        frequency_band=ReceiverBand.BAND_1,
        subarray_id=1,
    ),
    pss_config={},
    pst_config={},
    cbf_config=CBFConfiguration(
        fsp_configs=[
            FSPConfiguration(
                fsp_id=1,
                function_mode=FSPFunctionMode.CORR,
                frequency_slice_id=1,
                integration_factor=1,
                zoom_factor=0,
                channel_averaging_map=[(0, 2), (744, 0)],
                channel_offset=0,
                output_link_map=[(0, 0), (200, 1)],
            ),
            FSPConfiguration(
                fsp_id=2,
                function_mode=FSPFunctionMode.CORR,
                frequency_slice_id=2,
                integration_factor=1,
                zoom_factor=1,
                channel_averaging_map=[(0, 2), (744, 0)],
                channel_offset=744,
                output_link_map=[(0, 4), (200, 5)],
                zoom_window_tuning=650000,
            ),
        ],
        vlbi_config={},
    ),
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


def test_marshall_csp_configuration_does_not_modify_original():
    """
    Verify that serialising a CspConfiguration does not change the object.
    """
    config = CSPConfiguration(
        interface="interface",
        subarray_config=SubarrayConfiguration(subarray_name="subarray name"),
        common_config=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
            band_5_tuning=[5.85, 7.25],
        ),
        low_cbf_config=LOWCBFConfiguration(
            scan_id = 987654321,
            unix_epoch_seconds = 987654321,
            timestamp_ns = 987654321,
            packet_offset = 987654321,
            scan_seconds = 987654321,
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]
        ),
        pss_config=None,
        pst_config=None,
    )
    copied = copy.deepcopy(config)
    CSPConfigurationSchema().dumps(config)

    assert config.interface == copied.interface
    assert config.subarray_config == copied.subarray_config
    assert config.common_config == copied.common_config
    assert config.pst_config == copied.pst_config
    assert config.cbf_config == copied.cbf_config
    assert config.pss_config == copied.pss_config
    assert config.low_cbf_config == copied.low_cbf_config

    assert config == copied


def test_marshall_for_csp_configuration_pi16():
    """
    Verify that serialising a CSPConfiguration does not change the object.
    """
    utils.test_schema_serialisation_and_validation(
        schema_cls=CSPConfigurationSchema,
        instance=CSP_CONFIGURATION_OBJECT_PI16,
        modifier_fn=None,
        valid_json=VALID_CSP_JSON_PI16,
        invalid_json=None,
    )
