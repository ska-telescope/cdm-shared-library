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

    assert request.interface is not None
    assert request.interface == LOW_SCHEMA


def test_configure_request_with_dish_has_mid_interface_set_on_creation():
    """
    Verify that ConfigureRequest with valid DishConfiguration has a MID Schema set on creation
    """
    config_1 = (
        DishConfigurationBuilder()
        .set_receiver_band(receiver_band=ReceiverBand.BAND_1)
        .build()
    )

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
    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
        .build()
    )

    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    sdp_config = SDPConfigurationBuilder().set_scan_type("science_A").build()

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

    request_1 = ConfigureRequest(mccs=mccs_config)
    request_2 = ConfigureRequest(mccs=mccs_config)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """

    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
        .build()
    )

    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )

    sdp_config = SDPConfigurationBuilder().set_scan_type("science_A").build()

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


def test_configure_partial_configuration():
    """
    Verify that a non-partial Mid ConfigureRequest requires the correct fields
    """
    dish_config = (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )
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
        ConfigureRequestBuilder().set_dish(dish=dish_config).set_pointing(
            pointing=pointing_config
        ).set_tmc(
            tmc=TMCConfigurationBuilder()
            .set_partial_configuration(partial_configuration=False)
            .build()
        ).build()

    # ra and dec should be required for non-partial ConfigureRequest
    with pytest.raises(ValueError):

        ConfigureRequestBuilder().set_dish(dish=dish_config).set_pointing(
            pointing=pointing_config
        ).set_tmc(
            tmc=TMCConfigurationBuilder()
            .set_scan_duration(scan_duration=timedelta(seconds=10))
            .set_partial_configuration(partial_configuration=False)
            .build()
        ).build()
