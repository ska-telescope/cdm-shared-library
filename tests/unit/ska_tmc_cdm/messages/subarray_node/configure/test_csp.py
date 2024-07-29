"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.csp module.
"""
import copy
import itertools

import pytest

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import (
    BeamsConfigurationBuilder,
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    FSPConfigurationBuilder,
    LowCBFConfigurationBuilder,
    MidCBFConfigurationBuilder,
    StationConfigurationBuilder,
    StnBeamConfigurationBuilder,
    TimingBeamsConfigurationBuilder,
    VisConfigurationBuilder,
    VisFspConfigurationBuilder,
    VisStnBeamConfigurationBuilder,
)

tr = (
    TimingBeamsConfigurationBuilder()
    .set_beams(
        [
            BeamsConfigurationBuilder()
            .set_pst_beam_id(1)
            .set_stn_beam_id(1)
            .set_stn_weights([0.9, 1.0, 1.0, 1.0, 0.9, 1.0])
            .build()
        ]
    )
    .set_fsp(
        VisFspConfigurationBuilder()
        .set_fsp_ids([2])
        .set_firmware("pst")
        .build()
    )
    .build()
)


@pytest.mark.parametrize(
    "common_config_a, common_config_b, is_equal",
    [
        # Case when both configurations are identical
        (
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp01-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5A)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
            .build(),
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp01-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5A)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
            .build(),
            True,
        ),
        # Different frequency band
        (
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp02-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5A)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
            .build(),
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp02-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5B)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
            .build(),
            False,
        ),
        # Different subarray ID
        (
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp03-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5A)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
            .build(),
            CommonConfigurationBuilder()
            .set_config_id("sbi-mvp03-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_5A)
            .set_subarray_id(2)  # Different subarray ID
            .set_band_5_tuning([5.85, 7.25])
            .build(),
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
    "cbf_config_a, cbf_config_b, is_equal",
    [
        # Case when both configurations have the same FSP configuration
        (
            MidCBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(1)
                    .set_integration_factor(10)
                    .build()
                ]
            )
            .build(),
            MidCBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(1)
                    .set_integration_factor(10)
                    .build()
                ]
            )
            .build(),
            True,
        ),
        # Case when configurations have different FSP configurations
        (
            MidCBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(1)
                    .set_integration_factor(10)
                    .build()
                ]
            )
            .build(),
            MidCBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(1)
                    .set_integration_factor(10)
                    .build(),
                    FSPConfigurationBuilder()
                    .set_fsp_id(2)  # Different FSP ID
                    .set_integration_factor(10)
                    .build(),
                ]
            )
            .build(),
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
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .set_channel_averaging_map(
                list(zip(itertools.count(1, 744), 20 * [0]))
            )
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .set_channel_averaging_map(
                list(zip(itertools.count(1, 744), 20 * [0]))
            )
            .build(),
            True,
        ),
        # Cases when one attribute differs, making configurations not equal
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            FSPConfigurationBuilder()
            .set_integration_factor(10)
            .set_fsp_id(2)  # Different FSP ID
            .build(),
            False,
        ),
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            False,
        ),
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            False,
        ),
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(2)  # Different integration factor
            .build(),
            False,
        ),
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .build(),
            False,
        ),
        (
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .set_channel_averaging_map(
                list(zip(itertools.count(1, 744), 20 * [0]))
            )
            .build(),
            FSPConfigurationBuilder()
            .set_fsp_id(1)
            .set_integration_factor(10)
            .set_channel_averaging_map(
                list(zip(itertools.count(1, 744), 20 * [1]))
            )  # Different channel averaging map
            .build(),
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
def test_fsp_id_range_with_builder(fsp_id, expected_exception):
    """
    Verify that fsp id is in the range of 1 to 27 using the FSPConfigurationBuilder.
    """
    if expected_exception:
        with pytest.raises(expected_exception):
            FSPConfigurationBuilder().set_fsp_id(
                fsp_id
            ).set_integration_factor(10).build()
    else:
        try:
            FSPConfigurationBuilder().set_fsp_id(
                fsp_id
            ).set_integration_factor(10).build()
        except ValueError:
            pytest.fail(f"FSP ID {fsp_id} raised ValueError unexpectedly.")


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
    builder = FSPConfigurationBuilder().set_fsp_id(1)
    if expected_exception:
        with pytest.raises(expected_exception):
            builder.set_integration_factor(integration_factor).build()
    else:
        config = builder.set_integration_factor(integration_factor).build()
        assert (
            config.integration_factor == integration_factor
        )  # Verifies the integration_factor is set as expected


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
    builder = (
        FSPConfigurationBuilder()
        .set_fsp_id(1)
        .set_integration_factor(10)
        .set_channel_averaging_map(channel_avg_map)
    )

    if expected_exception:
        with pytest.raises(expected_exception):
            builder.build()
    else:
        config = builder.build()
        assert len(config.channel_averaging_map) == channel_avg_map_length


@pytest.mark.parametrize(
    "stn_beam_config_a, stn_beam_config_b, is_equal",
    [
        # Case where both configurations are the same
        (
            StnBeamConfigurationBuilder()
            .set_stn_beam_id(1)
            .set_beam_id(1)
            .set_freq_ids([400])
            .set_delay_poly("tango/device/instance/delay")
            .build(),
            StnBeamConfigurationBuilder()
            .set_stn_beam_id(1)
            .set_beam_id(1)
            .set_freq_ids([400])
            .set_delay_poly("tango/device/instance/delay")
            .build(),
            True,
        ),
        # Case where configurations are different
        (
            StnBeamConfigurationBuilder()
            .set_stn_beam_id(1)
            .set_beam_id(1)
            .set_freq_ids([400])
            .set_delay_poly("tango/device/instance/delay")
            .build(),
            StnBeamConfigurationBuilder()
            .set_stn_beam_id(2)  # Different stn_beam_id
            .set_beam_id(2)
            .set_freq_ids([400])
            .set_delay_poly("tango/device/instance/delay")
            .build(),
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
            StationConfigurationBuilder()
            .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
            .set_stn_beams(
                [
                    StnBeamConfigurationBuilder()
                    .set_stn_beam_id(1)
                    .set_beam_id(1)
                    .set_freq_ids([400])
                    .set_delay_poly("tango/device/instance/delay")
                    .build()
                ]
            )
            .build(),
            StationConfigurationBuilder()
            .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
            .set_stn_beams(
                [
                    StnBeamConfigurationBuilder()
                    .set_stn_beam_id(1)
                    .set_beam_id(1)
                    .set_freq_ids([400])
                    .set_delay_poly("tango/device/instance/delay")
                    .build()
                ]
            )
            .build(),
            True,
        ),
        # Case where configurations are different due to missing stn_beams
        (
            StationConfigurationBuilder()
            .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
            .set_stn_beams(
                [
                    StnBeamConfigurationBuilder()
                    .set_stn_beam_id(1)
                    .set_beam_id(1)
                    .set_freq_ids([400])
                    .set_delay_poly("tango/device/instance/delay")
                    .build()
                ]
            )
            .build(),
            StationConfigurationBuilder()
            .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
            .build(),
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
            VisFspConfigurationBuilder()
            .set_function_mode("vis")
            .set_fsp_ids([1])
            .build(),
            VisFspConfigurationBuilder()
            .set_function_mode("vis")
            .set_fsp_ids([1])
            .build(),
            True,
        ),
        # Case where configurations are different due to missing fsp_ids in the second instance
        (
            VisFspConfigurationBuilder()
            .set_function_mode("vis")
            .set_fsp_ids([1])
            .build(),
            VisFspConfigurationBuilder()
            .set_function_mode("vis")
            .build(),  # Omitting set_fsp_ids to simulate difference
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
            VisConfigurationBuilder()
            .set_fsp(
                VisFspConfigurationBuilder()
                .set_function_mode("vis")
                .set_fsp_ids([1])
                .build()
            )
            .set_stn_beam(
                [
                    VisStnBeamConfigurationBuilder()
                    .set_stn_beam_id(1)
                    .set_host([(0, "192.168.1.00")])
                    .set_port([(0, 9000, 1)])
                    .set_mac([(0, "02-03-04-0a-0b-0c")])
                    .set_integration_ms(849)
                    .build()
                ]
            )
            .build(),
            VisConfigurationBuilder()
            .set_fsp(
                VisFspConfigurationBuilder()
                .set_function_mode("vis")
                .set_fsp_ids([1])
                .build()
            )
            .set_stn_beam(
                [
                    VisStnBeamConfigurationBuilder()
                    .set_stn_beam_id(1)
                    .set_host([(0, "192.168.1.00")])
                    .set_port([(0, 9000, 1)])
                    .set_mac([(0, "02-03-04-0a-0b-0c")])
                    .set_integration_ms(849)
                    .build()
                ]
            )
            .build(),
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
            LowCBFConfigurationBuilder()
            .set_stations(
                StationConfigurationBuilder()
                .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
                .set_stn_beams(
                    [
                        StnBeamConfigurationBuilder()
                        .set_stn_beam_id(1)
                        .set_beam_id(1)
                        .set_freq_ids([400])
                        .set_delay_poly("tango/device/instance/delay")
                        .build()
                    ]
                )
                .build()
            )
            .set_vis(
                VisConfigurationBuilder()
                .set_fsp(
                    VisFspConfigurationBuilder()
                    .set_function_mode("vis")
                    .set_fsp_ids([1])
                    .build()
                )
                .set_stn_beam(
                    [
                        VisStnBeamConfigurationBuilder()
                        .set_stn_beam_id(1)
                        .set_host([(0, "192.168.1.00")])
                        .set_port([(0, 9000, 1)])
                        .set_mac([(0, "02-03-04-0a-0b-0c")])
                        .set_integration_ms(849)
                        .build()
                    ]
                )
                .build()
            )
            .set_timing_beams(
                TimingBeamsConfigurationBuilder()
                .set_beams(
                    [
                        BeamsConfigurationBuilder()
                        .set_pst_beam_id(1)
                        .set_stn_beam_id(1)
                        .set_stn_weights([0.9, 1.0, 1.0, 1.0, 0.9, 1.0])
                        .build()
                    ]
                )
                .set_fsp(
                    VisFspConfigurationBuilder()
                    .set_fsp_ids([2])
                    .set_firmware("pst")
                    .build()
                )
                .build()
            )
            .build(),
            LowCBFConfigurationBuilder()
            .set_stations(
                StationConfigurationBuilder()
                .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
                .set_stn_beams(
                    [
                        StnBeamConfigurationBuilder()
                        .set_stn_beam_id(1)
                        .set_beam_id(1)
                        .set_freq_ids([400])
                        .set_delay_poly("tango/device/instance/delay")
                        .build()
                    ]
                )
                .build()
            )
            .set_vis(
                VisConfigurationBuilder()
                .set_fsp(
                    VisFspConfigurationBuilder()
                    .set_function_mode("vis")
                    .set_fsp_ids([1])
                    .build()
                )
                .set_stn_beam(
                    [
                        VisStnBeamConfigurationBuilder()
                        .set_stn_beam_id(1)
                        .set_host([(0, "192.168.1.00")])
                        .set_port([(0, 9000, 1)])
                        .set_mac([(0, "02-03-04-0a-0b-0c")])
                        .set_integration_ms(849)
                        .build()
                    ]
                )
                .build()
            )
            .set_timing_beams(
                TimingBeamsConfigurationBuilder()
                .set_beams(
                    [
                        BeamsConfigurationBuilder()
                        .set_pst_beam_id(1)
                        .set_stn_beam_id(1)
                        .set_stn_weights([0.9, 1.0, 1.0, 1.0, 0.9, 1.0])
                        .build()
                    ]
                )
                .set_fsp(
                    VisFspConfigurationBuilder()
                    .set_fsp_ids([2])
                    .set_firmware("pst")
                    .build()
                )
                .build()
            )
            .build(),
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


def test_csp_configuration_equality(csp_config, low_csp_config):
    """
    Verify that CSPConfiguration objects are equal when all they have the same values
    and not equal when any attribute differs.
    """

    csp_config_invalid = CSPConfigurationBuilder().set_interface("foo").build()
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
