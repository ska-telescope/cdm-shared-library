import pytest

from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.core import (
    ReceiverBand,
    DishConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    FSPFunctionMode,
    CSPConfiguration,
)
from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    SubarrayBeamConfiguration,
    MCCSConfiguration,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import (
    DishConfigurationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import (
    CSPConfigurationBuilder,
    SubarrayConfigurationBuilder,
    CommonConfigurationBuilder,
    CBFConfigurationBuilder,
    FSPConfigurationBuilder,
    StnBeamConfigurationBuilder,
    VisFspConfigurationBuilder,
    VisConfigurationBuilder,
    StationConfigurationBuilder,
    LowCBFConfigurationBuilder,
    VisStnBeamConfigurationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import (
    SubarrayBeamConfigurationBuilder,
    MCCSConfigurationBuilder,
    SubarrayBeamSkyCoordinatesBuilder,
    SubarrayBeamLogicalbandsBuilder,
    SubarrayBeamApertureBuilder,
)
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.sdp import (
    SDPConfigurationBuilder,
)

from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.pst import (
    PSTBeamConfigurationBuilder,
    PSTChannelizationStageConfigurationBuilder,
    PSTConfigurationBuilder,
    PSTScanConfigurationBuilder,
    PSTScanCoordinatesBuilder,
)


@pytest.fixture(scope="module")
def station_beam_config() -> SubarrayBeamConfiguration:
    """
    Provides CDM Station Beam Configuration instance through Builder class with predefined values
    """
    return (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_update_rate(1.0)
        .set_logical_bands(
            SubarrayBeamLogicalbandsBuilder()
            .set_start_channel(80)
            .set_number_of_channels(16)
        )
        .set_apertures(
            SubarrayBeamApertureBuilder()
            .set_aperture_id("AP001.01")
            .set_weighting_key_ref("aperture2")
        )
        .set_sky_coordinates(
            SubarrayBeamSkyCoordinatesBuilder()
            .set_reference_frame("HORIZON")
            .set_c1(180.0)
            .set_c2(90.0)
        )
        .build()
    )


@pytest.fixture(scope="module")
def mccs_config(station_beam_config) -> MCCSConfiguration:
    """
    Provides CDM MCCS Configuration instance through Builder class with predefined values
    """
    return (
        MCCSConfigurationBuilder()
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )


@pytest.fixture(scope="module")
def dish_config() -> DishConfiguration:
    """
    Provides CDM Dish Configuration instance through Builder class with predefined values
    """
    return (
        DishConfigurationBuilder()
        .set_receiver_band(ReceiverBand.BAND_1)
        .build()
    )


@pytest.fixture(scope="module")
def sdp_config() -> SDPConfiguration:
    return SDPConfigurationBuilder()


@pytest.fixture(scope="module")
def csp_config() -> CSPConfiguration:
    """
    Provides Mid CDM CSP Configuration instance through Builder class with predefined values
    """
    return CSPConfigurationBuilder()


@pytest.fixture(scope="module")
def low_csp_config() -> CSPConfiguration:
    """
    Provides Low CDM CSP Configuration instance through Builder class with predefined values
    """
    return (
        CSPConfigurationBuilder(interface="https://schema.skao.int/ska-low-csp-configure/0.0",
        common=CommonConfigurationBuilder(
            config_id="sbi-mvp01-20200325-00001-science_A",
            frequency_band=ReceiverBand.BAND_1,
            subarray_id=1,
            band_5_tuning=[5.85, 7.25],
        )
        .set_pst_config(
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
            .build()
        )
        .set_lowcbf(
            lowcbf=LowCBFConfigurationBuilder()
            .set_stations(
                StationConfigurationBuilder()
                .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
                .set_stn_beams(
                    [
                        StnBeamConfigurationBuilder()
                        .set_stn_beam_id(1)
                        .set_freq_ids([400])
                        .set_beam_id(1)
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
            .build()
        )
        .build()
    )
