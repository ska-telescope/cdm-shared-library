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
    """
    Provides CDM SDP Configuration instance through Builder class with predefined values
    """
    return SDPConfigurationBuilder().set_scan_type("science_A").build()


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
                    .set_integration_factor(integration_factor=10)
                    .build()
                ]
            )
            .build()
        )
        .build()
    )


@pytest.fixture(scope="module")
def low_csp_config() -> CSPConfiguration:
    """
    Provides Low CDM CSP Configuration instance through Builder class with predefined values
    """
    return (
        CSPConfigurationBuilder()
        .set_interface("https://schema.skao.int/ska-low-csp-configure/0.0")
        .set_common(
            common=CommonConfigurationBuilder()
            .set_config_id("sbi-mvp01-20200325-00001-science_A")
            .set_frequency_band(ReceiverBand.BAND_1)
            .set_subarray_id(1)
            .set_band_5_tuning([5.85, 7.25])
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
