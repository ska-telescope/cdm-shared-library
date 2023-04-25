"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    EBScanType,
    EBScanTypeBeam,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PbDependency,
    PhaseDir,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
)
from tests.unit.ska_tmc_cdm.builder_pattern.central_node.sdp import (
    BeamConfigurationBuilder,
    ChannelBuilder,
    ChannelConfigurationBuilder,
    EBScanTypeBeamBuilder,
    EBScanTypeBuilder,
    ExecutionBlockConfigurationBuilder,
    FieldConfigurationBuilder,
    PbDependencyBuilder,
    PhaseDirBuilder,
    PolarisationConfigurationBuilder,
    ProcessingBlockConfigurationBuilder,
    ScanTypeBuilder,
    ScriptConfigurationBuilder,
    SDPConfigurationBuilder,
    SDPWorkflowBuilder,
)


def test_channel_equals():
    """
    Verify that Channel objects are considered equal when they have the same:
     - count
     - start
     - stride
     - freq_min
     - freq_max
     - link_map
    """
    channel1 = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    channel2 = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    assert channel1 == channel2

    assert channel1 != Channel(
        "fsp_2_channels",
        744,
        2000,
        2,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    assert channel1 != Channel(
        "fsp_2_channels",
        744,
        0,
        1,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    assert channel1 != Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.36e9,
        1.04e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    assert channel1 != Channel(
        "fsp_2_channels", 744, 0, 2, 0.35e9, 1.05e9, [[2000, 4], [2200, 5]]
    )

    # using Builder Pattern
    channel3 = (
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
    assert channel3 == Channel(
        744,
        0,
        2,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
        "fsp_2_channels",
    )

    assert channel3 != Channel(
        74,
        0,
        23,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [45, 3]],
        "fsp_2_channels",
    )


def test_channel_not_equal_to_other_objects():
    """
    Verify that Channel objects are not considered equal to objects of
    other types.
    """
    channel = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        1.05e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    assert channel != 1

    # using Builder Pattern
    channel2 = (
        ChannelBuilder()
        .set_count(count=744)
        .set_start(start=0)
        .set_stride(stride=2)
        .set_freq_min(freq_min=0.35e9)
        .set_freq_max(freq_max=1.05e9)
        .set_link_map(link_map=[[0, 0], [200, 1], [744, 2], [944, 3]])
        .set_spectral_window_id(spectral_window_id=None)
        .build()
    )
    assert channel2 != 1


def test_scan_type_equals():
    """
    Verify that ScanType objects are considered equal for the same passed parameter list
    """
    channel_1 = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        0.368e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    channel_2 = Channel(
        "fsp_2_channels", 744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]]
    )
    scan_type1 = ScanType(
        "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel_1, channel_2]
    )
    scan_type2 = ScanType(
        "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel_1, channel_2]
    )

    assert scan_type1 == scan_type2

    assert scan_type1 != ScanType(
        "calibration_B", "ICRS", "02:42:40.771", "-00:00:47.84", [channel_1, channel_2]
    )
    assert scan_type1 != ScanType(
        "science_A", "ICRS", "12:29:06.699", "-00:00:47.84", [channel_1, channel_2]
    )
    assert scan_type1 != ScanType(
        "science_A", "ICRS", "02:42:40.771", "02:03:08.598", [channel_1, channel_2]
    )
    assert scan_type1 != ScanType(
        "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel_1]
    )

    # Using Builder Pattern
    channel3 = (
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
    channel4 = (
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
    scan_type3 = (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science_A")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel3, channel4])
        .build()
    )

    assert scan_type3 == (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science_A")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel3, channel4])
        .build()
    )


def test_scan_type_not_equal_to_other_objects():
    """
    Verify that ScanType objects are not considered equal to objects of
    other types.
    """
    channel = Channel(
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        0.368e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel])
    assert scan_type != 1

    # Using Builder Pattern
    channel1 = (
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
    scan_type1 = (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science_A")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel1])
        .build()
    )
    assert scan_type1 != 1


def test_workflow_equals():
    """
    Verify that SDPWorkflow objects are considered equal when they have:
     - the same name
     - the same kind
     - the same version
    """
    workflow1 = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    workflow2 = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    assert workflow1 == workflow2

    assert workflow1 != SDPWorkflow(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    assert workflow2 != SDPWorkflow(
        name="vis_receive", kind="realtime", version="0.1.1"
    )

    # Using Builder Pattern
    workflow3 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.1")
        .build()
    )
    assert workflow3 == SDPWorkflow(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    assert workflow3 != SDPWorkflow(
        name="vis_receive", kind="realtime", version="0.0.1"
    )


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDPWorkflow objects are not considered equal to objects of
    other types.
    """
    workflow = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    assert workflow != 1

    workflow1 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.0")
        .build()
    )
    assert workflow1 != 1


def test_dependency_equals():
    """
    Verify that PBDependency objects are considered equal when they have:
     - the same PB ID
     - the same type
    """
    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    assert dep1 == dep2

    assert dep1 != PbDependency("pb-mvp01-20200325-00001", ["calibration"])
    assert dep1 != PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    # Using Builder Pattern
    dep3 = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_kind(kind=["visibilities"])
        .build()
    )

    assert dep3 == dep1

    assert dep3 != PbDependency("pb-mvp01-20200325-00001", ["calibration"])


def test_dependency_not_equal_to_other_objects():
    """
    Verify that PBDependency objects are not considered equal to objects of
    other types.
    """
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    assert dep != 1

    # Using Builder Pattern
    dep1 = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_kind(kind=["visibilities"])
        .build()
    )
    assert dep1 != 1


def test_processing_block_equals():
    """
    Verify that ProcessingBlock objects are considered equal
    """
    w_flow = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    pb1 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {}, [dep])
    pb2 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {}, [dep])

    assert pb1 == pb2

    assert pb1 != ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", w_flow, {}, [dep]
    )
    assert pb1 != ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", None, {}, [dep]
    )
    assert pb1 != ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00003", w_flow, None, [dep]
    )
    assert pb1 != ProcessingBlockConfiguration("pb-mvp01-20200325-00003", w_flow, {})

    # Using Builder Pattern
    workflow1 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.0")
        .build()
    )
    dep1 = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_kind(kind=["visibilities"])
        .build()
    )
    pb3 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_workflow(workflow=workflow1)
        .set_parameters(parameters={})
        .set_dependencies(dependencies=[dep1])
        .build()
    )
    assert pb3 == pb1

    assert pb3 != ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00003", w_flow, None, [dep]
    )


def test_processing_block_not_equal_to_other_objects():
    """
    Verify that ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    p_block = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", None, None, None)
    assert p_block != 1

    # Using Builder Pattern
    workflow = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.0")
        .build()
    )
    dep = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_kind(kind=["visibilities"])
        .build()
    )
    pb = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_workflow(workflow=workflow)
        .set_parameters(parameters={})
        .set_dependencies(dependencies=[dep])
        .build()
    )
    assert pb != 1


def test_sdp_configuration_block_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """
    channel = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    scan_type1 = ScanType(
        "science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel]
    )
    scan_type2 = ScanType(
        "calibration_B", "ICRS", "02:42:40.771", "-00:00:47.84", [channel]
    )

    scan_types = [scan_type1, scan_type2]

    wf1 = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    wf2 = SDPWorkflow("test_realtime", "realtime", "0.1.0")
    wf3 = SDPWorkflow("ical", "batch", "0.1.0")
    wf4 = SDPWorkflow("dpreb", "batch", "0.1.0")

    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    pb1 = ProcessingBlockConfiguration("pb-mvp01-20200325-00001", wf1, {})
    pb2 = ProcessingBlockConfiguration("pb-mvp01-20200325-00002", wf2, {})
    pb3 = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", wf3, {}, [dep1])
    pb4 = ProcessingBlockConfiguration("pb-mvp01-20200325-00004", wf4, {}, [dep2])

    processing_blocks = [pb1, pb2, pb3, pb4]

    sdp1 = SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks
    )
    sdp2 = SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, scan_types, processing_blocks
    )

    assert sdp1 == sdp2

    assert sdp1 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 0.0, scan_types, processing_blocks
    )
    assert sdp1 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, None, processing_blocks
    )
    assert sdp1 != SDPConfiguration("sbi-mvp01-20200325-00002", 100.0, scan_types, None)
    assert sdp1 != SDPConfiguration(None, None, None, None)

    # Using Builder Pattern
    channel1 = (
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
    scan_type3 = (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science_A")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel1])
        .build()
    )
    scan_type4 = (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id="calibration_B")
        .set_reference_frame(reference_frame="ICRS")
        .set_ra(ra="02:42:40.771")
        .set_dec(dec="-00:00:47.84")
        .set_channels(channels=[channel1])
        .build()
    )
    scan_types2 = [scan_type3, scan_type4]

    wf5 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.0")
        .build()
    )

    wf6 = (
        SDPWorkflowBuilder()
        .set_name(name="test_realtime")
        .set_kind(kind="realtime")
        .set_version(version="0.1.0")
        .build()
    )
    wf7 = (
        SDPWorkflowBuilder()
        .set_name(name="ical")
        .set_kind(kind="batch")
        .set_version(version="0.1.0")
        .build()
    )
    wf8 = (
        SDPWorkflowBuilder()
        .set_name(name="dpreb")
        .set_kind(kind="batch")
        .set_version(version="0.1.0")
        .build()
    )
    dep3 = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_kind(kind=["visibilities"])
        .build()
    )
    dep4 = (
        PbDependencyBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_kind(kind=["calibration"])
        .build()
    )
    pb5 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_workflow(workflow=wf5)
        .set_parameters(parameters={})
        .build()
    )
    pb6 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00002")
        .set_workflow(workflow=wf6)
        .set_parameters(parameters={})
        .build()
    )
    pb7 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_workflow(workflow=wf7)
        .set_parameters(parameters={})
        .set_dependencies([dep3])
        .build()
    )
    pb8 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00004")
        .set_workflow(workflow=wf8)
        .set_parameters(parameters={})
        .set_dependencies([dep4])
        .build()
    )
    processing_blocks1 = [pb5, pb6, pb7, pb8]

    sdp3 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=scan_types2)
        .set_processing_blocks(processing_blocks=processing_blocks1)
        .build()
    )
    sdp4 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=scan_types2)
        .set_processing_blocks(processing_blocks=processing_blocks1)
        .build()
    )

    assert sdp3 == sdp4

    assert sdp3 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 0.0, scan_types, processing_blocks
    )
    assert sdp3 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, None, processing_blocks
    )
    assert sdp3 != SDPConfiguration("sbi-mvp01-20200325-00002", 100.0, scan_types, None)
    assert sdp3 != SDPConfiguration(None, None, None, None)


def test_sdp_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    sdp = SDPConfiguration(None, None, None, None)
    assert sdp != 1

    # Using Builder Pattern

    sdp1 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=None)
        .set_processing_blocks(processing_blocks=None)
        .build()
    )
    assert sdp1 != 1


def test_sdp_modified_configuration_block_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """
    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    pb_config = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00003",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )
    beams = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00001",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )
    resource = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }

    sdp1 = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )
    sdp2 = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )

    assert sdp1 == sdp2

    assert sdp1 != SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    assert sdp2 != SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )

    # Using Builder Pattern
    channel1 = (
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
    scan_type1 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    script1 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(
            parameters={
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
                                {
                                    "name": "plasma-storage-volume",
                                    "mountPath": "/plasma",
                                },
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
        )
        .set_sbi_ids(sbi_ids=[sbi_ids_1])
        .set_script(script=script1)
        .build()
    )
    beams1 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    channels1 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    polarisation1 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir1 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    fields1 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir1)
        .build()
    )
    execution_block1 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=beams1)
        .set_channels(channels=channels1)
        .set_polarisations(polarisations=polarisation1)
        .set_fields(fields=fields1)
        .set_scan_types(scan_types=scan_type1)
        .build()
    )
    resource1 = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp3 = SDPConfiguration(
        resources=resource1,
        processing_blocks=[pb1],
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )
    sdp4 = SDPConfiguration(
        resources=resource1,
        processing_blocks=[pb1],
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )

    assert sdp3 == sdp4

    assert sdp3 != SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    assert sdp4 != SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )


def test_sdp_modified_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    pb_config = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00003",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )
    beams = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00001",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )
    resource = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    assert sdp != 1

    # Using Builder Pattern
    channel1 = (
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
    scan_type1 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    script1 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(
            parameters={
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
                                {
                                    "name": "plasma-storage-volume",
                                    "mountPath": "/plasma",
                                },
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
        )
        .set_sbi_ids(sbi_ids=[sbi_ids_1])
        .set_script(script=script1)
        .build()
    )
    beams1 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    channels1 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    polarisation1 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir1 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    fields1 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir1)
        .build()
    )
    execution_block1 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=beams1)
        .set_channels(channels=channels1)
        .set_polarisations(polarisations=polarisation1)
        .set_fields(fields=fields1)
        .set_scan_types(scan_types=scan_type1)
        .build()
    )
    resource1 = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp1 = SDPConfiguration(
        resources=resource1,
        processing_blocks=[pb1],
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )

    assert sdp1 != 1


def test_beam_equals():
    """
    Verify that Beam objects are considered equal when they have:
     - the same Beam ID
     - the same Function
     - the same Search Beam ID
    """
    beam1 = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    beam2 = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )

    assert beam1 == beam2

    assert beam1 != BeamConfiguration(
        beam_id="pss1", search_beam_id=2, function="pulsar search"
    )
    assert beam2 != BeamConfiguration(
        beam_id="pss1", search_beam_id=2, function="pulsar search"
    )

    # Using Builder Pattern
    beam3 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    beam4 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )

    assert beam3 == beam4


def test_beam_equals_not_equal_to_other_objects():
    """
    Verify that Beam objects are not considered equal to objects of
    other types.
    """
    beam = BeamConfiguration(beam_id="pss1", search_beam_id=1, function="pulsar search")
    assert beam != 1

    # Using Builder Pattern
    beam1 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    assert beam1 != 1


def test_chanel_configuration_equals():
    """
    Verify that Channels Configuration objects are considered equal when they have:
     - the same Channels ID
     - the same Spectral Windows
    """
    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    channels1 = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    channels2 = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )

    assert channels1 == channels2

    assert channels1 != ChannelConfiguration(
        channels_id="pulsar_channels",
        spectral_windows=[channel],
    )
    assert channels2 != ChannelConfiguration(
        channels_id="pulsar_channels",
        spectral_windows=[channel],
    )

    # Using Builder Pattern
    channel1 = (
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
    channels3 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    channels4 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )

    assert channels3 == channels4

    assert channels3 != ChannelConfiguration(
        channels_id="pulsar_channels",
        spectral_windows=[channel1],
    )
    assert channels4 != ChannelConfiguration(
        channels_id="pulsar_channels",
        spectral_windows=[channel1],
    )


def test_chanel_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Channels Configuration objects are not considered equal to objects of
    other types.
    """
    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    channels = ChannelConfiguration(
        channels_id="pulsar_channels",
        spectral_windows=[channel],
    )
    assert channels != 1

    # Using Builder Pattern
    channels1 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=None)
        .build()
    )
    assert channels1 != 1


def test_polarisation_configuration_equals():
    """
    Verify that Polarisation Configuration objects are considered equal when they have:
     - the same polarisation_id
     - the same corr_type
    """
    polar1 = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    polar2 = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )

    assert polar1 == polar2

    assert polar1 != PolarisationConfiguration(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )
    assert polar2 != PolarisationConfiguration(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )

    # Using Builder Pattern
    polar3 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    polar4 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )

    assert polar3 == polar4

    assert polar3 != PolarisationConfiguration(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )
    assert polar4 != PolarisationConfiguration(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )


def test_polarisation_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Polarisation Configuration objects are not considered equal to objects of
    other types.
    """
    polar = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    assert polar != 1

    # Using Builder Pattern
    polar1 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    assert polar1 != 1


def test_phase_dir_equals():
    """
    Verify that Phase Dir objects are considered equal when they have:
     - the same ra
     - the same dec
     - the same refrence_time
     - the same refrence_frame
    """
    phasedir1 = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    phasedir2 = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )

    assert phasedir1 == phasedir2

    assert phasedir1 != PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )
    assert phasedir2 != PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )

    # Using Builder Pattern
    phasedir3 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    phasedir4 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )

    assert phasedir3 == phasedir4

    assert phasedir3 != PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )
    assert phasedir4 != PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )


def test_phase_dir_equals_not_equal_to_other_objects():

    """
    Verify that Phase Dir objects are not considered equal to objects of
    other types.
    """
    phasedir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    assert phasedir != 1

    # Using Builder Pattern
    phasedir1 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    assert phasedir1 != 1


def test_field_equals():
    """
    Verify that Field Configuration objects are considered equal when they have:
     - the same field_id
     - the same pointing_fqdn
     - the same phase_dir
    """
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    field1 = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    field2 = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    assert field1 == field2

    assert field1 != FieldConfiguration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    assert field2 != FieldConfiguration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    # Using Builder Pattern
    phasedir = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    field3 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phasedir)
        .build()
    )
    field4 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phasedir)
        .build()
    )

    assert field3 == field4

    assert field3 != FieldConfiguration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    assert field4 != FieldConfiguration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )


def test_field_equals_not_equal_to_other_objects():

    """
    Verify that Field Configuration objects are not considered equal to objects of
    other types.
    """
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    field = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    assert field != 1

    # Using Builder Pattern
    field1 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=None)
        .build()
    )
    assert field1 != 1


def test_eb_scan_type_equals():
    """
    Verify that EBScanType objects are considered equal when they have:
     - the same scan_type_id
     - the same beams
     - the same derive_from
    """

    eb_scan_type1 = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    eb_scan_type2 = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    assert eb_scan_type1 == eb_scan_type2
    assert eb_scan_type1 != EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    assert eb_scan_type2 != EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )

    # Using Builder Pattern
    eb_scan_type3 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )
    eb_scan_type4 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    assert eb_scan_type3 == eb_scan_type4
    assert eb_scan_type3 != EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    assert eb_scan_type4 != EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )


def test_eb_scan_type_equals_not_equal_to_other_objects():

    """
    Verify that EBScanType objects are not considered equal to objects of
    other types.
    """
    eb_scan_type1 = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )

    assert eb_scan_type1 != 1

    # Using Builder Pattern
    eb_scan_type2 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    assert eb_scan_type2 != 1


def test_eb_scan_type_beam_equals():
    """
    Verify that EBScanTypeBeam objects are considered equal when they have:
     - the same field_id
     - the same channels_id
     - the same polarisations_id
    """
    eb_scan_type_beam1 = EBScanTypeBeam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )
    eb_scan_type_beam2 = EBScanTypeBeam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )

    assert eb_scan_type_beam1 == eb_scan_type_beam2

    assert eb_scan_type_beam1 != EBScanTypeBeam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam2 != EBScanTypeBeam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )

    # Using Builder pattern
    eb_scan_type_beam3 = (
        EBScanTypeBeamBuilder()
        .set_field_id(field_id="pss_field_0")
        .set_channels_id(channels_id="pulsar_channels")
        .set_polarisations_id(polarisations_id="all")
        .build()
    )
    eb_scan_type_beam4 = (
        EBScanTypeBeamBuilder()
        .set_field_id(field_id="pss_field_0")
        .set_channels_id(channels_id="pulsar_channels")
        .set_polarisations_id(polarisations_id="all")
        .build()
    )

    assert eb_scan_type_beam3 == eb_scan_type_beam4

    assert eb_scan_type_beam3 != EBScanTypeBeam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam4 != EBScanTypeBeam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )


def test_eb_scan_type_beam_equals_not_equal_to_other_objects():

    """
    Verify that EBScanTypeBeam objects are not considered equal to objects of
    other types.
    """
    eb_scan_type_beam = EBScanTypeBeam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam != 1

    # Using Builder Pattern
    eb_scan_type_beam1 = (
        EBScanTypeBeamBuilder()
        .set_field_id(field_id="pss_field_0")
        .set_channels_id(channels_id="pulsar_channels")
        .set_polarisations_id(polarisations_id="all")
        .build()
    )
    assert eb_scan_type_beam1 != 1


def test_script_equals():
    """
    Verify that ScriptConfiguration objects are considered equal when they have:
     - the same kind
     - the same name
     - the same version
    """
    script1 = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    script2 = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )

    assert script1 == script2

    assert script1 != ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )
    assert script2 != ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )

    # Using Builder Pattern
    script3 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    script4 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )

    assert script3 == script4

    assert script3 != ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )
    assert script4 != ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )


def test_scripts_equals_not_equal_to_other_objects():

    """
    Verify that ScriptConfiguration  objects are not considered equal to objects of
    other types.
    """
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    assert script != 1

    # Using Builder Pattern
    script1 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    assert script1 != 1


def test_pi_16_processing_block_equals():
    """
    Verify that PI16 ProcessingBlock objects are considered equal
    """
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    pb1 = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00003",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )
    pb2 = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00003",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )

    assert pb1 == pb2

    assert pb1 != ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )

    assert pb2 != ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )

    # Using Buikder pattern
    script1 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    pb3 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(
            parameters={
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
                                {
                                    "name": "plasma-storage-volume",
                                    "mountPath": "/plasma",
                                },
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
        )
        .set_sbi_ids(sbi_ids=[sbi_ids])
        .set_script(script=script1)
        .build()
    )
    pb4 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(
            parameters={
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
                                {
                                    "name": "plasma-storage-volume",
                                    "mountPath": "/plasma",
                                },
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
        )
        .set_sbi_ids(sbi_ids=[sbi_ids])
        .set_script(script=script1)
        .build()
    )

    assert pb3 == pb4

    assert pb3 != ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )

    assert pb4 != ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )


def test_pi_16_processing_block_not_equal_to_other_objects():
    """
    Verify that PI16 ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    p_block = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00003",
        parameters={
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
        },
        sbi_ids=[sbi_ids],
        script=script,
    )

    assert p_block != 1

    script1 = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(
            parameters={
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
                                {
                                    "name": "plasma-storage-volume",
                                    "mountPath": "/plasma",
                                },
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
        )
        .set_sbi_ids(sbi_ids=[sbi_ids])
        .set_script(script=script1)
        .build()
    )

    assert pb1 != 1


def test_execution_block_configuration_equals():
    """
    Verify that ExecutionBlockConfiguration objects are considered equal when they have:
     - the same eb_id
     - the same  max_length
     - the same context
     - the same beams
     - the same channels
     - the same polarisations
     - the same fields
     - the same scan_types
    """
    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    beams = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    scan_type = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )

    execution_block1 = ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00001",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )
    execution_block2 = ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00001",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )

    assert execution_block1 == execution_block2
    assert execution_block1 != ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )
    assert execution_block2 != ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )

    # Using Builder Pattern
    channel1 = (
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
    beam1 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    channels1 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    polarisation1 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir1 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    fields1 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir1)
        .build()
    )
    scan_type1 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    execution_block3 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=beam1)
        .set_channels(channels=channels1)
        .set_polarisations(polarisations=polarisation1)
        .set_fields(fields=fields1)
        .set_scan_types(scan_types=scan_type1)
        .build()
    )
    execution_block4 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=beam1)
        .set_channels(channels=channels1)
        .set_polarisations(polarisations=polarisation1)
        .set_fields(fields=fields1)
        .set_scan_types(scan_types=scan_type1)
        .build()
    )

    assert execution_block3 == execution_block4
    assert execution_block3 != ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )
    assert execution_block4 != ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )


def test_execution_block_not_equal_to_other_objects():
    """
    Verify that ExecutionBlockConfiguration  objects are not considered equal to objects of
    other types.
    """

    channel = Channel(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    beams = BeamConfiguration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = ChannelConfiguration(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )
    scan_type = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    execution_block = ExecutionBlockConfiguration(
        eb_id="eb-mvp01-20200325-00001",
        max_length=100,
        context={},
        beams=[beams],
        channels=[channels],
        polarisations=[polarisation],
        fields=[fields],
        scan_types=[scan_type],
    )

    assert execution_block != 1

    # Using Builder Pattern
    channel1 = (
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
    beam1 = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="pss1")
        .set_search_beam_id(search_beam_id=1)
        .set_function(function="pulsar search")
        .build()
    )
    channels1 = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    polarisation1 = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir1 = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    fields1 = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir1)
        .build()
    )
    scan_type1 = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    execution_block1 = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=beam1)
        .set_channels(channels=channels1)
        .set_polarisations(polarisations=polarisation1)
        .set_fields(fields=fields1)
        .set_scan_types(scan_types=scan_type1)
        .build()
    )

    assert execution_block1 != 1
