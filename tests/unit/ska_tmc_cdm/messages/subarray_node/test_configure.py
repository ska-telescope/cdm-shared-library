"""
Unit tests for the SubarrayNode.Configure request/response mapper module.
"""
import pytest

from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    PointingConfiguration,
    DishConfiguration,
    Target,
    ReceiverBand,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration
)
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget
)
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration


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
    sdp_config = SDPConfiguration(scan_type="science_A")
    csp_config = CSPConfiguration(
        interface="interface",
        subarray_config=SubarrayConfiguration(
            subarray_name="subarray name"
        ),
        common_config=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
            ]
        ),
        pss_config=None,
        pst_config=None,
    )
    request_1 = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
    request_2 = ConfigureRequest(
        pointing=pointing_config, dish=dish_config, sdp=sdp_config, csp=csp_config
    )
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
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[station_beam_config]
    )
    request_1 = ConfigureRequest(
        interface='https://schema.skatelescope.org/ska-low-tmc-configure/1.0',
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A")
    )
    request_2 = ConfigureRequest(
        interface='https://schema.skatelescope.org/ska-low-tmc-configure/1.0',
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A")
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
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[station_beam_config]
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
        subarray_config=SubarrayConfiguration(
            subarray_name="subarray name"
        ),
        common_config=CommonConfiguration(
            config_id="config_id",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1
        ),
        cbf_config=CBFConfiguration(
            fsp_configs=[
                FSPConfiguration(1, FSPFunctionMode.CORR, 1, 10, 0)
            ]
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
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[station_beam_config]
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
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[station_beam_config]
    )
    request = ConfigureRequest(
        interface='https://schema.skatelescope.org/ska-low-tmc-configure/1.0',
        mccs=mccs_config,
        sdp=SDPConfiguration(scan_type="science_A")
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
        1, [1, 2], [[1, 2, 3, 4, 5, 6]], 1.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    mccs_config = MCCSConfiguration(
        station_configs=[station_config],
        subarray_beam_configs=[station_beam_config]
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
