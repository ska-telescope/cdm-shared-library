"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    FieldConfiguration,
    PbDependency,
    PhaseDir,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ResourceBlockConfiguration,
    ScanType,
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
    workflow1 = SDPWorkflow("name", "kind", "version")
    workflow2 = SDPWorkflow("name", "kind", "version")
    assert workflow1 == workflow2

    assert workflow1 != SDPWorkflow("", "kind", "version")
    assert workflow1 != SDPWorkflow("name", "", "version")
    assert workflow1 != SDPWorkflow("name", "kind", "")


def test_workflow_not_equal_to_other_objects():
    """
    Verify that SDPWorkflow objects are not considered equal to objects of
    other types.
    """
    workflow = SDPWorkflow("name", "kind", "version")
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
        "fsp_2_channels",
        744,
        0,
        2,
        0.35e9,
        0.368e9,
        [[0, 0], [200, 1], [744, 2], [944, 3]],
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


def test_beam_equals():
    """
    Verify that Beam objects are considered equal when they have:
     - the same Beam ID
     - the same Function
     - the same Search Beam ID
    """
    beam1 = BeamConfiguration("pss1", 1, "pulsar search")
    beam2 = BeamConfiguration("pss1", 1, "pulsar search")

    assert beam1 == beam2

    assert beam1 != BeamConfiguration("pss1", 2, "pulsar search")
    assert beam2 != BeamConfiguration("pss1", 2, "pulsar search")


def test_beam_equals_not_equal_to_other_objects():
    """
    Verify that Beam objects are not considered equal to objects of
    other types.
    """
    beam = BeamConfiguration("pss1", 1, "pulsar search")
    assert beam != 1


def test_chanel_configuration_equals():
    """
    Verify that Channels Configuration objects are considered equal when they have:
     - the same Channels ID
     - the same Spectral Windows
    """
    channels1 = ChannelConfiguration(
        "vis_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )
    channels2 = ChannelConfiguration(
        "vis_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )

    assert channels1 == channels2

    assert channels1 != ChannelConfiguration(
        "pulsar_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )
    assert channels2 != ChannelConfiguration(
        "pulsar_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )


def test_chanel_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Channels Configuration objects are not considered equal to objects of
    other types.
    """
    channels = ChannelConfiguration(
        "pulsar_channels",
        [
            "fsp_2_channels",
            744,
            0,
            2,
            0.35e9,
            1.05e9,
            [[0, 0], [200, 1], [744, 2], [944, 3]],
        ],
    )
    assert channels != 1


def test_polarisation_configuration_equals():
    """
    Verify that Polarisation Configuration objects are considered equal when they have:
     - the same polarisation_id
     - the same corr_type
    """
    polar1 = PolarisationConfiguration("all", ["XX", "XY", "YY", "YX"])
    polar2 = PolarisationConfiguration("all", ["XX", "XY", "YY", "YX"])

    assert polar1 == polar2

    assert polar1 != PolarisationConfiguration("all", ["XY", "XY", "YY", "YX"])
    assert polar2 != PolarisationConfiguration("all", ["YY", "XY", "YY", "YX"])


def test_polarisation_configuration_equals_not_equal_to_other_objects():

    """
    Verify that Channels Configuration objects are not considered equal to objects of
    other types.
    """
    polar = PolarisationConfiguration("all", ["XY", "XY", "YY", "YX"])
    assert polar != 1


def test_phase_dir_equals():
    """
    Verify that Phase Dir objects are considered equal when they have:
     - the same ra
     - the same dec
     - the same refrence_time
     - the same refrence_frame
    """
    phasedir1 = PhaseDir([123, 0.1], [123, 0.1], "...", "ICRF3")
    phasedir2 = PhaseDir([123, 0.1], [123, 0.1], "...", "ICRF3")

    assert phasedir1 == phasedir2

    assert phasedir1 != PhaseDir([123, 0.1], [123, 0.1], "...", "ICRF34")
    assert phasedir2 != PhaseDir([123, 0.1], [123, 0.1], "...", "ICRF34")


def test_phase_dir_equals_not_equal_to_other_objects():

    """
    Verify that Channels Configuration objects are not considered equal to objects of
    other types.
    """
    phasedir = PhaseDir([123, 0.1], [123, 0.1], "...", "ICRF3")
    assert phasedir != 1


def test_field_equals():
    """
    Verify that Field Configuration objects are considered equal when they have:
     - the same field_id
     - the same pointing_fqdn
     - the same phase_dir
    """
    field1 = FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointing",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )
    field2 = FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointing",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )

    assert field1 == field2

    assert field1 != FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointings",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )
    assert field2 != FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointings",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )


def test_field_equals_not_equal_to_other_objects():

    """
    Verify that Field Configuration objects are not considered equal to objects of
    other types.
    """
    field = FieldConfiguration(
        "field_a",
        "low-tmc/telstate/0/pointing",
        [[123, 0.1], [123, 0.1], "...", "ICRF3"],
    )
    assert field != 1


def test_resource_equals():
    """
    Verify that Resource Configuration objects are considered equal when they have:
     - the same csp_links
     - the same receptors
     - the same receiver_nodes
    """
    resource1 = ResourceBlockConfiguration([1, 2, 3, 4], ["FS4", "FS8"], 10)
    resource2 = ResourceBlockConfiguration([1, 2, 3, 4], ["FS4", "FS8"], 10)

    assert resource1 == resource2

    assert resource1 != ResourceBlockConfiguration([1, 2, 3], ["FS4", "FS8"], 10)
    assert resource2 != ResourceBlockConfiguration([1, 2, 3], ["FS4", "FS8"], 10)


def test_resource_equals_not_equal_to_other_objects():

    """
    Verify that Field Configuration objects are not considered equal to objects of
    other types.
    """
    resource = ResourceBlockConfiguration([1, 2, 3, 4], ["FS4", "FS8"], 10)
    assert resource != 1
