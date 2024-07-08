"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure.csp module.
"""
import inspect

from ska_tmc_cdm import CODEC
from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    VisConfiguration,
    VisFspConfiguration,
    VisStnBeamConfiguration,
)

from ... import utils

VALID_CSP_JSON_PI16 = """{
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
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
                ]
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

VALID_LOW_CSP_JSON_PI20 = """{
    "interface": "https://schema.skao.int/ska-low-csp-configure/0.0",
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A"
    },
    "lowcbf": {
      "stations": {
        "stns": [
          [
            1,
            1
          ],
          [
            2,
            1
          ],
          [
            3,
            1
          ],
          [
            4,
            1
          ],
          [
            5,
            1
          ],
          [
            6,
            1
          ]
        ],
        "stn_beams": [
          {
            "stn_beam_id": 1,
            "freq_ids": [
              400
            ]
          }
        ]
      },
      "vis": {
        "fsp": {
          "function_mode": "vis",
          "fsp_ids": [
            1
          ]
        },
        "stn_beams": [
          {
            "stn_beam_id": 1,
            "host": [
              [
                0,
                "192.168.1.00"
              ]
            ],
            "port": [
              [
                0,
                9000,
                1
              ]
            ],
            "mac": [
              [
                0,
                "02-03-04-0a-0b-0c"
              ]
            ],
            "integration_ms": 849
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
    fsp_config = FSPConfiguration(
        fsp_id=1,
        function_mode=FSPFunctionMode.CORR,
        frequency_slice_id=1,
        integration_factor=10,
        zoom_factor=0,
    )
    marshalled = CODEC.dumps(fsp_config)

    optional_fields = [
        field
        for field, detail in FSPConfiguration.model_fields.items()
        if not detail.is_required()
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

    fsp_config = FSPConfiguration(
        fsp_id=1,
        function_mode=FSPFunctionMode.CORR,
        frequency_slice_id=1,
        integration_factor=10,
        zoom_factor=0,
        **null_kwargs,
    )
    marshalled = CODEC.dumps(fsp_config)

    # optional constructor args are optional fields in the schema
    optional_fields = [
        field
        for field, detail in FSPConfiguration.model_fields.items()
        if not detail.is_required()
    ]
    for field in optional_fields:
        assert field not in marshalled


def test_marshall_csp_configuration_does_not_modify_original():
    """
    Verify that serialising a CspConfiguration does not change the object.
    """
    fsp_config = FSPConfiguration(
        fsp_id=1,
        function_mode=FSPFunctionMode.CORR,
        frequency_slice_id=1,
        integration_factor=10,
        zoom_factor=0,
    )
    config = CSPConfiguration(
        interface="interface",
        common=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
            band_5_tuning=[5.85, 7.25],
        ),
        cbf_config=CBFConfiguration(fsp_configs=[fsp_config]),
        pss_config=None,
        pst_config=None,
    )
    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.interface == copied.interface
    assert config.common == copied.common
    assert config.cbf_config == copied.cbf_config
    assert config.pss_config == copied.pss_config
    assert config.pst_config == copied.pst_config

    assert config == copied


def test_marshall_for_csp_configuration_pi16():
    """
    Verify that serialising a CSPConfiguration does not change the object.
    """
    utils.test_serialisation_and_validation(
        model_class=CSPConfiguration,
        instance=CSP_CONFIGURATION_OBJECT_PI16,
        modifier_fn=None,
        valid_json=VALID_CSP_JSON_PI16,
        invalid_json=None,
    )


def test_marshall_station_configuration_does_not_modify_original():
    """
    Verify that serialising a StationConfiguration does not change the object.
    """
    config = StationConfiguration(
        stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
        stn_beams=[
            StnBeamConfiguration(
                beam_id=1,
                freq_ids=[400],
                stn_beam_id=1,
            )
        ],
    )
    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.stns == copied.stns
    assert config.stn_beams == copied.stn_beams
    assert config == copied


def test_marshall_station_beam_configuration_does_not_modify_original():
    """
    Verify that serialising a StationConfiguration does not change the object.
    """
    config = StnBeamConfiguration(
        beam_id=1,
        freq_ids=[400],
        stn_beam_id=1,
    )
    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.stn_beam_id == copied.stn_beam_id
    assert config.freq_ids == copied.freq_ids
    assert config == copied


def test_marshall_vis_configuration_does_not_modify_original():
    """
    Verify that serialising a VisConfiguration does not change the object.
    """
    config = VisConfiguration(
        fsp=VisFspConfiguration(function_mode="vis", fsp_ids=[1]),
        stn_beams=[
            VisStnBeamConfiguration(
                stn_beam_id=1,
                integration_ms=849,
                host=[[0, "192.168.1.00"]],
                port=[[0, 9000, 1]],
                mac=[[0, "02-03-04-0a-0b-0c"]],
            )
        ],
    )

    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.fsp == copied.fsp
    assert config.stn_beams == copied.stn_beams
    assert config == copied


def test_marshall_vis_fsp_configuration_does_not_modify_original():
    """
    Verify that serialising a VisFspConfiguration does not change the object.
    """
    config = VisFspConfiguration(function_mode="vis", fsp_ids=[1])

    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.function_mode == copied.function_mode
    assert config.fsp_ids == copied.fsp_ids
    assert config == copied


def test_marshall_low_cbf_configuration_does_not_modify_original():
    """
    Verify that serialising a LowCBFConfiguration does not change the object.
    """
    config = LowCBFConfiguration(
        stations=StationConfiguration(
            stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
            stn_beams=[
                StnBeamConfiguration(beam_id=1, freq_ids=[400], stn_beam_id=1)
            ],
        ),
        vis=VisConfiguration(
            fsp=VisFspConfiguration(function_mode="vis", fsp_ids=[1]),
            stn_beams=[
                VisStnBeamConfiguration(
                    integration_ms=849,
                    stn_beam_id=1,
                    host=[[0, "192.168.1.00"]],
                    port=[[0, 9000, 1]],
                    mac=[[0, "02-03-04-0a-0b-0c"]],
                )
            ],
        ),
    )
    copied = config.model_copy(deep=True)
    CODEC.dumps(config)

    assert config.stations == copied.stations
    assert config.vis == config.vis
    assert config == copied
