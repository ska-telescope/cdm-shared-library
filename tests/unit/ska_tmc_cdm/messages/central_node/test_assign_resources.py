"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import itertools

import pytest

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    EBScanType,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PhaseDir,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
)


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel1 = Channel(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = ScanType(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channels=[channel1],
    )
    workflow1 = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.1")
    pb1 = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[],
    )
    sdp1 = SDPConfiguration(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=[scan_type1],
        processing_blocks=[pb1],
    )

    request1 = AssignResourcesRequest(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequest(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request3 = AssignResourcesRequest(
        subarray_id=3,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00004",
    )

    assert request1 == request2

    assert request1 != request3
    assert request2 != request3


def test_assign_resources_request_mccs_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs1 = MCCSAllocate(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = AssignResourcesRequest(subarray_id=1, mccs=mccs1)
    request2 = AssignResourcesRequest(subarray_id=1, mccs=mccs1)
    assert request1 == request2
    assert request1 != AssignResourcesRequest(subarray_id=2, mccs=mccs1)


def test_assign_resources_request_from_mccs():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = MCCSAllocate(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )

    request = AssignResourcesRequest.from_mccs(subarray_id=1, mccs=mccs_allocate)

    expected = AssignResourcesRequest(
        subarray_id=1,
        mccs=MCCSAllocate(
            subarray_beam_ids=[1, 2, 3, 4, 5, 6],
            station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
            channel_blocks=[1, 2, 3, 4, 5],
        ),
    )
    assert request == expected


def test_assign_resources_request_from_dish():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest.from_dish(1, dish_allocation=dish_allocation)
    assert request == AssignResourcesRequest(1, dish_allocation=dish_allocation)


def test_assign_resources_request_dish_and_mccs_fail():
    """
    Verify that mccs & dish cannot be allocated together
    """
    mccs_allocate = MCCSAllocate(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )

    with pytest.raises(ValueError):
        dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
        AssignResourcesRequest(dish_allocation=dish_allocation, mccs=mccs_allocate)


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=None
    )
    assert request != 1
    assert request != object()


def test_assign_resources_request_eq_mccs_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    mccs = MCCSAllocate(subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3])
    request1 = AssignResourcesRequest(subarray_id=1, mccs=mccs)
    assert request1 != 1
    assert request1 != object()


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    unequal_allocation = DishAllocation(receptor_ids=["b", "aab"])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)

    assert response == AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != AssignResourcesResponse(dish_allocation=DishAllocation())
    assert response != AssignResourcesResponse(dish_allocation=unequal_allocation)


def test_assign_resources_response_eq_with_other_objects():
    """
    Verify that an AssignResourcesRequest response object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != 1
    assert response != object()


def test_assign_resources_request_for_low_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs1 = MCCSAllocate(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = AssignResourcesRequest(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request2 = AssignResourcesRequest(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request3 = AssignResourcesRequest(
        subarray_id=2,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/4.0",
    )
    assert request1 == request2

    assert request1 != request3


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = MCCSAllocate(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])

    with pytest.raises(ValueError):
        _ = AssignResourcesRequest(mccs=mccs)

    with pytest.raises(ValueError):
        _ = AssignResourcesRequest(dish_allocation=dish_allocation)


def test_modified_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel = Channel(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
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
    beams = BeamConfiguration(beam_id="vis0", function="visibilities")
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
    sdp_config = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request == AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request != AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=None,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00002",
    )
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(
        1,
        dish_allocation=None,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )


def test_modified_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
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
    sdp_config = SDPConfiguration(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request != 1
    assert request != object()


def test_low_assign_resources_request():
    """
    Verify creation of Low AssignResources request objects
    with both sdp & csp blocks and check equality
    """
    channel1 = Channel(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = ScanType(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channels=[channel1],
    )
    workflow1 = SDPWorkflow(name="vis_receive", kind="realtime", version="0.1.1")
    pb1 = ProcessingBlockConfiguration(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=[],
    )
    beams = BeamConfiguration(beam_id="vis0", function="visibilities")
    channels = ChannelConfiguration(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    polarization_config = PolarisationConfiguration(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase = PhaseDir(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    field = FieldConfiguration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase,
    )
    eb_scan_type = EBScanType(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    execution_block = ExecutionBlockConfiguration(
        eb_id="eb-test-20220916-00000",
        context={},
        max_length=3600,
        beams=[beams],
        channels=[channels],
        polarisations=[polarization_config],
        fields=[field],
        scan_types=[eb_scan_type],
    )
    sdp1 = SDPConfiguration(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=[scan_type1],
        processing_blocks=[pb1],
        execution_block=execution_block,
    )

    request1 = AssignResourcesRequest(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = AssignResourcesRequest(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request1 == request2
    assert request1 != 1 and request2 != object()
