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
    ResourceConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
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


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDPWorkflow objects are not considered equal to objects of
    other types.
    """
    workflow = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.0")
    assert workflow != 1


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


def test_dependency_not_equal_to_other_objects():
    """
    Verify that PBDependency objects are not considered equal to objects of
    other types.
    """
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    assert dep != 1


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


def test_processing_block_not_equal_to_other_objects():
    """
    Verify that ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    p_block = ProcessingBlockConfiguration("pb-mvp01-20200325-00003", None, None, None)
    assert p_block != 1


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


def test_sdp_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    sdp = SDPConfiguration(None, None, None, None)
    assert sdp != 1


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
    resource = ResourceConfiguration(
        csp_links=[1, 2, 3, 4], receptors=["FS4", "FS8"], receive_nodes=10
    )

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
    resource = ResourceConfiguration(
        csp_links=[1, 2, 3, 4], receptors=["FS4", "FS8"], receive_nodes=10
    )
    sdp = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    assert sdp != 1


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


def test_beam_equals_not_equal_to_other_objects():
    """
    Verify that Beam objects are not considered equal to objects of
    other types.
    """
    beam = BeamConfiguration(beam_id="pss1", search_beam_id=1, function="pulsar search")
    assert beam != 1


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


def test_polarisation_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Polarisation Configuration objects are not considered equal to objects of
    other types.
    """
    polar = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    assert polar != 1


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


def test_phase_dir_equals_not_equal_to_other_objects():

    """
    Verify that Phase Dir objects are not considered equal to objects of
    other types.
    """
    phasedir = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    assert phasedir != 1


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


def test_resource_equals():
    """
    Verify that Resource Configuration objects are considered equal when they have:
     - the same csp_links
     - the same receptors
     - the same receiver_nodes
    """
    resource1 = ResourceConfiguration(
        csp_links=[1, 2, 3, 4], receptors=["FS4", "FS8"], receive_nodes=10
    )
    resource2 = ResourceConfiguration(
        csp_links=[1, 2, 3, 4], receptors=["FS4", "FS8"], receive_nodes=10
    )

    assert resource1 == resource2

    assert resource1 != ResourceConfiguration(
        csp_links=[1, 2, 3], receptors=["FS4", "FS8"], receive_nodes=10
    )
    assert resource2 != ResourceConfiguration(
        csp_links=[1, 2, 3], receptors=["FS4", "FS8"], receive_nodes=10
    )


def test_resource_equals_not_equal_to_other_objects():

    """
    Verify that Resource Configuration objects are not considered equal to objects of
    other types.
    """
    resource = ResourceConfiguration(
        csp_links=[1, 2, 3, 4], receptors=["FS4", "FS8"], receive_nodes=10
    )
    assert resource != 1


def test_ebscantype_equals():
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


def test_ebscantype_equals_not_equal_to_other_objects():

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


def test_ebscantypebeam_equals():
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


def test_ebscantypebeam_equals_not_equal_to_other_objects():

    """
    Verify that EBScanTypeBeam objects are not considered equal to objects of
    other types.
    """
    eb_scan_type_beam = EBScanTypeBeam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam != 1


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


def test_scripts_equals_not_equal_to_other_objects():

    """
    Verify that ScriptConfiguration  objects are not considered equal to objects of
    other types.
    """
    script = ScriptConfiguration(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    assert script != 1


def test_PI16_processing_block_equals():
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


def test_PI_16_processing_block_not_equal_to_other_objects():
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


def test_executionblockconfiguration_equals():
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


def test_executionblock_not_equal_to_other_objects():
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
