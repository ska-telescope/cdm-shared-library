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
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.__init__ import (
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


def test_configure_request_eq(dish_config, sdp_config, csp_config):
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


def test_mccs_configure_request_eq(mccs_config):
    """
    Verify that ConfigurationRequest objects for are considered equal when:
      - their MCCS configuration is the same
    """

    request_1 = ConfigureRequest(mccs=mccs_config)
    request_2 = ConfigureRequest(mccs=mccs_config)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects(
    dish_config, sdp_config, csp_config
):
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = (
        PointingConfigurationBuilder()
        .set_target(TargetBuilder().set_ra(1).set_dec(1).build())
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


def test_mccs_configure_request_is_not_equal_to_other_objects(mccs_config):
    """
    Verify that an MCCS ConfigureRequest is not equal to other objects.
    """

    request = ConfigureRequestBuilder().set_mccs(mccs_config).build()
    assert request != object
    assert request is not None


def test_configure_request_mccs_independence(mccs_config, dish_config):
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """

    request = ConfigureRequestBuilder().set_mccs(mccs_config).build()
    assert request is not None

    with pytest.raises(ValueError):
        ConfigureRequestBuilder().set_dish(dish=dish_config).set_mccs(
            mccs=mccs_config
        ).build()


def test_configure_request_equals_pi16(
    mccs_config,
    csp_config,
    sdp_config,
    dish_config,
):
    """
    Verify that ConfigureRequest objects are considered equal when all
    attributes are equal and not equal when there value differ.
    """

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
