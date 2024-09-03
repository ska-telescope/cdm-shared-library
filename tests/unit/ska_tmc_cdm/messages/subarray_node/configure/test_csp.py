"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""
import copy
import itertools

import pytest

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import FSPFunctionMode
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import (
    CBFConfigurationBuilder,
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    FSPConfigurationBuilder,
    LowCBFConfigurationBuilder,
    StationConfigurationBuilder,
    StnBeamConfigurationBuilder,
    SubarrayConfigurationBuilder,
    VisConfigurationBuilder,
    VisFspConfigurationBuilder,
)


@pytest.mark.parametrize(
    "common_config_a, common_config_b, is_equal",
    [
        # Case when both configurations are identical
        (
            CommonConfigurationBuilder(),
            CommonConfigurationBuilder(),
            True,
        ),
        # Different frequency band
        (
            CommonConfigurationBuilder(frequency_band=ReceiverBand.BAND_1),
            CommonConfigurationBuilder(frequency_band=ReceiverBand.BAND_2),
            False,
        ),
        # Different subarray ID
        (
            CommonConfigurationBuilder(subarray_id=1),
            CommonConfigurationBuilder(subarray_id=2),
            False,
        ),
        # Missing band_5_tuning in second configuration
        (
            CommonConfigurationBuilder(band_5_tuning=[5.85, 7.25]),
            CommonConfigurationBuilder(band_5_tuning=None),
            False,
        ),
    ],
)
def test_common_configuration_equality(
    common_config_a, common_config_b, is_equal
):
    """
    Verify that CommonConfiguration objects are equal when they have the same values
    ,not equal when any attribute differs and not equal to other objects.
    """
    assert (common_config_a == common_config_b) == is_equal
    assert common_config_a != 1
    assert common_config_a != object


@pytest.mark.parametrize(
    "subarray_config_a, subarray_config_b, is_equal",
    [
        # Case when both configurations have the same subarray name
        (
            SubarrayConfigurationBuilder(),
            SubarrayConfigurationBuilder(),
            True,
        ),
        # Case when configurations have different subarray names
        (
            SubarrayConfigurationBuilder(subarray_name="Test Subarray"),
            SubarrayConfigurationBuilder(subarray_name="Test Subarray2"),
            False,
        ),
    ],
)
def test_subarray_configuration_equality(
    subarray_config_a, subarray_config_b, is_equal
):
    """
    Verify that SubarrayConfiguration objects are equal when they have the same subarray name
    and not equal when subarray names differ.
    """
    assert (subarray_config_a == subarray_config_b) == is_equal
    assert subarray_config_a != 1
    assert subarray_config_b != object


@pytest.mark.parametrize(
    "cbf_config_a, cbf_config_b, is_equal",
    [
        # Case when both configurations have the same FSP configuration
        (
            CBFConfigurationBuilder(fsp=[FSPConfigurationBuilder()]),
            CBFConfigurationBuilder(fsp=[FSPConfigurationBuilder()]),
            True,
        ),
        # Case when configurations have different FSP configurations
        (
            CBFConfigurationBuilder(fsp=[FSPConfigurationBuilder(fsp_id=1)]),
            CBFConfigurationBuilder(fsp=[FSPConfigurationBuilder(fsp_id=2)]),
            False,
        ),
    ],
)
def test_cbf_configuration_equality(cbf_config_a, cbf_config_b, is_equal):
    """
    Verify that CBFConfiguration objects are equal when they have the same FSP configurations
    and not equal when FSP configurations differ.
    """
    assert (cbf_config_a == cbf_config_b) == is_equal
    assert cbf_config_a != 1
    assert cbf_config_b != object()


@pytest.mark.parametrize(
    "fsp_config_a, fsp_config_b, is_equal",
    [
        # both configurations are the same
        (
            FSPConfigurationBuilder(),
            FSPConfigurationBuilder(),
            True,
        ),
        # Cases when one attribute differs, making configurations not equal
        (
            FSPConfigurationBuilder(fsp_id=1),
            FSPConfigurationBuilder(fsp_id=2),
            False,
        ),
        (
            FSPConfigurationBuilder(function_mode=FSPFunctionMode.CORR),
            FSPConfigurationBuilder(function_mode=FSPFunctionMode.PSS_BF),
            False,
        ),
        (
            FSPConfigurationBuilder(frequency_slice_id=1),
            FSPConfigurationBuilder(frequency_slice_id=2),
            False,
        ),
        (
            FSPConfigurationBuilder(integration_factor=10),
            FSPConfigurationBuilder(integration_factor=2),
            False,
        ),
        (
            FSPConfigurationBuilder(zoom_factor=0),
            FSPConfigurationBuilder(zoom_factor=1),
            False,
        ),
        (
            FSPConfigurationBuilder(
                channel_averaging_map=list(
                    zip(itertools.count(1, 744), 20 * [0])
                )
            ),
            FSPConfigurationBuilder(
                channel_averaging_map=list(
                    zip(itertools.count(1, 744), 20 * [1])
                )
            ),
            False,
        ),
    ],
)
def test_fsp_configuration_equality(fsp_config_a, fsp_config_b, is_equal):
    """
    Verify that FSPConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (fsp_config_a == fsp_config_b) == is_equal
    assert fsp_config_a != 1
    assert fsp_config_a != object()


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


@pytest.mark.parametrize(
    "stn_beam_config_a, stn_beam_config_b, is_equal",
    [
        # Case where both configurations are the same
        (
            StnBeamConfigurationBuilder(),
            StnBeamConfigurationBuilder(),
            True,
        ),
        # Case where configurations are different
        (
            StnBeamConfigurationBuilder(stn_beam_id=1),
            StnBeamConfigurationBuilder(stn_beam_id=2),
            False,
        ),
    ],
)
def test_stn_beam_configuration_equality(
    stn_beam_config_a, stn_beam_config_b, is_equal
):
    """
    Verify that StnBeamConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (stn_beam_config_a == stn_beam_config_b) == is_equal
    assert stn_beam_config_a != 1
    assert stn_beam_config_b != object


@pytest.mark.parametrize(
    "station_config_a, station_config_b, is_equal",
    [
        # Case where both configurations are the same
        (
            StationConfigurationBuilder(),
            StationConfigurationBuilder(),
            True,
        ),
        # Case where configurations are different due to missing stn_beams
        (
            StationConfigurationBuilder(
                stn_beams=(StnBeamConfigurationBuilder(),)
            ),
            StationConfigurationBuilder(stn_beams=None),
            False,
        ),
    ],
)
def test_station_configuration_equality(
    station_config_a, station_config_b, is_equal
):
    """
    Verify that StationConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (station_config_a == station_config_b) == is_equal
    assert station_config_a != 1
    assert station_config_b != object


@pytest.mark.parametrize(
    "vis_fsp_config_a, vis_fsp_config_b, is_equal",
    [
        # Case where both configurations are the same
        (
            VisFspConfigurationBuilder(),
            VisFspConfigurationBuilder(),
            True,
        ),
        # Case where configurations are different due to missing fsp_ids in the second instance
        (
            VisFspConfigurationBuilder(fsp_ids=[1, 2]),
            VisFspConfigurationBuilder(fsp_ids=None),
            False,
        ),
    ],
)
def test_vis_fsp_configuration_equality(
    vis_fsp_config_a, vis_fsp_config_b, is_equal
):
    """
    Verify that VisFspConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (vis_fsp_config_a == vis_fsp_config_b) == is_equal
    assert (
        vis_fsp_config_a != 1
    )  # Additional check to ensure VisFspConfiguration objects are not equal to objects of other types.
    assert vis_fsp_config_b != object


@pytest.mark.parametrize(
    "vis_config_a, vis_config_b, is_equal",
    [
        (
            VisConfigurationBuilder(),
            VisConfigurationBuilder(),
            True,
        )
    ],
)
def test_vis_configuration_equality(vis_config_a, vis_config_b, is_equal):
    """
    Verify that VisConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (vis_config_a == vis_config_b) == is_equal
    assert (
        vis_config_a != 1
    )  # Additional check to ensure VisConfiguration objects are not equal to objects of other types.
    assert vis_config_b != object


@pytest.mark.parametrize(
    "low_cbf_config_a, low_cbf_config_b, is_equal",
    [
        # Case where both LowCBFConfiguration objects are exactly the same
        (
            LowCBFConfigurationBuilder(),
            LowCBFConfigurationBuilder(),
            True,
        ),
    ],
)
def test_low_cbf_configuration_equality(
    low_cbf_config_a, low_cbf_config_b, is_equal
):
    """
    Verify that LowCBFConfiguration objects are equal when they have the same values
    and not equal when any attribute differs.
    """
    assert (low_cbf_config_a == low_cbf_config_b) == is_equal
    assert low_cbf_config_a != 1
    assert low_cbf_config_b != object()


def test_csp_configuration_equality(csp_config):
    """
    Verify that CSPConfiguration objects are equal when all they have the same values
    and not equal when any attribute differs.
    """

    low_csp_config = CSPConfigurationBuilder(
        interface="https://schema.skao.int/ska-low-csp-configure/0.0",
        common=CommonConfigurationBuilder(),
        pst_config=PSTConfigurationBuilder(),
        lowcbf=LowCBFConfigurationBuilder(
            vis=VisConfigurationBuilder(),
            stations=StationConfigurationBuilder(
                stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
                stn_beams=[
                    StnBeamConfigurationBuilder(
                        stn_beam_id=1, freq_ids=[400], beam_id=1
                    )
                ],
            ),
        ),
    )

    csp_config_invalid = CSPConfigurationBuilder(interface="foo")
    csp_config_b = copy.deepcopy(csp_config)
    assert (
        csp_config == csp_config_b
    )  # comparing same instance created using deepcopy
    assert csp_config != csp_config_invalid  # comparing with invalid instance
    assert csp_config != 1  # comparing with other instance

    assert low_csp_config == copy.deepcopy(
        low_csp_config
    )  # comparing same instance created using deepcopy
    assert (
        low_csp_config != csp_config_invalid
    )  # comparing with invalid instance
    assert low_csp_config != 1  # comparing with other instance

    assert csp_config != low_csp_config  # comparing mid with low
    assert csp_config != object  # comparing with object
    assert low_csp_config != object  # comparing with object
