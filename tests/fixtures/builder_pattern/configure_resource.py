import pytest

from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand, DishConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.csp import FSPFunctionMode, CSPConfiguration
from ska_tmc_cdm.messages.subarray_node.configure.mccs import StnConfiguration, SubarrayBeamTarget, SubarrayBeamConfiguration, MCCSConfiguration
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.core import DishConfigurationBuilder
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.csp import CSPConfigurationBuilder, SubarrayConfigurationBuilder, CommonConfigurationBuilder, CBFConfigurationBuilder, \
    FSPConfigurationBuilder, StnBeamConfigurationBuilder, VisFspConfigurationBuilder, VisConfigurationBuilder, StationConfigurationBuilder, LowCBFConfigurationBuilder
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.mccs import StnConfigurationBuilder, SubarrayBeamTargetBuilder, SubarrayBeamConfigurationBuilder, MCCSConfigurationBuilder
from tests.unit.ska_tmc_cdm.builder.subarray_node.configure.sdp import SDPConfigurationBuilder


@pytest.fixture(scope="module")
def station_config() -> StnConfiguration:
    """
    Provides CDM Station Configuration instance through Builder class with predefined values
    """
    return StnConfigurationBuilder().set_station_id(1).build()


@pytest.fixture(scope="module")
def target() -> SubarrayBeamTarget:
    """
    Provides CDM Target instance through Builder class with predefined values
    """
    return (
        SubarrayBeamTargetBuilder()
        .set_az(180.0)
        .set_el(45.0)
        .set_target_name("DriftScan")
        .set_reference_frame("HORIZON")
        .build()
    )


@pytest.fixture(scope="module")
def station_beam_config(target) -> SubarrayBeamConfiguration:
    """
    Provides CDM Station Beam Configuration instance through Builder class with predefined values
    """
    return (
        SubarrayBeamConfigurationBuilder()
        .set_subarray_beam_id(1)
        .set_station_ids([1, 2])
        .set_channels([[1, 2, 3, 4, 5, 6]])
        .set_update_rate(1.0)
        .set_target(target)
        .set_antenna_weights([1.0, 1.0, 1.0])
        .set_phase_centre([0.0, 0.0])
        .build()
    )


@pytest.fixture(scope="module")
def mccs_config(station_config, station_beam_config) -> MCCSConfiguration:
    """
    Provides CDM MCCS Configuration instance through Builder class with predefined values
    """
    return (
        MCCSConfigurationBuilder()
        .set_station_configs(station_configs=[station_config])
        .set_subarray_beam_config(subarray_beam_configs=[station_beam_config])
        .build()
    )


@pytest.fixture(scope="module")
def dish_config() -> DishConfiguration:
    """
    Provides CDM Dish Configuration instance through Builder class with predefined values
    """
    return (
        DishConfigurationBuilder().set_receiver_band(ReceiverBand.BAND_1).build()
    )


@pytest.fixture(scope="module")
def sdp_config() -> SDPConfiguration:
    """
    Provides CDM SDP Configuration instance through Builder class with predefined values
    """
    return (
        SDPConfigurationBuilder().set_scan_type("science_A").build()
    )


@pytest.fixture(scope="module")
def csp_config() -> CSPConfiguration:
    """
    Provides Mid CDM CSP Configuration instance through Builder class with predefined values
    """
    return (
        CSPConfigurationBuilder()
        .set_interface("interface")
        .set_subarray(
            SubarrayConfigurationBuilder()
            .set_subarray_name(subarray_name="subarray name")
            .build()
        )
        .set_common(
            CommonConfigurationBuilder()
            .set_config_id(config_id="config_id")
            .set_frequency_band(frequency_band=ReceiverBand.BAND_1)
            .set_subarray_id(1)
            .build()
        )
        .set_cbf_config(
            CBFConfigurationBuilder()
            .set_fsp_config(
                [
                    FSPConfigurationBuilder()
                    .set_fsp_id(fsp_id=1)
                    .set_function_mode(function_mode=FSPFunctionMode.CORR)
                    .set_frequency_slice_id(frequency_slice_id=1)
                    .set_integration_factor(integration_factor=10)
                    .set_zoom_factor(0)
                    .build()
                ]
            )
            .build()
        )
        .build()
    )


@pytest.fixture(scope="module")
def low_csp_config() ->CSPConfiguration:
    """
    Provides Low CDM CSP Configuration instance through Builder class with predefined values
    """
    return (CSPConfigurationBuilder()
            .set_interface("https://schema.skao.int/ska-low-csp-configure/0.0")
            .set_common(common=CommonConfigurationBuilder()
                .set_config_id("sbi-mvp01-20200325-00001-science_A")
                .set_frequency_band(ReceiverBand.BAND_1)
                .set_subarray_id(1)
                .set_band_5_tuning([5.85, 7.25])
                .build())
            .set_lowcbf(lowcbf=LowCBFConfigurationBuilder()
                .set_stations(
                    StationConfigurationBuilder()
                        .set_stns([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]])
                        .set_stn_beams(
                           [ StnBeamConfigurationBuilder()
                                .set_stn_beam_id(1)
                                .set_freq_ids([400])
                            .set_host([(0, "192.168.1.00")])
                            .set_port([(0, 9000, 1)])
                            .set_mac([(0, "02-03-04-0a-0b-0c")])
                                .set_integration_ms(849)
                                .build()]
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
                            [StnBeamConfigurationBuilder()
                                .set_stn_beam_id(1)
                                .set_freq_ids([400])
                            .set_host([(0, "192.168.1.00")])
                            .set_port([(0, 9000, 1)])
                            .set_mac([(0, "02-03-04-0a-0b-0c")])
                                .set_integration_ms(849)
                                .build()]
                        )
                        .build())
                    .build())

            .build())