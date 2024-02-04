"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import copy
from datetime import timedelta

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.subarray_node.configure import (
    LOW_SCHEMA,
    MID_SCHEMA,
    ConfigureRequest,
)
from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import FSPFunctionMode
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure_resource import (
    ConfigureRequestBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.core import (
    DishConfigurationBuilder,
    PointingConfigurationBuilder,
    TargetBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.csp import (
    CBFConfigurationBuilder,
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    FSPConfigurationBuilder,
    SubarrayConfigurationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.mccs import (
    MCCSConfigurationBuilder,
    StnConfigurationBuilder,
    SubarrayBeamConfigurationBuilder,
    SubarrayBeamTargetBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.sdp import SDPConfigurationBuilder
from tests.unit.ska_tmc_cdm.builder.subarray_node.tmc import TMCConfigurationBuilder

# CONFIGURE_OBJECT_ARGS_PI16 = dict(
#     interface="https://schema.skao.int/ska-tmc-configure/2.1",
#     transaction_id="txn-....-00001",
#     pointing=PointingConfiguration(
#         Target(
#             ra="21:08:47.92",
#             dec="-88:57:22.9",
#             target_name="Polaris Australis",
#             reference_frame="icrs",
#         )
#     ),
#     dish=DishConfiguration(receiver_band=ReceiverBand.BAND_1),
#     sdp=SDPConfiguration(
#         interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
#     ),
#     csp=CSPConfiguration(
#         interface="https://schema.skao.int/ska-csp-configure/2.0",
#         subarray=SubarrayConfiguration("science period 23"),
#         common=CommonConfiguration(
#             config_id="sbi-mvp01-20200325-00001-science_A",
#             frequency_band=ReceiverBand.BAND_1,
#             subarray_id=1,
#         ),
#         pss_config={},
#         pst_config={},
#         cbf_config=CBFConfiguration(
#             fsp_configs=[
#                 FSPConfiguration(
#                     fsp_id=1,
#                     function_mode=FSPFunctionMode.CORR,
#                     frequency_slice_id=1,
#                     integration_factor=1,
#                     zoom_factor=0,
#                     channel_averaging_map=[(0, 2), (744, 0)],
#                     channel_offset=0,
#                     output_link_map=[(0, 0), (200, 1)],
#                 ),
#                 FSPConfiguration(
#                     fsp_id=2,
#                     function_mode=FSPFunctionMode.CORR,
#                     frequency_slice_id=2,
#                     integration_factor=1,
#                     zoom_factor=1,
#                     channel_averaging_map=[(0, 2), (744, 0)],
#                     channel_offset=744,
#                     output_link_map=[(0, 4), (200, 5)],
#                     zoom_window_tuning=650000,
#                 ),
#             ],
#             vlbi_config={},
#         ),
#     ),
#     tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
# )
#
# CONFIGURE_LOW_OBJECT_ARGS = dict(
#     interface="https://schema.skao.int/ska-low-tmc-configure/3.1",
#     transaction_id="txn-....-00001",
#     sdp=SDPConfiguration(
#         interface="https://schema.skao.int/ska-sdp-configure/0.4", scan_type="science_A"
#     ),
#     csp=CSPConfiguration(
#         interface="https://schema.skao.int/ska-low-csp-configure/0.0",
#         common=CommonConfiguration(
#             config_id="sbi-mvp01-20200325-00001-science_A",
#         ),
#         lowcbf=LowCBFConfiguration(
#             stations=StationConfiguration(
#                 stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
#                 stn_beams=[
#                     StnBeamConfiguration(
#                         stn_beam_id=1,
#                         freq_ids=[400],
#                     )
#                 ],
#             ),
#             vis=VisConfiguration(
#                 fsp=VisFspConfiguration(function_mode="vis", fsp_ids=[1]),
#                 stn_beams=[
#                     StnBeamConfiguration(
#                         stn_beam_id=1,
#                         host=[[0, "192.168.1.00"]],
#                         port=[[0, 9000, 1]],
#                         mac=[[0, "02-03-04-0a-0b-0c"]],
#                         integration_ms=849,
#                     )
#                 ],
#             ),
#         ),
#     ),
#     tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
# )


def test_empty_configure_request_fails():
    """
    Verify that an empty ConfigureRequest without dish, mccs or interface set throws a ValueError
    """
    with pytest.raises(ValueError):
        _ = ConfigureRequestBuilder().build()


def test_configure_request_with_mccs_has_low_interface_set_on_creation():
    """
    Verify that ConfigureRequest with valid MCCSConfiguration has a LOW Schema set on creation
    """
    # station_config = StnConfiguration(1)
    station_config = StnConfigurationBuilder().set_station_id(1).build()

    # target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    target = (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )

    # station_beam_config = SubarrayBeamConfiguration(1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0])
    station_beam_config = (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )

    # mccs_config = MCCSConfiguration(station_configs=[station_config], subarray_beam_configs=[station_beam_config])
    mccs_config = (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )

    # request = ConfigureRequest(mccs=mccs_config,)
    request = ConfigureRequestBuilder().set_mccs(mccs_config).build()

    assert request.interface is not None
    assert request.interface == LOW_SCHEMA


def test_configure_request_with_dish_has_mid_interface_set_on_creation():
    """
    Verify that ConfigureRequest with valid DishConfiguration has a MID Schema set on creation
    """
    # config_1 = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    config_1 = (
        DishConfigurationBuilder()
        .set_receiver_band(receiver_band=ReceiverBand.BAND_1)
        .build()
    )

    # request = ConfigureRequest(dish=config_1)
    request = ConfigureRequestBuilder().set_dish(config_1).build()

    assert request.interface is not None
    assert request.interface == MID_SCHEMA


def test_configure_request_eq():
    """
    Verify that ConfigureRequest objects are considered equal when:
      - they point to the same target
      - they set the same receiver band
      - their SDP configuration is the same
      - their CSP configuration is the same
    """
    transaction_id = "transaction_id"
    # pointing_config = PointingConfiguration(Target(1, 1))
    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
        .build()
    )

    # dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    # sdp_config = SDPConfiguration(scan_type="science_A")
    sdp_config = SDPConfigurationBuilder().set_scan_type("science_A").build()
    # csp_config = CSPConfiguration(
    #     interface="interface",
    #     subarray=SubarrayConfiguration(subarray_name="subarray name"),
    #     common=CommonConfiguration(config_id="config_id", frequency_band=ReceiverBand.BAND_1, subarray_id=1),
    #     cbf_config=CBFConfiguration(fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]),
    #     pss_config=None,
    #     pst_config=None,
    # )

    csp_config = (
        CSPConfigurationBuilder()
        .set_interface("interface")
        .set_subarray(
            SubarrayConfigurationBuilder()
            .set_subarray_name(subarray_name="subarray name")
            .build()
        )
        .set_common(
            CommonConfigurationBuilder()
            .set_config_id(config_id="config_id")
            .set_frequency_band(frequency_band=ReceiverBand.BAND_1)
            .set_subarray_id(1)
            .build()
        )
        .set_cbf_config(
            CBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(fsp_id=1)
                    .set_function_mode(function_mode=FSPFunctionMode.CORR)
                    .set_frequency_slice_id(frequency_slice_id=1)
                    .set_integration_factor(integration_factor=10)
                    .set_zoom_factor(0)
                    .build()
                ]
            )
            .build()
        )
        .build()
    )

    # request_1 = ConfigureRequest(
    #     transaction_id=transaction_id,
    #     pointing=pointing_config,
    #     dish=dish_config,
    #     sdp=sdp_config,
    #     csp=csp_config,
    # )

    request_1 = (
        ConfigureRequestBuilder()
        .set_transaction_id(transaction_id=transaction_id)
        .set_pointing(pointing=pointing_config)
        .set_dish(dish=dish_config)
        .set_sdp(sdp=sdp_config)
        .set_csp(csp=csp_config)
        .build()
    )
    request_2 = copy.deepcopy(request_1)
    assert request_1 == request_2


def test_mccs_configure_request_eq():
    """
    Verify that ConfigurationRequest objects for are considered equal when:
      - they point to the same target
      - their MCCS configuration is the same
    """
    # station_config = StnConfiguration(1)
    station_config = StnConfigurationBuilder().set_station_id(1).build()
    # target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    target = (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )

    # station_beam_config = SubarrayBeamConfiguration(
    #     1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    # )

    station_beam_config = (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )

    # mccs_config = MCCSConfiguration(
    #     station_configs=[station_config], subarray_beam_configs=[station_beam_config]
    # )

    mccs_config = (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )

    request_1 = ConfigureRequest(mccs=mccs_config)
    request_2 = ConfigureRequest(mccs=mccs_config)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """

    # pointing_config = PointingConfiguration(Target(1, 1))
    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
        .build()
    )

    # dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    # sdp_config = SDPConfiguration(scan_type="science_A")
    sdp_config = SDPConfigurationBuilder().set_scan_type("science_A").build()

    # csp_config = CSPConfiguration(
    #     interface="interface",
    #     subarray=SubarrayConfiguration(subarray_name="subarray name"),
    #     common=CommonConfiguration(
    #         config_id="config_id", frequency_band=ReceiverBand.BAND_1, subarray_id=1
    #     ),
    #     cbf_config=CBFConfiguration(
    #         fsp_configs=[FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)]
    #     ),
    #     pss_config=None,
    #     pst_config=None,
    # )

    csp_config = (
        CSPConfigurationBuilder()
        .set_interface("interface")
        .set_subarray(
            SubarrayConfigurationBuilder()
            .set_subarray_name(subarray_name="subarray name")
            .build()
        )
        .set_common(
            CommonConfigurationBuilder()
            .set_config_id(config_id="config_id")
            .set_frequency_band(frequency_band=ReceiverBand.BAND_1)
            .set_subarray_id(1)
            .build()
        )
        .set_cbf_config(
            CBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(fsp_id=1)
                    .set_function_mode(function_mode=FSPFunctionMode.CORR)
                    .set_frequency_slice_id(frequency_slice_id=1)
                    .set_integration_factor(integration_factor=10)
                    .set_zoom_factor(0)
                    .build()
                ]
            )
            .build()
        )
        .build()
    )

    # request = ConfigureRequest(
    #     pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    # )

    request = (
        ConfigureRequestBuilder()
        .set_pointing(pointing=pointing_config)
        .set_dish(dish=dish_config)
        .set_sdp(sdp=sdp_config)
        .set_csp(csp=csp_config)
        .build()
    )
    assert request != object


def test_mccs_configure_request_is_not_equal_to_other_objects():
    """
    Verify that an MCCS ConfigureRequest is not equal to other objects.
    """
    station_config = StnConfigurationBuilder().set_station_id(1).build()

    target = (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )
    station_beam_config = (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )
    mccs_config = (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )
    request = ConfigureRequestBuilder().set_mccs(mccs_config).build()
    assert request != object
    assert request is not None


def test_configure_request_mccs_independence():
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """
    # station_config = StnConfiguration(1)
    station_config = StnConfigurationBuilder().set_station_id(1).build()
    # target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    target = (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )

    # station_beam_config = SubarrayBeamConfiguration(
    #     1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
    # )

    station_beam_config = (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )

    mccs_config = (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )
    request = ConfigureRequestBuilder().set_mccs(mccs_config).build()
    assert request is not None

    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )
    with pytest.raises(ValueError):
        ConfigureRequestBuilder().set_dish(dish=dish_config).set_mccs(
            mccs=mccs_config
        ).build()


def test_configure_request_equals_pi16():
    """
    Verify that ConfigureRequest objects are considered equal when all
    attributes are equal and not equal when there value differ.
    """

    station_config = StnConfigurationBuilder().set_station_id(1).build()
    target = (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )

    station_beam_config = (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )

    csp_config = (
        CSPConfigurationBuilder()
        .set_interface("interface")
        .set_subarray(
            SubarrayConfigurationBuilder()
            .set_subarray_name(subarray_name="subarray name")
            .build()
        )
        .set_common(
            CommonConfigurationBuilder()
            .set_config_id(config_id="config_id")
            .set_frequency_band(frequency_band=ReceiverBand.BAND_1)
            .set_subarray_id(1)
            .build()
        )
        .set_cbf_config(
            CBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(fsp_id=1)
                    .set_function_mode(function_mode=FSPFunctionMode.CORR)
                    .set_frequency_slice_id(frequency_slice_id=1)
                    .set_integration_factor(integration_factor=10)
                    .set_zoom_factor(0)
                    .build()
                ]
            )
            .build()
        )
        .build()
    )

    sdp_config = SDPConfigurationBuilder().set_scan_type("science_A").build()
    mccs_config = (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )

    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    configure_request_obj_1 = (
        ConfigureRequestBuilder()
        .set_dish(dish=dish_config)
        .set_csp(csp=csp_config)
        .set_sdp(sdp=sdp_config)
        .build()
    )

    configure_request_obj_2 = (
        ConfigureRequestBuilder()
        .set_dish(dish=dish_config)
        .set_csp(csp=csp_config)
        .set_sdp(sdp=sdp_config)
        .build()
    )

    configure_request_obj_3 = (
        ConfigureRequestBuilder()
        .set_mccs(mccs=mccs_config)
        .set_csp(csp=csp_config)
        .set_sdp(sdp=sdp_config)
        .build()
    )
    assert configure_request_obj_1 == configure_request_obj_2
    assert configure_request_obj_1 != configure_request_obj_3


#
# def test_configure_request_not_equal_to_other_objects_pi16():
#     """
#     Verify that ConfigureRequest objects are not considered equal to objects
#     of other types.
#     """
#     configure_request_obj_1 = ConfigureRequest(**CONFIGURE_OBJECT_ARGS_PI16)
#
#     assert configure_request_obj_1 != 1
#
#
# def test_configure_request_equals_for_low():
#     """
#     Verify that ConfigureRequest objects are considered equal when all
#     attributes are equal and not equal when there value differ.
#     """
#
#     configure_request_obj_1 = ConfigureRequest(**CONFIGURE_LOW_OBJECT_ARGS)
#     configure_request_obj_2 = ConfigureRequest(**CONFIGURE_LOW_OBJECT_ARGS)
#
#     assert configure_request_obj_1 == configure_request_obj_2
#
#     alt_csp_configuration_csp_2_0_args = CONFIGURE_LOW_OBJECT_ARGS.copy()
#     alt_csp_configuration_csp_2_0_args[
#         "interface"
#     ] = "Changing interface value for creating object with different value"
#
#     configure_request_obj_3 = ConfigureRequest(**alt_csp_configuration_csp_2_0_args)
#
#     assert configure_request_obj_1 != configure_request_obj_3
#
#
# def test_configure_request_not_equal_to_other_objects_for_low():
#     """
#     Verify that ConfigureRequest objects are not considered equal to objects
#     of other types.
#     """
#     configure_request_obj_1 = ConfigureRequest(**CONFIGURE_LOW_OBJECT_ARGS)
#
#     assert configure_request_obj_1 != 1
#
#
# def test_configure_request_eq_for_low():
#     """
#     Verify that ConfigurationRequest objects for are considered equal
#     """
#     station_config = StnConfiguration(1)
#     target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
#     station_beam_config = SubarrayBeamConfiguration(
#         1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
#     )
#     mccs_config = MCCSConfiguration(
#         station_configs=[station_config], subarray_beam_configs=[station_beam_config]
#     )
#     stn_beam = {
#         "stn_beam_id": 1,
#         "freq_ids": [400],
#         "host": [[0, "192.168.1.00"]],
#         "port": [[0, 9000, 1]],
#         "mac": [[0, "02-03-04-0a-0b-0c"]],
#         "integration_ms": 849,
#     }
#     station = {
#         "stns": [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
#         "stn_beams": [StnBeamConfiguration(**stn_beam)],
#     }
#     vis_fsp = {"function_mode": "vis", "fsp_ids": [1]}
#     vis = {
#         "vis_fsp": [VisFspConfiguration(**vis_fsp)],
#         "stn_beams": [StnBeamConfiguration(**stn_beam)],
#     }
#     low_cbf = {
#         "station": StationConfiguration(**station),
#         "vis": VisConfiguration(**vis),
#     }
#
#     request_1 = ConfigureRequest(
#         interface="https://schema.skao.int/ska-low-tmc-configure/3.1",
#         transaction_id="txn-....-00001",
#         mccs=mccs_config,
#         sdp=SDPConfiguration(
#             interface="https://schema.skao.int/ska-sdp-configure/0.4",
#             scan_type="science_A",
#         ),
#         tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
#         csp=CSPConfiguration(
#             interface="https://schema.skao.int/ska-low-csp-configure/0.0",
#             common=CommonConfiguration(
#                 config_id="sbi-mvp01-20200325-00001-science_A",
#             ),
#             lowcbf=LowCBFConfiguration(low_cbf),
#         ),
#     )
#     request_2 = copy.deepcopy(request_1)
#     assert request_1 == request_2
#
#
# def test_configure_request_is_not_equal_to_other_objects_for_low():
#     """
#     Verify that  ConfigureRequest is not equal to other objects.
#     """
#     station_config = StnConfiguration(1)
#     target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
#     station_beam_config = SubarrayBeamConfiguration(
#         1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target, [1.0, 1.0, 1.0], [0.0, 0.0]
#     )
#     mccs_config = MCCSConfiguration(
#         station_configs=[station_config], subarray_beam_configs=[station_beam_config]
#     )
#
#     request = ConfigureRequest(
#         interface="https://schema.skao.int/ska-low-tmc-configure/3.1",
#         transaction_id="txn-....-00001",
#         mccs=mccs_config,
#         sdp=SDPConfiguration(
#             interface="https://schema.skao.int/ska-sdp-configure/0.4",
#             scan_type="science_A",
#         ),
#         tmc=TMCConfiguration(scan_duration=timedelta(seconds=10)),
#         csp=CSPConfiguration(
#             interface="https://schema.skao.int/ska-low-csp-configure/0.0",
#             common=CommonConfiguration(
#                 config_id="sbi-mvp01-20200325-00001-science_A",
#             ),
#             lowcbf=LowCBFConfiguration(
#                 stations=StationConfiguration(
#                     stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
#                     stn_beams=[
#                         StnBeamConfiguration(
#                             stn_beam_id=1,
#                             freq_ids=[400],
#                         )
#                     ],
#                 ),
#                 vis=VisConfiguration(
#                     fsp=VisFspConfiguration(function_mode="vis", fsp_ids=[1]),
#                     stn_beams=[
#                         StnBeamConfiguration(
#                             stn_beam_id=1,
#                             host=[[0, "192.168.1.00"]],
#                             port=[[0, 9000, 1]],
#                             mac=[[0, "02-03-04-0a-0b-0c"]],
#                             integration_ms=849,
#                         )
#                     ],
#                 ),
#             ),
#         ),
#     )
#     assert request != object
#     assert request is not None


def test_configure_partial_configuration():
    """
    Verify that a non-partial Mid ConfigureRequest requires the correct fields
    """
    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    # pointing_config = PointingConfiguration(
    #     Target(ca_offset_arcsec=5.0, ie_offset_arcsec=5.0)
    # )

    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(
            TargetBuilder()
            .set_ca_offset_arcsec(ca_offset_arcsec=5.0)
            .set_ie_offset_arcsec(ie_offset_arcsec=5.0)
            .build()
        )
        .build()
    )

    # valid_partial_request = ConfigureRequest(
    #     pointing=pointing_config,
    #     tmc=TMCConfiguration(partial_configuration=True),
    #     dish=dish_config,
    # )

    valid_partial_request = (
        ConfigureRequestBuilder()
        .set_pointing(pointing=pointing_config)
        .set_tmc(
            tmc=TMCConfigurationBuilder()
            .set_partial_configuration(partial_configuration=True)
            .build()
        )
        .set_dish(dish=dish_config)
        .build()
    )
    assert valid_partial_request is not None

    # scan_duration should be required for non-partial ConfigureRequest
    with pytest.raises(ValidationError):
        # ConfigureRequest(
        #     dish=dish_config,
        #     pointing=PointingConfiguration(
        #         Target(
        #             ra="21:08:47.92",
        #             dec="-88:57:22.9",
        #             target_name="Polaris Australis",
        #             reference_frame="icrs",
        #         )
        #     ),
        #     tmc=TMCConfiguration(partial_configuration=False),
        # )

        ConfigureRequestBuilder().set_dish(dish=dish_config).set_pointing(
            pointing=pointing_config
        ).set_tmc(
            tmc=TMCConfigurationBuilder()
            .set_partial_configuration(partial_configuration=False)
            .build()
        ).build()

    # ra and dec should be required for non-partial ConfigureRequest
    with pytest.raises(ValueError):
        # ConfigureRequest(
        #     dish=dish_config,
        #     pointing=pointing_config,
        #     tmc=TMCConfiguration(
        #         scan_duration=timedelta(10.0), partial_configuration=False
        #     ),
        # )

        ConfigureRequestBuilder().set_dish(dish=dish_config).set_pointing(
            pointing=pointing_config
        ).set_tmc(
            tmc=TMCConfigurationBuilder()
            .set_scan_duration(scan_duration=timedelta(seconds=10))
            .set_partial_configuration(partial_configuration=False)
            .build()
        ).build()
