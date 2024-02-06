"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import copy
from datetime import timedelta

import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.subarray_node.configure import LOW_SCHEMA, MID_SCHEMA
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure import (
    ConfigureRequestBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import (
    PointingConfigurationBuilder,
    TargetBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.tmc import (
    TMCConfigurationBuilder,
)


def test_empty_configure_request_fails():
    """
    Verify that an empty ConfigureRequest without dish, mccs or interface set throws a ValueError
    """
    with pytest.raises(ValueError):
        _ = ConfigureRequestBuilder().build()


@pytest.mark.parametrize(
    "config_name, setter_method, expected_schema",
    [
        ("mccs_config", "set_mccs", LOW_SCHEMA),
        ("dish_config", "set_dish", MID_SCHEMA),
    ],
)
def test_configure_request_has_correct_schema_on_creation(
    request, config_name, setter_method, expected_schema
):
    """
    Verify that ConfigureRequest with valid DishConfiguration has a MID Schema set on creation
    And Low Schema set on creation for MCCS Configuration
    """
    config = request.getfixturevalue(config_name)
    builder = ConfigureRequestBuilder()
    getattr(builder, setter_method)(config)
    request_obj = builder.build()
    assert request_obj.interface == expected_schema


@pytest.mark.parametrize(
    "config_type, is_equal, use_deepcopy",
    [
        (
            "dish",
            True,
            False,
        ),  # Test equality for ConfigureRequests with dish, sdp, and csp configs
        ("mccs", True, False),  # Test equality for ConfigureRequests with mccs config
        ("other_objects", False, True),  # Test inequality against other object types
    ],
)
def test_configure_request_equality(
    config_type,
    is_equal,
    use_deepcopy,
    dish_config,
    sdp_config,
    csp_config,
    mccs_config,
):
    """
    Verify that ConfigureRequests are equal when they have the same values, not equal for different values
    And that ConfigureRequests are not considered equal to objects of other types.
    """
    # Initialize pointing based on config_type
    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
        .build()
    )

    # Initialize request based on config_type
    if config_type == "dish":
        request = (
            ConfigureRequestBuilder()
            .set_pointing(pointing=pointing_config)
            .set_dish(dish=dish_config)
            .set_sdp(sdp=sdp_config)
            .set_csp(csp=csp_config)
            .build()
        )
        request_2 = copy.deepcopy(request) if use_deepcopy else request
    elif config_type == "mccs":
        request = (
            ConfigureRequestBuilder()
            .set_mccs(mccs=mccs_config)
            .set_sdp(sdp=sdp_config)
            .set_csp(csp=csp_config)
            .build()
        )
        request_2 = copy.deepcopy(request) if use_deepcopy else request
    else:  # For testing inequality with other objects
        request = (
            ConfigureRequestBuilder()
            .set_pointing(pointing=pointing_config)
            .set_dish(dish=dish_config)
            .set_sdp(sdp=sdp_config)
            .set_csp(csp=csp_config)
            .build()
        )
        request_2 = object()

    if is_equal:
        assert request == request_2
    else:
        assert request != request_2


def test_configure_request_mccs_independence(mccs_config, dish_config):
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """

    with pytest.raises(ValueError):
        ConfigureRequestBuilder().set_dish(dish=dish_config).set_mccs(
            mccs=mccs_config
        ).build()


#


def test_configure_partial_configuration(dish_config):
    """
    Verify that a non-partial Mid ConfigureRequest requires the correct fields
    """

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
