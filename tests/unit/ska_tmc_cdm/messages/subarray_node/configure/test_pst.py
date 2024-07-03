"""
Unit tests for the ska_tmc_cdm.messages.subarray_node.configure.pst module.
"""
import pytest

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.pst import (
    PSTBeamConfigurationBuilder,
    PSTChannelizationStageConfigurationBuilder,
    PSTConfigurationBuilder,
    PSTScanConfigurationBuilder,
    PSTScanCoordinatesBuilder,
)


@pytest.mark.parametrize(
    "pst_configuration_1, pst_configuration_2, is_equal",
    [
        (
            PSTConfigurationBuilder()
            .set_beams(
                [
                    PSTBeamConfigurationBuilder()
                    .set_beam_id(1)
                    .set_scan(
                        PSTScanConfigurationBuilder()
                        .set_activation_time("2022-01-19T23:07:45Z")
                        .set_bits_per_sample(32)
                        .set_num_of_polarizations(2)
                        .set_udp_nsamp(32)
                        .set_wt_nsamp(32)
                        .set_udp_nchan(24)
                        .set_num_frequency_channels(432)
                        .set_centre_frequency(200000000.0)
                        .set_total_bandwidth(1562500.0)
                        .set_observation_mode("VOLTAGE_RECORDER")
                        .set_observer_id("jdoe")
                        .set_project_id("project1")
                        .set_pointing_id("pointing1")
                        .set_source("J1921+2153")
                        .set_itrf([5109360.133, 2006852.586, -3238948.127])
                        .set_receiver_id("receiver3")
                        .set_feed_polarization("LIN")
                        .set_feed_handedness(1)
                        .set_feed_angle(1.234)
                        .set_feed_tracking_mode("FA")
                        .set_feed_position_angle(10.0)
                        .set_oversampling_ratio([8, 7])
                        .set_coordinates(
                            PSTScanCoordinatesBuilder()
                            .set_equinox(2000.0)
                            .set_ra("19:21:44.815")
                            .set_dec("21:53:02.400")
                            .build()
                        )
                        .set_max_scan_length(20000.0)
                        .set_subint_duration(30.0)
                        .set_receptors(["receptor1", "receptor2"])
                        .set_receptor_weights([0.4, 0.6])
                        .set_num_channelization_stages(2)
                        .set_channelization_stages(
                            [
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(1024)
                                .set_oversampling_ratio([32, 27])
                                .build(),
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(256)
                                .set_oversampling_ratio([4, 3])
                                .build(),
                            ]
                        )
                        .build()
                    )
                    .build()
                ]
            )
            .build(),
            PSTConfigurationBuilder()
            .set_beams(
                [
                    PSTBeamConfigurationBuilder()
                    .set_beam_id(1)
                    .set_scan(
                        PSTScanConfigurationBuilder()
                        .set_activation_time("2022-01-19T23:07:45Z")
                        .set_bits_per_sample(32)
                        .set_num_of_polarizations(2)
                        .set_udp_nsamp(32)
                        .set_wt_nsamp(32)
                        .set_udp_nchan(24)
                        .set_num_frequency_channels(432)
                        .set_centre_frequency(200000000.0)
                        .set_total_bandwidth(1562500.0)
                        .set_observation_mode("VOLTAGE_RECORDER")
                        .set_observer_id("jdoe")
                        .set_project_id("project1")
                        .set_pointing_id("pointing1")
                        .set_source("J1921+2153")
                        .set_itrf([5109360.133, 2006852.586, -3238948.127])
                        .set_receiver_id("receiver3")
                        .set_feed_polarization("LIN")
                        .set_feed_handedness(1)
                        .set_feed_angle(1.234)
                        .set_feed_tracking_mode("FA")
                        .set_feed_position_angle(10.0)
                        .set_oversampling_ratio([8, 7])
                        .set_coordinates(
                            PSTScanCoordinatesBuilder()
                            .set_equinox(2000.0)
                            .set_ra("19:21:44.815")
                            .set_dec("21:53:02.400")
                            .build()
                        )
                        .set_max_scan_length(20000.0)
                        .set_subint_duration(30.0)
                        .set_receptors(["receptor1", "receptor2"])
                        .set_receptor_weights([0.4, 0.6])
                        .set_num_channelization_stages(2)
                        .set_channelization_stages(
                            [
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(1024)
                                .set_oversampling_ratio([32, 27])
                                .build(),
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(256)
                                .set_oversampling_ratio([4, 3])
                                .build(),
                            ]
                        )
                        .build()
                    )
                    .build()
                ]
            )
            .build(),
            True,
        ),
        (
            PSTConfigurationBuilder()
            .set_beams(
                [
                    PSTBeamConfigurationBuilder()
                    .set_beam_id(1)
                    .set_scan(
                        PSTScanConfigurationBuilder()
                        .set_activation_time("2022-01-19T23:07:45Z")
                        .set_bits_per_sample(32)
                        .set_num_of_polarizations(2)
                        .set_udp_nsamp(32)
                        .set_wt_nsamp(32)
                        .set_udp_nchan(24)
                        .set_num_frequency_channels(432)
                        .set_centre_frequency(200000000.0)
                        .set_total_bandwidth(1562500.0)
                        .set_observation_mode("VOLTAGE_RECORDER")
                        .set_observer_id("jdoe")
                        .set_project_id("project1")
                        .set_pointing_id("pointing1")
                        .set_source("J1921+2153")
                        .set_itrf([5109360.133, 2006852.586, -3238948.127])
                        .set_receiver_id("receiver3")
                        .set_feed_polarization("LIN")
                        .set_feed_handedness(1)
                        .set_feed_angle(1.234)
                        .set_feed_tracking_mode("FA")
                        .set_feed_position_angle(10.0)
                        .set_oversampling_ratio([8, 7])
                        .set_coordinates(
                            PSTScanCoordinatesBuilder()
                            .set_equinox(2000.0)
                            .set_ra("19:21:44.815")
                            .set_dec("21:53:02.400")
                            .build()
                        )
                        .set_max_scan_length(20000.0)
                        .set_subint_duration(30.0)
                        .set_receptors(["receptor1", "receptor2"])
                        .set_receptor_weights([0.4, 0.6])
                        .set_num_channelization_stages(2)
                        .set_channelization_stages(
                            [
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(1024)
                                .set_oversampling_ratio([32, 27])
                                .build(),
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(256)
                                .set_oversampling_ratio([4, 3])
                                .build(),
                            ]
                        )
                        .build()
                    )
                    .build()
                ]
            )
            .build(),
            PSTConfigurationBuilder()
            .set_beams(
                [
                    PSTBeamConfigurationBuilder()
                    .set_beam_id(1)
                    .set_scan(
                        PSTScanConfigurationBuilder()
                        .set_activation_time("2022-01-19T23:07:45Z")
                        .set_bits_per_sample(32)
                        .set_num_of_polarizations(2)
                        .set_udp_nsamp(32)
                        .set_wt_nsamp(32)
                        .set_udp_nchan(24)
                        .set_num_frequency_channels(432)
                        .set_centre_frequency(200000000.0)
                        .set_total_bandwidth(1562500.0)
                        .set_observation_mode("VOLTAGE_RECORDER")
                        .set_observer_id("jdoe")
                        .set_project_id("project1")
                        .set_pointing_id("pointing1")
                        .set_source("J1921+2153")
                        .set_itrf([5109360.133, 2006852.586, -3238948.127])
                        .set_receiver_id("receiver3")
                        .set_feed_polarization("LIN")
                        .set_feed_handedness(1)
                        .set_feed_angle(1.234)
                        .set_feed_tracking_mode("FA")
                        .set_feed_position_angle(10.0)
                        .set_oversampling_ratio([8, 7])
                        .set_coordinates(
                            PSTScanCoordinatesBuilder()
                            .set_equinox(2000.0)
                            .set_ra("19:21:44.815")
                            .set_dec("21:53:02.400")
                            .build()
                        )
                        .set_max_scan_length(20000.0)
                        .set_subint_duration(30.0)
                        .set_receptors(["receptor2", "receptor3"])
                        .set_receptor_weights([0.4, 0.6])
                        .set_num_channelization_stages(2)
                        .set_channelization_stages(
                            [
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(1024)
                                .set_oversampling_ratio([32, 27])
                                .build(),
                                PSTChannelizationStageConfigurationBuilder()
                                .set_num_filter_taps(1)
                                .set_filter_coefficients([1.0])
                                .set_num_frequency_channels(256)
                                .set_oversampling_ratio([4, 3])
                                .build(),
                            ]
                        )
                        .build()
                    )
                    .build()
                ]
            )
            .build(),
            False,
        ),
    ],
)
def test_pst_configuration_builder(
    pst_configuration_1, pst_configuration_2, is_equal
):
    """
    Test the PSTConfigurationBuilder class.

    :param pst_configuration_1: The first PSTConfiguration object to compare.
    :type pst_configuration_1: PSTConfiguration
    :param pst_configuration_2: The second PSTConfiguration object to compare.
    :type pst_configuration_2: PSTConfiguration
    :param is_equal: Whether the two objects are equal or not.
    :type is_equal: bool
    """
    assert (pst_configuration_1 == pst_configuration_2) == is_equal
    assert pst_configuration_1 != 1
    assert pst_configuration_1 != object
