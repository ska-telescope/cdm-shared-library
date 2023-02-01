"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.csp module.
"""
import copy
import inspect

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    BeamsConfiguration,
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationsConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamsConfiguration,
)
from ska_tmc_cdm.schemas.subarray_node.configure import (
    CSPConfigurationSchema,
    FSPConfigurationSchema,
)
from ska_tmc_cdm.schemas.subarray_node.configure.csp import (
    BeamsConfigurationSchema,
    LowCBFConfigurationSchema,
    StationsConfigurationSchema,
    StnBeamConfigurationSchema,
    TimingBeamsConfigurationSchema,
)
from ska_tmc_cdm.utils import assert_json_is_equal

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
    subarray=SubarrayConfiguration("science period 23"),
    common=CommonConfiguration(
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

VALID_CSP_JSON_PI17 = """{
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "subarray": {
      "subarray_name": "science period 23"
    },
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band":"1"
    },
    "lowcbf": {
      "stations": {
        "stns": [
          [
            1,
            0
          ],
          [
            2,
            0
          ],
          [
            3,
            0
          ],
          [
            4,
            0
          ]
        ],
        "stn_beams": [
          {
            "beam_id": 1,
            "freq_ids": [
              64,
              65,
              66,
              67,
              68,
              68,
              70,
              71
            ],
            "boresight_dly_poly": "url"
          }
        ]
      },
      "timing_beams": {
        "beams": [
          {
            "pst_beam_id": 13,
            "stn_beam_id": 1,
            "offset_dly_poly": "url",
            "stn_weights": [
              0.9,
              1.0,
              1.0,
              0.9
            ],
            "jones": "url",
            "dest_chans": [
              128,
              256
            ],
            "rfi_enable": [
              true,
              true,
              true
           ],
            "rfi_static_chans": [
              1,
              206,
              997
            ],
            "rfi_dynamic_chans": [
              242,
              1342
            ],
            "rfi_weighted": 0.87
          }
        ]
      }
    }
  }"""


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
        subarray=SubarrayConfiguration(subarray_name="subarray name"),
        common=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
            band_5_tuning=[5.85, 7.25],
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
    assert config.subarray == copied.subarray
    assert config.common == copied.common
    assert config.cbf_config == copied.cbf_config
    assert config.pss_config == copied.pss_config
    assert config.pst_config == copied.pst_config

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


def test_marshall_for_csp_configuration_pi17():
    """
    Verify that serialising a CSPConfiguration does not change the object.
    """
    csp_configuration_object = CSPConfigurationSchema().loads(VALID_CSP_JSON_PI17)
    serialized_csp_config = CSPConfigurationSchema().dumps(csp_configuration_object)
    assert_json_is_equal(VALID_CSP_JSON_PI17, serialized_csp_config)


def test_marshall_station_configuration_does_not_modify_original():
    """
    Verify that serialising a StationsConfiguration does not change the object.
    """
    config = StationsConfiguration(
        stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
        stn_beams=[
            StnBeamConfiguration(
                beam_id=1,
                freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                boresight_dly_poly="url",
            )
        ],
    )
    copied = copy.deepcopy(config)
    StationsConfigurationSchema().dumps(config)

    assert config.stns == copied.stns
    assert config.stn_beams == copied.stn_beams
    assert config == copied


def test_marshall_station_beam_configuration_does_not_modify_original():
    """
    Verify that serialising a StationsConfiguration does not change the object.
    """
    config = StnBeamConfiguration(
        beam_id=1, freq_ids=[64, 65, 66, 67, 68, 68, 70, 71], boresight_dly_poly="url"
    )
    copied = copy.deepcopy(config)
    StnBeamConfigurationSchema().dumps(config)

    assert config.beam_id == copied.beam_id
    assert config.freq_ids == copied.freq_ids
    assert config.boresight_dly_poly == copied.boresight_dly_poly
    assert config == copied


def test_marshall_timing_beam_configuration_does_not_modify_original():
    """
    Verify that serialising a TimingBeamsConfiguration does not change the object.
    """
    config = TimingBeamsConfiguration(
        beams=[
            BeamsConfiguration(
                pst_beam_id=13,
                stn_beam_id=1,
                offset_dly_poly="url",
                stn_weights=[0.9, 1.0, 1.0, 0.9],
                jones="url",
                dest_chans=[128, 256],
                rfi_enable=[True, True, True],
                rfi_static_chans=[1, 206, 997],
                rfi_dynamic_chans=[242, 1342],
                rfi_weighted=0.87,
            )
        ]
    )

    copied = copy.deepcopy(config)

    TimingBeamsConfigurationSchema().dumps(config)

    assert config.beams == copied.beams
    assert config == copied


def test_marshall_beam_configuration_does_not_modify_original():
    """
    Verify that serialising a StationsConfiguration does not change the object.
    """
    config = BeamsConfiguration(
        pst_beam_id=13,
        stn_beam_id=1,
        offset_dly_poly="url",
        stn_weights=[0.9, 1.0, 1.0, 0.9],
        jones="url",
        dest_chans=[128, 256],
        rfi_enable=[True, True, True],
        rfi_static_chans=[1, 206, 997],
        rfi_dynamic_chans=[242, 1342],
        rfi_weighted=0.87,
    )
    copied = copy.deepcopy(config)
    BeamsConfigurationSchema().dumps(config)

    assert config.pst_beam_id == copied.pst_beam_id
    assert config.stn_beam_id == copied.stn_beam_id
    assert config.offset_dly_poly == copied.offset_dly_poly
    assert config.stn_weights == copied.stn_weights
    assert config.jones == copied.jones
    assert config.dest_chans == copied.dest_chans
    assert config.rfi_enable == copied.rfi_enable
    assert config.rfi_static_chans == copied.rfi_static_chans
    assert config.rfi_dynamic_chans == copied.rfi_dynamic_chans
    assert config.rfi_weighted == copied.rfi_weighted
    assert config == copied


def test_marshall_low_cbf_configuration_does_not_modify_original():
    """
    Verify that serialising a LowCBFConfiguration does not change the object.
    """
    config = LowCBFConfiguration(
        stations=StationsConfiguration(
            stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
            stn_beams=[
                StnBeamConfiguration(
                    beam_id=1,
                    freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                    boresight_dly_poly="url",
                )
            ],
        ),
        timing_beams=TimingBeamsConfiguration(
            beams=[
                BeamsConfiguration(
                    pst_beam_id=13,
                    stn_beam_id=1,
                    offset_dly_poly="url",
                    stn_weights=[0.9, 1.0, 1.0, 0.9],
                    jones="url",
                    dest_chans=[128, 256],
                    rfi_enable=[True, True, True],
                    rfi_static_chans=[1, 206, 997],
                    rfi_dynamic_chans=[242, 1342],
                    rfi_weighted=0.87,
                )
            ]
        ),
    )
    copied = copy.deepcopy(config)

    LowCBFConfigurationSchema().dumps(config)

    assert config.stations == copied.stations
    assert config.timing_beams == copied.timing_beams
    assert config == copied
