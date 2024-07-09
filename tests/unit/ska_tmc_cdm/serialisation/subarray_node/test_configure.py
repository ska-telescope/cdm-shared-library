"""
Unit tests for the ska_tmc_cdm.schemas.subarray_node.configure module.
"""

import json
from datetime import timedelta

import pytest
from ska_ost_osd.telvalidation.semantic_validator import (
    SchematicValidationError,
)

from ska_tmc_cdm.messages.mccssubarray.scan import ScanRequest
from ska_tmc_cdm.messages.subarray_node.configure import (
    MID_SCHEMA,
    ConfigureRequest,
)
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    PointingCorrection,
    ReceiverBand,
    Target,
)
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
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration

from .. import utils

PARTIAL_CONFIGURATION_OFFSET_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.3",
    transaction_id="txn-....-00002",
    pointing=PointingConfiguration(
        target=Target(
            ca_offset_arcsec=-5.0,
            ie_offset_arcsec=5.0,
        )
    ),
    tmc=TMCConfiguration(partial_configuration=True),
)

PARTIAL_CONFIGURATION_OFFSET_JSON = json.dumps(
    {
        "interface": "https://schema.skao.int/ska-tmc-configure/2.3",
        "transaction_id": "txn-....-00002",
        "pointing": {
            "target": {
                "ca_offset_arcsec": -5.0,
                "ie_offset_arcsec": 5.0,
            }
        },
        "tmc": {"partial_configuration": True},
    }
)

NON_COMPLIANCE_MID_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.3",
    transaction_id="txn-....-00001",
    pointing=PointingConfiguration(
        target=Target(
            ra="21:08:47.92",
            dec="-88:57:22.9",
            target_name="Polaris Australis",
            reference_frame="icrs",
        ),
        correction=PointingCorrection.MAINTAIN,
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_5A),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4",
        scan_type="science_A",
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_5B,
            subarray_id=1,
        ),
        pss_config={},
        pst_config={},
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=5,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=744,
                    output_link_map=[(0, 4), (200, 5)],
                    zoom_window_tuning=650000,
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=7,
                    function_mode=FSPFunctionMode.VLBI,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
            ],
            vlbi_config={},
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

NON_COMPLIANCE_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.3",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    },
    "correction": "MAINTAIN"
  },
  "dish": {
    "receiver_band": "5a"
  },
  "csp": {
    "interface": "https://schema.skao.int/ska-csp-configure/2.0",
    "common": {
      "config_id": "sbi-mvp01-20200325-00001-science_A",
      "frequency_band": "5b",
      "subarray_id": 1
    },
    "cbf": {
      "fsp": [
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
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
          "fsp_id": 5,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
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
        },
        {
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
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
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
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
          "fsp_id": 7,
          "function_mode": "VLBI",
          "frequency_slice_id": 2,
          "integration_factor": 1,
          "zoom_factor": 1,
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
        }
      ],
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-configure/3.2",
  "transaction_id": "txn-....-00001",
  "mccs":{
  "subarray_beams": [
    {
        "subarray_beam_id": 1,
        "update_rate": 0.0,
        "logical_bands": [
          {
            "start_channel": 80,
            "number_of_channels": 16
          },
          {
            "start_channel": 384,
            "number_of_channels": 16
          }
        ],
        "apertures": [
          {
            "aperture_id": "AP001.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP001.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP002.01",
            "weighting_key_ref": "aperture2"
          },
          {
            "aperture_id": "AP002.02",
            "weighting_key_ref": "aperture3"
          },
          {
            "aperture_id": "AP003.01",
            "weighting_key_ref": "aperture1"
          }
        ],
        "sky_coordinates": {
          "reference_frame": "ICRS",
          "c1": 180.0,
          "c2": 45.0
          }
      }
    ]
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "csp": {
    "interface": "https://schema.skao.int/ska-low-csp-configure/3.1",
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
          ]
        ],
        "stn_beams": [
          {
            "beam_id": 1,
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
          ],
          "firmware": "vis"
        },
        "stn_beams": [
          {
            "stn_beam_id": 1,
            "integration_ms": 849
          }
        ]
      }
    }
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

VALID_LOW_CONFIGURE_OBJECT_3_1 = ConfigureRequest(
    interface="https://schema.skao.int/ska-low-tmc-configure/3.2",
    transaction_id="txn-....-00001",
    mccs=MCCSConfiguration(
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                update_rate=0.0,
                logical_bands=[
                    SubarrayBeamLogicalBands(
                        start_channel=80, number_of_channels=16
                    ),
                    SubarrayBeamLogicalBands(
                        start_channel=384, number_of_channels=16
                    ),
                ],
                apertures=[
                    SubarrayBeamAperatures(
                        aperture_id="AP001.01", weighting_key_ref="aperture2"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP001.02", weighting_key_ref="aperture3"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP002.01", weighting_key_ref="aperture2"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP002.02", weighting_key_ref="aperture3"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP003.01", weighting_key_ref="aperture1"
                    ),
                ],
                sky_coordinates=SubarrayBeamSkyCoordinates(
                    reference_frame="ICRS",
                    c1=180.0,
                    c2=45.0,
                ),
            )
        ],
    ),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4",
        scan_type="science_A",
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-low-csp-configure/3.1",
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A", subarray_id=1
        ),
        lowcbf=LowCBFConfiguration(
            stations=StationConfiguration(
                stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
                stn_beams=[
                    StnBeamConfiguration(
                        beam_id=1,
                        freq_ids=[400],
                        delay_poly="a/b/c/delaymodel",
                    )
                ],
            ),
            vis=VisConfiguration(
                fsp=VisFspConfiguration(fsp_ids=[1], firmware="vis"),
                stn_beams=[
                    VisStnBeamConfiguration(
                        stn_beam_id=1,
                        integration_ms=849,
                        host=[[0, "192.168.1.00"]],
                        port=[[0, 9000, 1]],
                    )
                ],
            ),
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

VALID_LOW_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-low-tmc-configure/3.2",
    transaction_id="txn-....-00001",
    mccs=MCCSConfiguration(
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                update_rate=0.0,
                logical_bands=[
                    SubarrayBeamLogicalBands(
                        start_channel=80, number_of_channels=16
                    ),
                    SubarrayBeamLogicalBands(
                        start_channel=384, number_of_channels=16
                    ),
                ],
                apertures=[
                    SubarrayBeamAperatures(
                        aperture_id="AP001.01", weighting_key_ref="aperture2"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP001.02", weighting_key_ref="aperture3"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP002.01", weighting_key_ref="aperture2"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP002.02", weighting_key_ref="aperture3"
                    ),
                    SubarrayBeamAperatures(
                        aperture_id="AP003.01", weighting_key_ref="aperture1"
                    ),
                ],
                sky_coordinates=SubarrayBeamSkyCoordinates(
                    reference_frame="ICRS",
                    c1=180.0,
                    c2=45.0,
                ),
            )
        ],
    ),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4",
        scan_type="science_A",
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-low-csp-configure/3.1",
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A"
        ),
        lowcbf=LowCBFConfiguration(
            stations=StationConfiguration(
                stns=[[1, 1], [2, 1], [3, 1], [4, 1]],
                stn_beams=[StnBeamConfiguration(beam_id=1, freq_ids=[400])],
            ),
            vis=VisConfiguration(
                fsp=VisFspConfiguration(
                    function_mode="vis", fsp_ids=[1], firmware="vis"
                ),
                stn_beams=[
                    VisStnBeamConfiguration(
                        stn_beam_id=1,
                        integration_ms=849,
                    )
                ],
            ),
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

VALID_MID_DISH_ONLY_JSON = (
    """
{
    "interface": """
    + f'"{MID_SCHEMA}"'
    + """,
    "dish": {
        "receiver_band": "1"
    }
}
"""
)

VALID_MID_DISH_ONLY_OBJECT = ConfigureRequest(
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1)
)

VALID_NULL_JSON = (
    """
{
    "interface": """
    + f'"{MID_SCHEMA}"'
    + """
}
"""
)

VALID_NULL_OBJECT = ConfigureRequest(interface=MID_SCHEMA)

VALID_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.3",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    },
    "correction": "MAINTAIN"
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
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
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": 10.0
  }
}"""

INVALID_MID_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-tmc-configure/2.1",
  "transaction_id": "txn-....-00001",
  "pointing": {
    "target": {
      "reference_frame": "ICRS",
      "target_name": "Polaris Australis",
      "ra": "21:08:47.92",
      "dec": "-88:57:22.9"
    },
    "correction": "MAINTAIN"
  },
  "dish": {
    "receiver_band": "1"
  },
  "csp": {
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
      "vlbi": {}
    },
    "pss": {},
    "pst": {}
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
  "tmc": {
    "scan_duration": -10
  }
}"""

VALID_MID_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-tmc-configure/2.3",
    transaction_id="txn-....-00001",
    pointing=PointingConfiguration(
        target=Target(
            ra="21:08:47.92",
            dec="-88:57:22.9",
            target_name="Polaris Australis",
            reference_frame="icrs",
        ),
        correction=PointingCorrection.MAINTAIN,
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4",
        scan_type="science_A",
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration(subarray_name="science period 23"),
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
                    channel_offset=0,
                    output_link_map=[(0, 0), (200, 1)],
                ),
                FSPConfiguration(
                    fsp_id=2,
                    function_mode=FSPFunctionMode.CORR,
                    frequency_slice_id=2,
                    integration_factor=1,
                    zoom_factor=1,
                    channel_offset=744,
                    output_link_map=[(0, 4), (200, 5)],
                    zoom_window_tuning=650000,
                ),
            ],
            vlbi_config={},
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

INVALID_LOW_CONFIGURE_JSON = """
{
  "interface": "https://schema.skao.int/ska-low-tmc-configure/3.2",
  "transaction_id": "txn-....-00001",
  "mccs": {
  "subarray_beams": [
    {
        "subarray_beam_id": 1,
        "update_rate": 1.0,
        "logical_bands": [
          {
            "start_channel": 80 ,
            "number_of_channels": 16
          }
        ],
        "apertures": [
          {
            "aperture_id": "AP001.01",
            "weighting_key_ref": "aperture2"
          }
        ],
        "sky_coordinates": {
          "reference_frame": "ICRS",
          "c1": 180.0,
          "c2": 45.0
          }
      }
    ]
  },
  "sdp": {
    "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
    "scan_type": "science_A"
  },
"csp": {
    "interface": "https://schema.skao.int/ska-low-csp-configure/3.1",
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
          ]
        ],
        "stn_beams": [
          {
            "beam_id":1,
            "freq_ids": [
              400
            ]
          }
        ]
      },
      "vis": {
        "fsp": {
          "firmware": "abcd",
          "fsp_ids": [
            1, 2, 2, 4, 5, 6, 7
          ]
        },
        "stn_beams": [
          {
            "stn_beam_id": 1,
            "integration_ms": 849
          }
        ]
      }
    }
  },
  "tmc": {
    "scan_duration": 10.0
  }
}
"""

INVALID_LOW_CONFIGURE_OBJECT = ConfigureRequest(
    interface="https://schema.skao.int/ska-low-tmc-configure/3.2",
    transaction_id="txn-....-00001",
    mccs=MCCSConfiguration(
        subarray_beam_configs=[
            SubarrayBeamConfiguration(
                subarray_beam_id=1,
                update_rate=1.0,
                logical_bands=[
                    SubarrayBeamLogicalBands(
                        start_channel=80, number_of_channels=16
                    )
                ],
                apertures=[
                    SubarrayBeamAperatures(
                        aperture_id="AP001.01", weighting_key_ref="aperture2"
                    )
                ],
                sky_coordinates=SubarrayBeamSkyCoordinates(
                    reference_frame="ICRS",
                    c1=180.0,
                    c2=45.0,
                ),
            )
        ],
    ),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4",
        scan_type="science_A",
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-low-csp-configure/3.1",
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
        ),
        lowcbf=LowCBFConfiguration(
            stations=StationConfiguration(
                stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
                stn_beams=[StnBeamConfiguration(beam_id=1, freq_ids=[400])],
            ),
            vis=VisConfiguration(
                fsp=VisFspConfiguration(
                    firmware="abcd", fsp_ids=[1, 2, 2, 4, 5, 6, 7]
                ),
                stn_beams=[
                    VisStnBeamConfiguration(stn_beam_id=1, integration_ms=849)
                ],
            ),
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)


SCAN_VALID_JSON = """
{
  "interface": "https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
  "scan_id":1,
  "start_time": 0.0
}
"""

SCAN_VALID_OBJECT = ScanRequest(
    interface="https://schema.skatelescope.org/ska-low-mccs-scan/1.0",
    scan_id=1,
    start_time=0.0,
)


def low_invalidator(o: ConfigureRequest):
    # function to make a valid LOW ConfigureRequest invalid
    o.mccs.subarray_beam_configs[0].subarray_beam_id = -1


def mid_invalidator(o: ConfigureRequest):
    # function to make a valid MID ConfigureRequest invalid
    o.tmc.scan_duration = timedelta(seconds=-10)


def partial_invalidator(o: ConfigureRequest):
    # function to make a valid partial MID ConfigureRequest invalid
    o.pointing.target.coord = None
    o.tmc.partial_configuration = False


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ConfigureRequest,
            PARTIAL_CONFIGURATION_OFFSET_OBJECT,
            mid_invalidator,
            PARTIAL_CONFIGURATION_OFFSET_JSON,
            None,
            True,
        ),
        (
            ConfigureRequest,
            VALID_MID_CONFIGURE_OBJECT,
            mid_invalidator,
            VALID_MID_CONFIGURE_JSON,
            INVALID_MID_CONFIGURE_JSON,
            True,
        ),
        (
            ConfigureRequest,
            VALID_MID_DISH_ONLY_OBJECT,
            None,  # no validation on MID
            VALID_MID_DISH_ONLY_JSON,
            None,
            False,
        ),
        (
            ConfigureRequest,
            VALID_NULL_OBJECT,
            None,  # no validation for null object
            VALID_NULL_JSON,
            None,
            False,
        ),
        (
            ConfigureRequest,
            VALID_LOW_CONFIGURE_OBJECT,
            None,
            VALID_LOW_CONFIGURE_JSON,
            None,
            False,
        ),
        (
            ConfigureRequest,
            VALID_MID_CONFIGURE_OBJECT,
            None,
            VALID_MID_CONFIGURE_JSON,
            None,
            True,
        ),
        (
            ScanRequest,
            SCAN_VALID_OBJECT,
            None,
            SCAN_VALID_JSON,
            None,
            True,
        ),
    ],
)
def test_configure_serialisation_and_validation(
    model_class,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly.
    """
    utils.test_serialisation_and_validation(
        model_class,
        instance,
        modifier_fn,
        valid_json,
        invalid_json,
        is_validate,
    )


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ConfigureRequest,
            NON_COMPLIANCE_MID_CONFIGURE_OBJECT,
            None,
            NON_COMPLIANCE_MID_CONFIGURE_JSON,
            None,
            True,
        ),
    ],
)
def test_configure_serialisation_and_validation_invalid_json(
    model_class,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly
    for invalid json and raise SchematicValidationError.
    """
    with pytest.raises(SchematicValidationError):
        utils.test_serialisation_and_validation(
            model_class,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
        )


@pytest.mark.parametrize(
    "model_class,instance,modifier_fn,valid_json,invalid_json,is_validate",
    [
        (
            ConfigureRequest,
            INVALID_LOW_CONFIGURE_OBJECT,
            low_invalidator,
            INVALID_LOW_CONFIGURE_JSON,
            None,
            True,
        ),
    ],
)
def test_low_configure_serialisation_and_validation_invalid_json(
    model_class,
    instance,
    modifier_fn,
    valid_json,
    invalid_json,
    is_validate,
):
    """
    Verifies that the schema marshals, unmarshals, and validates correctly
    for invalid json and raise SchematicValidationError.
    """
    with pytest.raises(SchematicValidationError):
        utils.test_serialisation_and_validation(
            model_class,
            instance,
            modifier_fn,
            valid_json,
            invalid_json,
            is_validate,
        )
