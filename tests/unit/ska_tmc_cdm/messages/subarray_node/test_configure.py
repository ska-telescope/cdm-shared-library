"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import copy
from datetime import timedelta

import pytest

from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    DishConfiguration,
    PointingConfiguration,
    ReceiverBand,
    Target,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    BeamConfiguration,
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget,
)
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration

CONFIGURE_OBJECT_ARGS_PI16 = dict(
    interface="https://schema.skao.int/ska-tmc-configure/2.1",
    transaction_id="txn-....-00001",
    pointing=PointingConfiguration(
        Target(
            ra="21:08:47.92",
            dec="-88:57:22.9",
            target_name="Polaris Australis",
            reference_frame="icrs",
        )
    ),
    dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1),
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
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
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)

CONFIGURE_OBJECT_ARGS_PI7 = dict(
    interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
    transaction_id="txn-....-00001",
    sdp=SDPConfiguration(
        interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
    ),
    csp=CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/2.0",
        subarray=SubarrayConfiguration("science period 23"),
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
        ),
        lowcbf=LowCBFConfiguration(
            {
                "station": StationConfiguration(
                    **{
                        "stns": [[1, 0], [2, 0], [3, 0], [4, 0]],
                        "stn_beams": [
                            StnBeamConfiguration(
                                **{
                                    "beam_id": 1,
                                    "freq_ids": [64, 65, 66, 67, 68, 68, 70, 71],
                                    "boresight_dly_poly": "url",
                                }
                            )
                        ],
                    }
                ),
                "timing_beams": TimingBeamConfiguration(
                    **{
                        "beams": [
                            BeamConfiguration(
                                **{
                                    "pst_beam_id": 13,
                                    "stn_beam_id": 1,
                                    "offset_dly_poly": "url",
                                    "stn_weights": [0.9, 1.0, 1.0, 0.9],
                                    "jones": "url",
                                    "dest_chans": [128, 256],
                                    "rfi_enable": [True, True, True],
                                    "rfi_static_chans": [1, 206, 997],
                                    "rfi_dynamic_chans": [242, 1342],
                                    "rfi_weighted": 0.87,
                                }
                            )
                        ]
                    }
                ),
            }
        ),
    ),
    tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
)


def test_configure_request_eq():
    """
    Verify that ConfigurationRequest objects are considered equal when:
      - they point to the same target
      - they set the same receiver band
      - their SDP configuration is the same
      - their CSP configuration is the same
    """
    transaction_id = "transaction_id"
    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration(scan_type="science_A")
    csp_config = CSPConfiguration(
        interface="interface",
        subarray=SubarrayConfiguration(subarray_name="subarray name"),
        common=CommonConfiguration(
            config_id="config_id", frequency_band=ReceiverBand.BAND_1, subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]
        ),
        pss_config=None,
        pst_config=None,
    )
    request_1 = ConfigureRequest(
        transaction_id=transaction_id,
        pointing=pointing_config,
        dish=dish_config,
        sdp=sdp_config,
        csp=csp_config,
    )
    request_2 = copy.deepcopy(request_1)
    assert request_1 == request_2


def test_configure_request_eq_for_low():
    """
    Verify that ConfigurationRequest objects for are considered equal when:
      - they point to the same target
      - their MCCS configuration is the same
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    request_1 = ConfigureRequest(
        interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A"),
    )
    request_2 = ConfigureRequest(
        interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A"),
    )
    assert request_1 == request_2


def test_mccs_configure_request_eq():
    """
    Verify that ConfigurationRequest objects for are considered equal when:
      - they point to the same target
      - their MCCS configuration is the same
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    request_1 = ConfigureRequest(mccs=mccs_config)
    request_2 = ConfigureRequest(mccs=mccs_config)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration(scan_type="science_A")
    csp_config = CSPConfiguration(
        interface="interface",
        subarray=SubarrayConfiguration(subarray_name="subarray name"),
        common=CommonConfiguration(
            config_id="config_id", frequency_band=ReceiverBand.BAND_1, subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]
        ),
        pss_config=None,
        pst_config=None,
    )
    request = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
    assert request != object


def test_mccs_configure_request_is_not_equal_to_other_objects():
    """
    Verify that an MCCS ConfigureRequest is not equal to other objects.
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    request = ConfigureRequest(mccs=mccs_config)
    assert request != object
    assert request is not None


def test_configure_request_is_not_equal_to_other_objects_for_low():
    """
    Verify that an MCCS ConfigureRequest is not equal to other objects.
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    request = ConfigureRequest(
        interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A"),
    )
    assert request != object
    assert request is not None


def test_configure_request_mccs_independence():
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    request = ConfigureRequest(mccs=mccs_config)
    assert request is not None

    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    with pytest.raises(ValueError):
        ConfigureRequest(dish=dish_config, mccs=mccs_config)

    # sdp_config = SDPConfiguration("science_A")
    # with pytest.raises(ValueError):
    #     ConfigureRequest(dish=dish_config, sdp=sdp_config, mccs=mccs_config)
    #
    # channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    # config_id = "sbi-mvp01-20200325-00001-science_A"
    # fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    # csp_config = CSPConfiguration(config_id, ReceiverBand.BAND_1, [fsp_config])
    # with pytest.raises(ValueError):
    #     ConfigureRequest(
    #         dish=dish_config, sdp=sdp_config, csp=csp_config, mccs=mccs_config
    #     )


def test_configure_request_equals_pi16():
    """
    Verify that ConfigureRequest objects are considered equal when all
    attributes are equal and not equal when there value differ.
    """

    configure_request_obj_1 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI16)
    configure_request_obj_2 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI16)

    assert configure_request_obj_1 == configure_request_obj_2

    alt_csp_configuration_csp_2_0_args = CONFIGURE_OBJECT_ARGS_PI16.copy()
    alt_csp_configuration_csp_2_0_args[
        "interface"
    ] = "Changing interface value for creating object with different value"

    configure_request_obj_3 = ConfigureRequest(**alt_csp_configuration_csp_2_0_args)

    assert configure_request_obj_1 != configure_request_obj_3


def test_configure_request_not_equal_to_other_objects_pi16():
    """
    Verify that ConfigureRequest objects are not considered equal to objects
    of other types.
    """
    configure_request_obj_1 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI16)

    assert configure_request_obj_1 != 1


def test_configure_request_equals_pi17():
    """
    Verify that ConfigureRequest objects are considered equal when all
    attributes are equal and not equal when there value differ.
    """

    configure_request_obj_1 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI7)
    configure_request_obj_2 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI7)

    assert configure_request_obj_1 == configure_request_obj_2

    alt_csp_configuration_csp_2_0_args = CONFIGURE_OBJECT_ARGS_PI7.copy()
    alt_csp_configuration_csp_2_0_args[
        "interface"
    ] = "Changing interface value for creating object with different value"

    configure_request_obj_3 = ConfigureRequest(**alt_csp_configuration_csp_2_0_args)

    assert configure_request_obj_1 != configure_request_obj_3


def test_configure_request_not_equal_to_other_objects_pi17():
    """
    Verify that ConfigureRequest objects are not considered equal to objects
    of other types.
    """
    configure_request_obj_1 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI7)

    assert configure_request_obj_1 != 1


def test_configure_request_eq_for_low_pi17():
    """
    Verify that ConfigurationRequest objects for are considered equal
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )
    stn_beam = {
        "beam_id": 1,
        "freq_ids": [64, 65, 66, 67, 68, 68, 70, 71],
        "boresight_dly_poly": "url",
    }
    station = {
        "stns": [[1, 0], [2, 0], [3, 0], [4, 0]],
        "stn_beams": [StnBeamConfiguration(stn_beam)],
    }
    beams = {
        "pst_beam_id": 13,
        "stn_beam_id": 1,
        "offset_dly_poly": "url",
        "stn_weights": [0.9, 1.0, 1.0, 0.9],
        "jones": "url",
        "dest_chans": [128, 256],
        "rfi_enable": [True, True, True],
        "rfi_static_chans": [1, 206, 997],
        "rfi_dynamic_chans": [242, 1342],
        "rfi_weighted": 0.87,
    }
    timing_beams = {"beams": [BeamConfiguration(beams)]}
    low_cbf = {
        "station": StationConfiguration(station),
        "timing_beams": TimingBeamConfiguration(timing_beams),
    }

    request_1 = ConfigureRequest(
        interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
        transaction_id="txn-....-00001",
        mccs=mccs_config,
        sdp=SDPConfiguration(
            interface="https://schema.skao.int/ska-sdp-configure/0.4",
            scan_type="science_A",
        ),
        tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
        csp=CSPConfiguration(
            interface="https://schema.skao.int/ska-csp-configure/2.0",
            subarray=SubarrayConfiguration("science period 23"),
            common=CommonConfiguration(
                config_id="sbi-mvp01-20200325-00001-science_A",
            ),
            lowcbf=LowCBFConfiguration(low_cbf),
        ),
    )
    request_2 = copy.deepcopy(request_1)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects_for_low_pi17():
    """
    Verify that  ConfigureRequest is not equal to other objects.
    """
    station_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    station_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    )

    request = ConfigureRequest(
        interface="https://schema.skao.int/ska-low-tmc-configure/3.0",
        transaction_id="txn-....-00001",
        mccs=mccs_config,
        sdp=SDPConfiguration(
            interface="https://schema.skao.int/ska-sdp-configure/0.4",
            scan_type="science_A",
        ),
        tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
        csp=CSPConfiguration(
            interface="https://schema.skao.int/ska-csp-configure/2.0",
            subarray=SubarrayConfiguration("science period 23"),
            common=CommonConfiguration(
                config_id="sbi-mvp01-20200325-00001-science_A",
            ),
            lowcbf=LowCBFConfiguration(
                stations=StationConfiguration(
                    stns=[[1, 0], [2, 0], [3, 0], [4, 0]],
                    stn_beams=[
                        StnBeamConfiguration(
                            beam_id=1,
                            freq_ids=[64, 65, 66, 67, 68, 68, 70, 71],
                            boresight_dly_poly="url",
                        )
                    ],
                ),
                timing_beams=TimingBeamConfiguration(
                    beams=[
                        BeamConfiguration(
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
            ),
        ),
    )
    assert request != object
    assert request is not None
