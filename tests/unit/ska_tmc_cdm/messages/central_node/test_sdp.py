"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from tests.unit.ska_tmc_cdm.builder.central_node.sdp import (
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


def eb_scantype_beam(field_id=None, channels_id=None, polarisations_id=None):
    return (
        EBScanTypeBeamBuilder()
        .set_field_id(field_id=field_id)
        .set_channels_id(channels_id=channels_id)
        .set_polarisations_id(polarisations_id=polarisations_id)
        .build()
    )


def execution(
    eb_id=None,
    max_length=None,
    context=None,
    beams=None,
    channels=None,
    polarisations=None,
    fields=None,
    scan_types=None,
):
    return (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id=eb_id)
        .set_max_length(max_length=max_length)
        .set_context(context=context)
        .set_beams(beams=beams)
        .set_channels(channels=channels)
        .set_polarisations(polarisations=polarisations)
        .set_fields(fields=fields)
        .set_scan_types(scan_types=scan_types)
        .build()
    )


def fields_configuration(field_id=None, pointing_fqdn=None, phase_dir=None):
    return (
        FieldConfigurationBuilder()
        .set_field_id(field_id=field_id)
        .set_pointing_fqdn(pointing_fqdn=pointing_fqdn)
        .set_phase_dir(phase_dir=phase_dir)
        .build()
    )


def beam_config(
    beam_id=None,
    function=None,
    search_beam_id=None,
    timing_beam_id=None,
    vlbi_beam_id=None,
):
    return (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id=beam_id)
        .set_function(function=function)
        .set_search_beam_id(search_beam_id=search_beam_id)
        .set_timing_beam_id(timing_beam_id=timing_beam_id)
        .set_vlbi_beam_id(vlbi_beam_id=vlbi_beam_id)
        .build()
    )


def eb_scan(scan_type_id=None, beams=None, derive_from=None):
    return (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id=scan_type_id)
        .set_beams(beams=beams)
        .set_derive_from(derive_from=derive_from)
        .build()
    )


def phase_dir_configuration(
    ra=None, dec=None, reference_time=None, reference_frame=None
):
    return (
        PhaseDirBuilder()
        .set_ra(ra=ra)
        .set_dec(dec=dec)
        .set_reference_time(reference_time=reference_time)
        .set_reference_frame(reference_frame=reference_frame)
        .build()
    )


def sdp(
    eb_id=None,
    max_length=None,
    scan_types=None,
    processing_blocks=None,
    execution_block=None,
    resources=None,
    interface=None,
):
    return (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id=eb_id)
        .set_max_length(max_length=max_length)
        .set_scan_types(scan_types=scan_types)
        .set_processing_blocks(processing_blocks=processing_blocks)
        .set_execution_block(execution_block=execution_block)
        .set_resources(resources=resources)
        .set_interface(interface=interface)
        .build()
    )


def channel_configure(
    count=None,
    start=None,
    stride=None,
    freq_min=None,
    freq_max=None,
    link_map=None,
    spectral_window_id=None,
):
    return (
        ChannelBuilder()
        .set_count(count=count)
        .set_start(start=start)
        .set_stride(stride=stride)
        .set_freq_min(freq_min=freq_min)
        .set_freq_max(freq_max=freq_max)
        .set_link_map(link_map=link_map)
        .set_spectral_window_id(spectral_window_id=spectral_window_id)
        .build()
    )


def scan_type(scan_type_id=None, reference_frame=None, ra=None, dec=None, channel=None):
    return (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id=scan_type_id)
        .set_reference_frame(reference_frame=reference_frame)
        .set_ra(ra=ra)
        .set_dec(dec=dec)
        .set_channels(channels=channel)
        .build()
    )


def workflow_configuration(name=None, kind=None, version=None):
    return (
        SDPWorkflowBuilder()
        .set_name(name=name)
        .set_kind(kind=kind)
        .set_version(version=version)
        .build()
    )


def pbdependency(pb_id=None, kind=None):
    return PbDependencyBuilder().set_pb_id(pb_id=pb_id).set_kind(kind=kind).build()


def processing_block(
    pb_id=None,
    workflow=None,
    parameters=None,
    dependencies=None,
    sbi_ids=None,
    script=None,
):
    return (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id=pb_id)
        .set_workflow(workflow=workflow)
        .set_parameters(parameters=parameters)
        .set_dependencies(dependencies=dependencies)
        .set_sbi_ids(sbi_ids=sbi_ids)
        .set_script(script=script)
        .build()
    )


def scripts(kind=None, name=None, version=None):
    return (
        ScriptConfigurationBuilder()
        .set_kind(kind=kind)
        .set_name(name=name)
        .set_version(version=version)
        .build()
    )


def channel_configuration(channels_id=None, spectral_windows=None):
    return (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id=channels_id)
        .set_spectral_windows(spectral_windows=[spectral_windows])
        .build()
    )


def polarization(polarisations_id=None, corr_type=None):
    return (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id=polarisations_id)
        .set_corr_type(corr_type=corr_type)
        .build()
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
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channel2 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    assert channel1 == channel2

    assert channel1 != channel_configure(
        count=743,
        start=0,
        stride=1,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [220, 1], [744, 2], [944, 3]],
        spectral_window_id=None,
    )


def test_channel_not_equal_to_other_objects():
    """
    Verify that Channel objects are not considered equal to objects of
    other types.
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    assert channel1 != 1


def test_scan_type_equals():
    """
    Verify that ScanType objects are considered equal for the same passed parameter list
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channel2 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1, channel2],
    )
    scan_type2 = scan_type(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1, channel2],
    )

    assert scan_type1 == scan_type2


def test_scan_type_not_equal_to_other_objects():
    """
    Verify that ScanType objects are not considered equal to objects of
    other types.
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    assert scan_type1 != 1


def test_workflow_equals():
    """
    Verify that SDPWorkflow objects are considered equal when they have:
     - the same name
     - the same kind
     - the same version
    """
    workflow1 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    workflow2 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    assert workflow1 == workflow2
    assert workflow1 != workflow_configuration(
        name="vis_receive", kind="realtime", version="0.0.1"
    )


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDPWorkflow objects are not considered equal to objects of
    other types.
    """
    workflow1 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    assert workflow1 != 1


def test_dependency_equals():
    """
    Verify that PBDependency objects are considered equal when they have:
     - the same PB ID
     - the same type
    """
    dep1 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])
    dep2 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])

    assert dep1 == dep2

    assert dep1 != pbdependency("pb-mvp01-20200325-00001", ["calibration"])


def test_dependency_not_equal_to_other_objects():
    """
    Verify that PBDependency objects are not considered equal to objects of
    other types.
    """
    dep1 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])
    assert dep1 != 1


def test_processing_block_equals():
    """
    Verify that ProcessingBlock objects are considered equal
    """
    workflow1 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    dep1 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])
    pb1 = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[dep1],
    )
    pb2 = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[dep1],
    )
    assert pb1 == pb2

    assert pb1 != processing_block("pb-mvp01-20200325-00003", workflow1, None, [dep1])


def test_processing_block_not_equal_to_other_objects():
    """
    Verify that ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    workflow1 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    dep1 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])
    p_block = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[dep1],
    )
    assert p_block != 1


def test_sdp_configuration_block_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    scan_type2 = scan_type(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    scan_types = [scan_type1, scan_type2]

    workflow1 = workflow_configuration(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    workflow2 = workflow_configuration(
        name="test_realtime", kind="realtime", version="0.1.0"
    )
    workflow3 = workflow_configuration(name="ical", kind="batch", version="0.1.0")
    workflow4 = workflow_configuration(name="dpreb", kind="batch", version="0.1.0")

    dep1 = pbdependency(pb_id="pb-mvp01-20200325-00001", kind=["visibilities"])
    dep2 = pbdependency(pb_id="pb-mvp01-20200325-00003", kind=["calibration"])

    pb1 = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[dep1],
    )
    pb2 = processing_block(
        pb_id="pb-mvp01-20200325-00002",
        workflow=workflow2,
        parameters={},
        dependencies=[dep2],
    )
    pb3 = processing_block(
        pb_id="pb-mvp01-20200325-00003",
        workflow=workflow3,
        parameters={},
        dependencies=[dep1],
    )
    pb4 = processing_block(
        pb_id="pb-mvp01-20200325-00004",
        workflow=workflow4,
        parameters={},
        dependencies=[dep2],
    )
    processing_blocks = [pb1, pb2, pb3, pb4]

    sdp1 = sdp(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=scan_types,
        processing_blocks=processing_blocks,
    )
    sdp2 = sdp(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=scan_types,
        processing_blocks=processing_blocks,
    )

    assert sdp1 == sdp2

    assert sdp1 != sdp("sbi-mvp01-20200325-00001", 0.0, scan_types, processing_blocks)
    assert sdp1 != sdp("sbi-mvp01-20200325-00001", 100.0, None, processing_blocks)
    assert sdp1 != sdp("sbi-mvp01-20200325-00002", 100.0, scan_types, None)
    assert sdp1 != sdp(None, None, None, None)


def test_sdp_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    sdp1 = sdp(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=None,
        processing_blocks=None,
    )
    assert sdp1 != 1


def test_sdp_modified_configuration_block_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """

    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    script1 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    pb1 = processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )
    beams1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    polarisation1 = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    execution_block1 = execution(
        eb_id="eb-mvp01-20200325-00001",
        context={},
        max_length=100,
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )
    resource1 = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp3 = sdp(
        processing_blocks=[pb1],
        resources=resource1,
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )
    sdp4 = sdp(
        processing_blocks=[pb1],
        resources=resource1,
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.1",
    )

    assert sdp3 == sdp4

    assert sdp3 != sdp(
        resources=resource1,
        processing_blocks=[pb1],
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    assert sdp4 != sdp(
        resources=resource1,
        processing_blocks=[pb1],
        execution_block=execution_block1,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )


def test_sdp_modified_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    script1 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    pb1 = processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )
    beams1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    polarisation1 = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    execution_block1 = execution(
        eb_id="eb-mvp01-20200325-00001",
        context={},
        max_length=100,
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )
    resource1 = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp1 = sdp(
        processing_blocks=[pb1],
        resources=resource1,
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
    beam1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    beam2 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)

    assert beam1 == beam2


def test_beam_equals_not_equal_to_other_objects():
    """
    Verify that Beam objects are not considered equal to objects of
    other types.
    """
    beam1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    assert beam1 != 1


def test_chanel_configuration_equals():
    """
    Verify that Channels Configuration objects are considered equal when they have:
     - the same Channels ID
     - the same Spectral Windows
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    channels2 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )

    assert channels1 == channels2

    assert channels1 != channel_configuration(
        channels_id="pulsar_channels",
        spectral_windows=[channel1],
    )
    assert channels2 != channel_configuration(
        channels_id="pulsar_channels",
        spectral_windows=[channel1],
    )


def test_chanel_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Channels Configuration objects are not considered equal to objects of
    other types.
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    assert channels1 != 1


def test_polarisation_configuration_equals():
    """
    Verify that Polarisation Configuration objects are considered equal when they have:
     - the same polarisation_id
     - the same corr_type
    """
    polar1 = polarization(polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"])
    polar2 = polarization(polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"])

    assert polar1 == polar2

    assert polar1 != polarization(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )
    assert polar2 != polarization(
        polarisations_id="all", corr_type=["XY", "XY", "YY", "YX"]
    )


def test_polarisation_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Polarisation Configuration objects are not considered equal to objects of
    other types.
    """
    polar1 = polarization(polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"])
    assert polar1 != 1


def test_phase_dir_equals():
    """
    Verify that Phase Dir objects are considered equal when they have:
     - the same ra
     - the same dec
     - the same refrence_time
     - the same refrence_frame
    """
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    phase_dir2 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )

    assert phase_dir1 == phase_dir2

    assert phase_dir1 != phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )
    assert phase_dir2 != phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF4"
    )


def test_phase_dir_equals_not_equal_to_other_objects():

    """
    Verify that Phase Dir objects are not considered equal to objects of
    other types.
    """
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    assert phase_dir1 != 1


def test_field_equals():
    """
    Verify that Field Configuration objects are considered equal when they have:
     - the same field_id
     - the same pointing_fqdn
     - the same phase_dir
    """
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    fields2 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )

    assert fields1 == fields2

    assert fields1 != fields_configuration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    assert fields2 != fields_configuration(
        field_id="field_b",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )


def test_field_equals_not_equal_to_other_objects():

    """
    Verify that Field Configuration objects are not considered equal to objects of
    other types.
    """
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    assert fields1 != 1


def test_eb_scan_type_equals():
    """
    Verify that EBScanType objects are considered equal when they have:
     - the same scan_type_id
     - the same beams
     - the same derive_from
    """
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    eb_scan2 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    assert eb_scan1 == eb_scan2
    assert eb_scan1 != eb_scan(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    assert eb_scan2 != eb_scan(
        scan_type_id="science",
        beams={"vis0": {"pss_field_1", "pulsar_channels", "all"}},
        derive_from=".default",
    )


def test_eb_scan_type_equals_not_equal_to_other_objects():

    """
    Verify that EBScanType objects are not considered equal to objects of
    other types.
    """
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )

    assert eb_scan1 != 1


def test_eb_scan_type_beam_equals():
    """
    Verify that EBScanTypeBeam objects are considered equal when they have:
     - the same field_id
     - the same channels_id
     - the same polarisations_id
    """
    eb_scan_type_beam1 = eb_scantype_beam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )
    eb_scan_type_beam2 = eb_scantype_beam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )

    assert eb_scan_type_beam1 == eb_scan_type_beam2

    assert eb_scan_type_beam1 != eb_scantype_beam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam2 != eb_scantype_beam(
        field_id="pss_field_1", channels_id="pulsar_channels", polarisations_id="all"
    )


def test_eb_scan_type_beam_equals_not_equal_to_other_objects():

    """
    Verify that EBScanTypeBeam objects are not considered equal to objects of
    other types.
    """
    eb_scan_type_beam1 = eb_scantype_beam(
        field_id="pss_field_0", channels_id="pulsar_channels", polarisations_id="all"
    )
    assert eb_scan_type_beam1 != 1


def test_script_equals():
    """
    Verify that ScriptConfiguration objects are considered equal when they have:
     - the same kind
     - the same name
     - the same version
    """
    script1 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    script2 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")

    assert script1 == script2

    assert script1 != scripts(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )
    assert script2 != scripts(
        kind="realtime", name="test-receive-addresses", version="0.5.1"
    )


def test_scripts_equals_not_equal_to_other_objects():

    """
    Verify that ScriptConfiguration  objects are not considered equal to objects of
    other types.
    """
    script1 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    assert script1 != 1


def test_pi_16_processing_block_equals():
    """
    Verify that PI16 ProcessingBlock objects are considered equal
    """
    sbi_ids_1 = "sbi-mvp01-20200325-00001"
    script1 = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    pb1 = processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )
    pb2 = processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )

    assert pb1 == pb2

    assert pb1 != processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )

    assert pb2 != processing_block(
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
        },
        sbi_ids=[sbi_ids_1],
        script=script1,
    )


def test_pi_16_processing_block_not_equal_to_other_objects():
    """
    Verify that PI16 ProcessingBlock objects are not considered equal to objects of
    other types.
    """

    p_block = processing_block(
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
        },
        sbi_ids=None,
        script=None,
    )
    assert p_block != 1


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
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    beams1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    polarisation1 = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    execution_block1 = execution(
        eb_id="eb-mvp01-20200325-00001",
        context={},
        max_length=100,
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )
    execution_block2 = execution(
        eb_id="eb-mvp01-20200325-00001",
        context={},
        max_length=100,
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )

    assert execution_block1 == execution_block2
    assert execution_block1 != execution(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )
    assert execution_block2 != execution(
        eb_id="eb-mvp01-20200325-00003",
        max_length=100,
        context={},
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )


def test_execution_block_not_equal_to_other_objects():
    """
    Verify that ExecutionBlockConfiguration  objects are not considered equal to objects of
    other types.
    """
    channel1 = channel_configure(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    channels1 = channel_configuration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    eb_scan1 = eb_scan(
        scan_type_id="science_A",
        beams={"vis0": {"pss_field_0", "pulsar_channels", "all"}},
        derive_from=".default",
    )
    beams1 = beam_config(beam_id="pss1", function="pulsar search", search_beam_id=1)
    polarisation1 = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir1 = phase_dir_configuration(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields1 = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir1,
    )
    execution_block1 = execution(
        eb_id="eb-mvp01-20200325-00001",
        context={},
        max_length=100,
        beams=[beams1],
        channels=[channels1],
        polarisations=[polarisation1],
        fields=[fields1],
        scan_types=[eb_scan1],
    )
    assert execution_block1 != 1
