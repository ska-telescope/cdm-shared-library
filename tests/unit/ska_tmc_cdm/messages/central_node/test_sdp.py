"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from ska_tmc_cdm.messages.central_node.sdp import ProcessingBlockConfiguration
from ska_tmc_cdm.messages.central_node.sdp import PbDependency, ScanType, Channel
from ska_tmc_cdm.messages.central_node.sdp import SDPWorkflow, SDPConfiguration


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
        744, 0, 2, 0.35e9, 1.05e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    channel2 = Channel(
        744, 0, 2, 0.35e9, 1.05e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    assert channel1 == channel2

    assert channel1 != Channel(
        744, 2000, 2, 0.35e9, 1.05e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    assert channel1 != Channel(
        744, 0, 1, 0.35e9, 1.05e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    assert channel1 != Channel(
        744, 0, 2, 0.36e9, 1.04e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    assert channel1 != Channel(744, 0, 2, 0.35e9, 1.05e9, [[2000, 4], [2200, 5]])


def test_channel_not_equal_to_other_objects():
    """
    Verify that Channel objects are not considered equal to objects of
    other types.
    """
    channel = Channel(744, 0, 2, 0.35e9, 1.05e9, [[0, 0], [200, 1], [744, 2], [944, 3]])
    assert channel != 1


def test_scan_type_equals():
    """
    Verify that ScanType objects are considered equal for the same passed parameter list
    """
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [[2000, 4], [2200, 5]])
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
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
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
