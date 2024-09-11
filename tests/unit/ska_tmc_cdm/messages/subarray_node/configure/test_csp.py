"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""

import copy
import itertools
from contextlib import nullcontext as does_not_raise
from typing import NamedTuple, Optional

import pytest

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CorrelationConfiguration,
    FSPFunctionMode,
    ProcessingRegionConfiguration,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import (
    CBFConfigurationBuilder,
    CommonConfiguration,
    CommonConfigurationBuilder,
    CSPConfiguration,
    CSPConfigurationBuilder,
    FSPConfigurationBuilder,
    LowCBFConfigurationBuilder,
    MidCBFConfigurationBuilder,
    StationConfigurationBuilder,
    StnBeamConfigurationBuilder,
    SubarrayConfigurationBuilder,
    VisConfigurationBuilder,
    VisFspConfigurationBuilder,
)


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
    expected_error: Optional[Exception]


INTERFACE_VALIDATION_CASES = (
    ValidationCase(
        args={
            "interface": "https://schema.skao.int/ska-csp-configure/4.0",
            "subarray_id": 1,
        },
        expected_error=KeyError,
    ),
)


@pytest.mark.parametrize(("args, expected_error"), INTERFACE_VALIDATION_CASES)
def test_interface_validation(args, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            MidCBFConfiguration(**args)
    else:
        MidCBFConfiguration(**args)


def test_interface_validation():
    """
    Verify the interface validation.
    """
    csp = (
        CSPConfiguration(
            interface="https://schema.skao.int/ska-csp-configure/4.0",
            common=CommonConfiguration(
                config_id="sbi-mvp01-20200325-00001-science_A",
                frequency_band=ReceiverBand.BAND_1,
            ),
            midcbf=MidCBFConfiguration(
                frequency_band_offset_stream1=80,
                frequency_band_offset_stream2=80,
                correlation=CorrelationConfiguration(
                    processing_regions=[
                        ProcessingRegionConfiguration(
                            fsp_ids=[1, 2, 3, 4],
                            receptors=["SKA063", "SKA001", "SKA100"],
                            start_freq=350000000,
                            channel_width=13440,
                            channel_count=52080,
                            sdp_start_channel_id=0,
                            integration_factor=1,
                        )
                    ]
                ),
                vlbi_config={},
            ),
        ),
    )
    expected = CSPConfiguration(
        interface="https://schema.skao.int/ska-csp-configure/4.0",
        common=CommonConfiguration(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
        ),
        midcbf=MidCBFConfiguration(
            frequency_band_offset_stream1=80,
            frequency_band_offset_stream2=80,
            correlation=CorrelationConfiguration(
                processing_regions=[
                    ProcessingRegionConfiguration(
                        fsp_ids=[1, 2, 3, 4],
                        receptors=["SKA063", "SKA001", "SKA100"],
                        start_freq=350000000,
                        channel_width=13440,
                        channel_count=52080,
                        sdp_start_channel_id=0,
                        integration_factor=1,
                    )
                ]
            ),
            vlbi_config={},
        ),
    )
    assert expected == repr(csp)
