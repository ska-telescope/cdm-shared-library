import pytest

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
    FieldConfigurationBuilder, ExecutionBlockConfigurationBuilder, SDPConfigurationBuilder
)


@pytest.fixture(scope="module")
def processing_block_parameters():
    """
    Provides Processing block parameters
    """
    return {
        "plasmaEnabled": True,
        "reception": {
            "layout": "http://127.0.0.1:80/model/default/ska1_low/layout",
            "num_channels": 13824,
            "channels_per_stream": 6912,
            "continuous_mode": True,
            "transport_protocol": "tcp",
        },
        "pvc": {"name": "receive-data"},
        "plasma_parameters": {
            "initContainers": [
                {
                    "name": "existing-output-remover",
                    "image": "artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                    "command": ["rm", "-rf", "/mnt/data/output*.ms"],
                    "volumeMounts": [
                        {"mountPath": "/mnt/data", "name": "receive-data"}
                    ],
                }
            ],
            "extraContainers": [
                {
                    "name": "plasma-processor",
                    "image": "artefact.skao.int/ska-sdp-realtime-receive-modules:3.3.0",
                    "command": [
                        "plasma-mswriter",
                        "-s",
                        "/plasma/socket",
                        "--max_payloads",
                        "12",
                        "--use_plasmastman",
                        "False",
                        "/mnt/data/output.ms",
                    ],
                    "volumeMounts": [
                        {"name": "plasma-storage-volume", "mountPath": "/plasma"},
                        {"mountPath": "/mnt/data", "name": "receive-data"},
                    ],
                },
                {
                    "name": "tmlite-server",
                    "image": "artefact.skao.int/ska-sdp-tmlite-server:0.3.0",
                },
            ],
        },
    }


@pytest.fixture(scope="module")
def channel():
    """
    Provides CDM Channel configuration instance through ChannelBuilder builder class
    """
    return (
        ChannelBuilder()
        .set_count(count=744)
        .set_start(start=0)
        .set_stride(stride=2)
        .set_freq_min(freq_min=0.35e9)
        .set_freq_max(freq_max=1.05e9)
        .set_link_map(link_map=[[0, 0], [200, 1], [744, 2], [944, 3]])
        .set_spectral_window_id(spectral_window_id="fsp_2_channels")
        .build()
    )


@pytest.fixture(scope="module")
def eb_scan_type():
    """
    Provides CDM EBScanType configuration instance through EBScanTypeBuilder builder class
    """
    return (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"field_id": "field_a"}})
        .set_derive_from(derive_from=".default")
        .build()
    )


@pytest.fixture(scope="module")
def scan_type(channel):
    """
    Provides CDM ScanType configuration instance through ScanTypeBuilder builder class
    """
    return (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science_A")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel])
        .build()
    )


@pytest.fixture(scope="module")
def workflow():
    """
    Provides CDM SDPWorkflow configuration instance through SDPWorkflowBuilder builder class
    """
    return (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.1")
        .build()
    )


@pytest.fixture(scope="module")
def processing_block(workflow, processing_block_parameters):
    """
    Provides CDM ProcessingBlock configuration instance through ProcessingBlockConfigurationBuilder builder class
    """
    return (
        ProcessingBlockConfigurationBuilder()
        .set_parameters(parameters=processing_block_parameters)
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_workflow(workflow=workflow)
        .build()
    )


@pytest.fixture(scope="module")
def beams():
    """
    Provides CDM Beam configuration instance through BeamConfigurationBuilder builder class
    """
    return (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="vis0")
        .set_function(function="visibilities")
        .build()
    )


@pytest.fixture(scope="module")
def channels(channel):
    """
    Provides CDM Channel configuration instance through ChannelConfigurationBuilder builder class
    """
    return (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel])
        .build()
    )


@pytest.fixture(scope="module")
def polarisation_config():
    """
    Provides CDM Polarisation configuration instance through PolarisationConfigurationBuilder builder class
    """
    return (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )


@pytest.fixture(scope="module")
def phase_dir():
    """
    Provides CDM PhaseDir configuration instance through PhaseDirBuilder builder class
    """
    return (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )


@pytest.fixture(scope="module")
def field_config(phase_dir):
    """
    Provides CDM Field configuration instance through FieldConfigurationBuilder builder class
    """
    return (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir)
        .build()
    )


@pytest.fixture(scope="module")
def execution_block(beams, channels, polarisation_config, field_config, eb_scan_type):
    """
    Provides CDM Execution Block configuration instance through ExecutionBlockConfigurationBuilder builder class
    """
    return (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=3600)
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisation_config])
        .set_fields(fields=[field_config])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )


@pytest.fixture(scope="module")
def sdp_allocate(processing_block, execution_block, scan_type):
    """
    Provides CDM SDP configuration instance through SDPConfigurationBuilder builder class
    """
    return (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=[scan_type])
        .set_processing_blocks(processing_blocks=[processing_block])
        .set_execution_block(execution_block=execution_block)
        .build()
    )
