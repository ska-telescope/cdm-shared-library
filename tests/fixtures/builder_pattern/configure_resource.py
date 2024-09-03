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
    return SubarrayBeamConfigurationBuilder()


@pytest.fixture(scope="module")
def mccs_config(station_beam_config) -> MCCSConfiguration:
    """
    Provides CDM MCCS Configuration instance through Builder class with predefined values
    """
    return MCCSConfigurationBuilder(
        subarray_beam_configs=[station_beam_config]
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
        pst_config=PSTConfigurationBuilder(),
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
