"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""
import itertools
from contextlib import nullcontext as does_not_raise
from typing import ContextManager, NamedTuple

import pytest
from pydantic import ValidationError

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import (
    CSPConfigurationBuilder,
    FSPConfigurationBuilder,
)

MID_CSP_SCHEMA = "https://schema.skao.int/ska-csp-configurescan/4.0"
MID_CSP_SCHEMA_DEPRECATED = "https://schema.skao.int/ska-csp-configurescan/2.0"


@pytest.mark.parametrize(
    "fsp_id, expected_exception",
    [
        (0, ValueError),  # fsp_id below the valid range
        (28, ValueError),  # fsp_id above the valid range
        (1, None),  # Valid lower boundary
        (27, None),  # Valid upper boundary
    ],
)
def test_fsp_id_range_constraints(fsp_id, expected_exception):
    """
    Verify that fsp id must be in the range of 1 to 27
    """
    if expected_exception:
        with pytest.raises(expected_exception):
            FSPConfigurationBuilder(fsp_id=fsp_id)
    else:
        FSPConfigurationBuilder(fsp_id=fsp_id)


@pytest.mark.parametrize(
    "zoom_factor, expected_exception",
    [
        (-1, ValueError),  # Invalid zoom_factor below range
        (7, ValueError),  # Invalid zoom_factor above range
        (0, None),  # Valid zoom_factor at lower bound
        (6, None),  # Valid zoom_factor at upper bound
    ],
)
def test_fsp_zoom_factor_range(zoom_factor, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            FSPConfigurationBuilder(zoom_factor=zoom_factor)
    else:
        FSPConfigurationBuilder(zoom_factor=zoom_factor)


@pytest.mark.parametrize(
    "integration_factor, expected_exception",
    [
        (1, None),  # Valid integration_factor at lower bound
        (10, None),  # Valid integration_factor at upper bound
        (0, ValueError),  # Invalid integration_factor below range
        (11, ValueError),  # Invalid integration_factor above range
    ],
)
def test_fsp_integration_factor_range(integration_factor, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            FSPConfigurationBuilder(integration_factor=integration_factor)
    else:
        FSPConfigurationBuilder(integration_factor=integration_factor)


@pytest.mark.parametrize(
    "channel_avg_map_length, expected_exception",
    [
        (20, None),  # Assuming 20 entries are valid
        (
            21,
            ValueError,
        ),  # Invalid number of entries, assuming more than 20 is invalid
    ],
)
def test_fsp_configuration_channel_avg_map_length(
    channel_avg_map_length, expected_exception
):
    channel_avg_map = list(
        zip(itertools.count(1, 744), [0] * channel_avg_map_length)
    )
    if expected_exception:
        with pytest.raises(expected_exception):
            FSPConfigurationBuilder(channel_averaging_map=channel_avg_map)
    else:
        FSPConfigurationBuilder(channel_averaging_map=channel_avg_map)


class ValidationCase(NamedTuple):
    args: dict
    expected: ContextManager


INTERFACE_VALIDATION_CASES = (
    ValidationCase(
        args={
            "interface": MID_CSP_SCHEMA,
            "subarray_id": 1,
        },
        expected=pytest.raises(ValidationError),
    ),
    ValidationCase(
        args={
            "interface": MID_CSP_SCHEMA,
            "config_id": None,
        },
        expected=pytest.raises(ValidationError),
    ),
    ValidationCase(
        args={
            "interface": MID_CSP_SCHEMA_DEPRECATED,
            "subarray_id": None,
        },
        expected=pytest.raises(ValidationError),
    ),
    ValidationCase(
        args={"interface": MID_CSP_SCHEMA_DEPRECATED, "subarray_id": 1},
        expected=does_not_raise(),
    ),
)


@pytest.mark.parametrize(("args, expected"), INTERFACE_VALIDATION_CASES)
def test_interface_validation(args, expected):
    with expected:
        CSPConfigurationBuilder(**args)
