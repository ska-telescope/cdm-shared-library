"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import pytest
import itertools

from ska.cdm.messages.subarray_node.configure import ConfigureRequest
from ska.cdm.messages.subarray_node.configure.core import (
    PointingConfiguration,
    DishConfiguration,
    Target,
    ReceiverBand,
)
from ska.cdm.messages.subarray_node.configure.csp import (
    FSPConfiguration,
    FSPFunctionMode,
    CSPConfiguration,
)
from ska.cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    StnBeamConfiguration,
)


def test_configure_request_eq():
    """
    Verify that ConfigurationRequest objects are considered equal when:
      - they point to the same target
      - they set the same receiver band
      - their SDP configuration is the same
      - their CSP configuration is the same
    """

    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration("science_A")
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    request_1 = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
    request_2 = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
    assert request_1 == request_2


def test_mccs_configure_request_eq():
    """
    Verify that ConfigurationRequest objects for are considered equal when:
      - they point to the same target
      - their MCCS configuration is the same
    """
    station_config = StnConfiguration(1)
    print(station_config)
    station_beam_config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )
    mccs_config = MCCSConfiguration([station_config], [station_beam_config])
    request_1 = ConfigureRequest(mccs=mccs_config)
    request_2 = ConfigureRequest(mccs=mccs_config)
    assert request_1 == request_2


def test_configure_request_is_not_equal_to_other_objects():
    """
    Verify that ConfigureRequest is not equal to other objects.
    """
    pointing_config = PointingConfiguration(Target(1, 1))
    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    sdp_config = SDPConfiguration("science_A")
    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    request = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
    assert request != object


def test_mccs_configure_request_is_not_equal_to_other_objects():
    """
    Verify that an MCCS ConfigureRequest is not equal to other objects.
    """
    station_config = StnConfiguration(1)
    station_beam_config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )
    mccs_config = MCCSConfiguration([station_config], [station_beam_config])
    request = ConfigureRequest(mccs=mccs_config)
    assert request != object
    assert request is not None


def test_configure_request_mccs_independence():
    """
    Verify that an Mid & Low ConfigureRequests are independent.
    """
    station_config = StnConfiguration(1)
    station_beam_config = StnBeamConfiguration(
        1, [1, 2], [1, 2, 3, 4, 5, 6], 1.0, [0.1, 182.0, 0.5, 45.0, 1.6]
    )
    mccs_config = MCCSConfiguration([station_config], [station_beam_config])
    request = ConfigureRequest(mccs=mccs_config)
    assert request is not None

    dish_config = DishConfiguration(receiver_band=ReceiverBand.BAND_1)
    with pytest.raises(ValueError):
        ConfigureRequest(dish=dish_config, mccs=mccs_config)

    sdp_config = SDPConfiguration("science_A")
    with pytest.raises(ValueError):
        ConfigureRequest(dish=dish_config, sdp=sdp_config, mccs=mccs_config)

    channel_avg_map = list(zip(itertools.count(1, 744), [2] + 19 * [0]))
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 140, 0, channel_avg_map)
    csp_config = CSPConfiguration(csp_id, ReceiverBand.BAND_1, [fsp_config])
    with pytest.raises(ValueError):
        ConfigureRequest(
            dish=dish_config, sdp=sdp_config, csp=csp_config, mccs=mccs_config
        )
