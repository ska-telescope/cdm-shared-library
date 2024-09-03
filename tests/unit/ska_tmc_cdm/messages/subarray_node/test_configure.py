"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import pytest
from pydantic import ValidationError

from ska_tmc_cdm.messages.subarray_node.configure import (
    LOW_SCHEMA,
    MID_SCHEMA,
    ConfigureRequest,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import (
    DishConfigurationBuilder,
    PointingConfigurationBuilder,
    SpecialTargetBuilder,
    TargetBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    MCCSConfigurationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.tmc import (
    TMCConfigurationBuilder,
)


def test_empty_configure_request_fails():
    """
    Verify that an empty ConfigureRequest without dish, mccs or interface set throws a ValueError
    """
    with pytest.raises(ValueError):
        ConfigureRequest()


@pytest.mark.parametrize(
    "configure_request, expected_schema",
    [
        (ConfigureRequest(mccs=MCCSConfigurationBuilder()), LOW_SCHEMA),
        (ConfigureRequest(dish=DishConfigurationBuilder()), MID_SCHEMA),
    ],
)
def test_configure_request_has_correct_schema_on_creation(
    configure_request, expected_schema
):
    """
    Verify that ConfigureRequest with valid DishConfiguration has a MID Schema set on creation
    And Low Schema set on creation for MCCS Configuration
    """
    assert configure_request.interface == expected_schema


@pytest.mark.parametrize(
    "request1,request2,is_equal",
    [
        (
            ConfigureRequest(dish=DishConfigurationBuilder()),
            ConfigureRequest(dish=DishConfigurationBuilder()),
            True,
        ),  # Test equality for ConfigureRequests with dish
        (
            ConfigureRequest(mccs=MCCSConfigurationBuilder()),
            ConfigureRequest(mccs=MCCSConfigurationBuilder()),
            True,
        ),  # Test equality for ConfigureRequests with mccs config
        (
            ConfigureRequest(mccs=MCCSConfigurationBuilder()),
            object(),
            False,
        ),  # Test inequality against other object types
    ],
)
def test_configure_request_equality(request1, request2, is_equal):
    """
    Verify that ConfigureRequests are equal when they have the same values, not equal for different values
    And that ConfigureRequests are not considered equal to objects of other types.
    """
    assert (request1 == request2) == is_equal


def test_configure_request_mccs_independence():
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """

    with pytest.raises(ValueError):
        ConfigureRequest(
            dish=DishConfigurationBuilder(), mccs=MCCSConfigurationBuilder()
        )


def test_configure_partial_configuration():
    """
    Verify that a non-partial Mid ConfigureRequest requires the correct fields
    """

    ConfigureRequest(
        pointing=PointingConfigurationBuilder(
            target=TargetBuilder(ra=None, dec=None)
        ),
        tmc=TMCConfigurationBuilder(partial_configuration=True),
        dish=DishConfigurationBuilder(),
    )

    ConfigureRequest(
        dish=DishConfigurationBuilder(),
        pointing=PointingConfigurationBuilder(target=SpecialTargetBuilder()),
        tmc=TMCConfigurationBuilder(partial_configuration=False),
    )

    # scan_duration should be required for non-partial ConfigureRequest
    with pytest.raises(ValidationError):
        ConfigureRequest(
            tmc=TMCConfigurationBuilder(
                scan_duration=None, partial_configuration=False
            ),
            dish=DishConfigurationBuilder(),
            pointing=PointingConfigurationBuilder(),
        )

    # ra and dec should be required for non-partial ConfigureRequest
    with pytest.raises(ValueError):
        ConfigureRequest(
            pointing=PointingConfigurationBuilder(
                target=TargetBuilder(ra=None, dec=None)
            ),
            tmc=TMCConfigurationBuilder(partial_configuration=False),
            ish=DishConfigurationBuilder(),
        )
