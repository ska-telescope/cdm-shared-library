import pytest

from ska_tmc_cdm.messages.central_node.sdp import Channel, EBScanType

from tests.unit.ska_tmc_cdm.builder.central_node.sdp import (
    ChannelBuilder,
    EBScanTypeBuilder,
    ScanTypeBuilder,
    SDPWorkflowBuilder,
    ProcessingBlockConfigurationBuilder,
    BeamConfigurationBuilder,
    ChannelConfigurationBuilder,
    PolarisationConfigurationBuilder,
    PhaseDirBuilder,
    FieldConfigurationBuilder,
    ExecutionBlockConfigurationBuilder,
    SDPConfigurationBuilder,
)


@pytest.fixture(scope="module")
def channel() -> Channel:
    return ChannelBuilder()


@pytest.fixture(scope="module")
def eb_scan_type() -> EBScanType:
    return EBScanTypeBuilder()


@pytest.fixture(scope="module")
def scan_type():
    return ScanTypeBuilder()


@pytest.fixture(scope="module")
def sdp_workflow():
    return SDPWorkflowBuilder()


@pytest.fixture(scope="module")
def processing_block():
    return ProcessingBlockConfigurationBuilder()


@pytest.fixture(scope="module")
def beams():
    return BeamConfigurationBuilder()


@pytest.fixture(scope="module")
def channels():
    return ChannelConfigurationBuilder()


@pytest.fixture(scope="module")
def polarisation_config():
    return PolarisationConfigurationBuilder()


@pytest.fixture(scope="module")
def phase_dir():
    return PhaseDirBuilder()


@pytest.fixture(scope="module")
def field_config():
    return FieldConfigurationBuilder()


@pytest.fixture(scope="module")
def execution_block():
    """
    Provides CDM Execution Block configuration instance through ExecutionBlockConfigurationBuilder builder class
    """
    return ExecutionBlockConfigurationBuilder()


@pytest.fixture(scope="module")
def sdp_allocate():
    """
    Provides CDM SDP configuration instance through SDPConfigurationBuilder builder class
    """
    return SDPConfigurationBuilder()
