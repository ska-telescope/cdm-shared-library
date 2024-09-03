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
    return SubarrayBeamConfigurationBuilder(
        subarray_beam_id=1,
        update_rate=1.0,
        logical_bands=SubarrayBeamLogicalbandsBuilder(
            start_channel=80,
            number_of_channels=16,
        ),
        apertures=SubarrayBeamApertureBuilder(
            aperture_id="AP001.01",
            weighting_key_ref="aperture2",
        ),
        sky_coordinates=SubarrayBeamSkyCoordinatesBuilder(
            reference_frame="HORIZON",
            c1=180.0,
            c2=90.0,
        ),
    )


@pytest.fixture(scope="module")
def mccs_config(station_beam_config) -> MCCSConfiguration:
    """
    Provides CDM MCCS Configuration instance through Builder class with predefined values
    """
    return MCCSConfigurationBuilder(
        subarray_beam_configs=[station_beam_config],
    )


@pytest.fixture(scope="module")
def dish_config() -> DishConfiguration:
    """
    Provides CDM Dish Configuration instance through Builder class with predefined values
    """
    return DishConfigurationBuilder()


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
    return CSPConfigurationBuilder(
        interface="https://schema.skao.int/ska-low-csp-configure/0.0",
        common=CommonConfigurationBuilder(),
        pst_config=PSTConfigurationBuilder(
            beams=[
                PSTBeamConfigurationBuilder(
                    beam_id=1,
                    scan=PSTScanConfigurationBuilder(
                        activation_time="2022-01-19T23:07:45Z",
                        bits_per_sample=32,
                        num_of_polarizations=2,
                        udp_nsamp=32,
                        wt_nsamp=32,
                        udp_nchan=24,
                        num_frequency_channels=432,
                        centre_frequency=200000000.0,
                        total_bandwidth=1562500.0,
                        observation_mode="VOLTAGE_RECORDER",
                        observer_id="jdoe",
                        project_id="project1",
                        pointing_id="pointing1",
                        source="J1921+2153",
                        itrf=[5109360.133, 2006852.586, -3238948.127],
                        receiver_id="receiver3",
                        feed_polarization="LIN",
                        feed_handedness=1,
                        feed_angle=1.234,
                        feed_tracking_mode="FA",
                        feed_position_angle=10.0,
                        oversampling_ratio=[8, 7],
                        coordinates=PSTScanCoordinatesBuilder(
                            equinox=2000.0,
                            ra="19:21:44.815",
                            dec="21:53:02.400",
                        ),
                        max_scan_length=20000.0,
                        subint_duration=30.0,
                        receptors=["receptor1", "receptor2"],
                        receptor_weights=[0.4, 0.6],
                        num_channelization_stages=2,
                        channelization_stages=[
                            PSTChannelizationStageConfigurationBuilder(
                                num_filter_taps=1,
                                filter_coefficients=[1.0],
                                num_frequency_channels=1024,
                                oversampling_ratio=[32, 27],
                            ),
                            PSTChannelizationStageConfigurationBuilder(
                                num_filter_taps=1,
                                filter_coefficients=[1.0],
                                num_frequency_channels=256,
                                oversampling_ratio=[4, 3],
                            ),
                        ],
                    ),
                )
            ]
        ),
        lowcbf=LowCBFConfigurationBuilder(
            stations=StationConfigurationBuilder(
                stns=[[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
                stn_beams=[
                    StnBeamConfigurationBuilder(
                        stn_beam_id=1, freq_ids=[400], beam_id=1
                    )
                ],
            )
        ),
        vis=VisConfigurationBuilder(),
    )
