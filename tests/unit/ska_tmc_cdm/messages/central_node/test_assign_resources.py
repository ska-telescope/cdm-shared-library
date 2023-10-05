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
from tests.unit.ska_tmc_cdm.builder.central_node.assign_resources import (
    AssignResourcesRequestBuilder,
)

from .test_mccs import mccs_allocate_builder
from .test_sdp import (
    beam_configuration_builder,
    channel_builder,
    channel_configuration_builder,
    eb_scan_type_builder,
    execution_block_configuration_builder,
    fields_configuration_builder,
    phase_dir_configuration_builder,
    polarization_builder,
    processing_block_builder,
    scan_type_builder,
    scripts_builder,
    sdp_builder,
    workflow_configuration_builder,
)


def assign_request_builder(
    subarray_id=None,
    dish_allocation=None,
    sdp_config=None,
    interface=None,
    transaction_id=None,
    mccs=None,
    csp=None,
):
    """This assign request configuration builder is a test data builder for CDM assign request configuration"""
    return (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=subarray_id)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_config)
        .set_csp_config(csp_config=csp)
        .set_interface(interface=interface)
        .set_transaction_id(transaction_id=transaction_id)
        .set_mccs(mccs=mccs)
        .build()
    )


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel1 = channel_builder(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type_builder(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    workflow1 = workflow_configuration_builder(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    pb1 = processing_block_builder(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=None,
    )
    sdp1 = sdp_builder(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=[scan_type1],
        processing_blocks=[pb1],
    )

    request1 = assign_request_builder(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = assign_request_builder(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request3 = assign_request_builder(
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
    mccs1 = mccs_allocate_builder(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request_builder(subarray_id=1, mccs=mccs1)
    request2 = assign_request_builder(subarray_id=1, mccs=mccs1)
    assert request1 == request2
    assert request1 != assign_request_builder(subarray_id=2, mccs=mccs1)


def test_assign_resources_request_from_mccs():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = mccs_allocate_builder(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )

    request = AssignResourcesRequest.from_mccs(subarray_id=1, mccs=mccs_allocate)

    expected = assign_request_builder(
        subarray_id=1,
        mccs=mccs_allocate_builder(
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
    assert request == assign_request_builder(1, dish_allocation=dish_allocation)


def test_assign_resources_request_dish_and_mccs_fail():
    """
    Verify that mccs & dish cannot be allocated together
    """
    mccs_allocate = mccs_allocate_builder(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )

    with pytest.raises(ValueError):
        dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
        assign_request_builder(dish_allocation=dish_allocation, mccs=mccs_allocate)


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = assign_request_builder(
        1, dish_allocation=dish_allocation, sdp_config=None
    )
    assert request != 1
    assert request != object()


def test_assign_resources_request_eq_mccs_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    mccs = mccs_allocate_builder(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request_builder(subarray_id=1, mccs=mccs)
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
    mccs1 = mccs_allocate_builder(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request_builder(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request2 = assign_request_builder(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request3 = assign_request_builder(
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
    mccs = mccs_allocate_builder(
        subarray_beam_ids=[1, 2, 3, 4, 5, 6],
        station_ids=list(zip(itertools.count(1, 1), 1 * [2])),
        channel_blocks=[1, 2, 3, 4, 5],
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])

    with pytest.raises(ValueError):
        _ = assign_request_builder(mccs=mccs)

    with pytest.raises(ValueError):
        _ = assign_request_builder(dish_allocation=dish_allocation)


def test_modified_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel = channel_builder(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )

    scan_type = eb_scan_type_builder(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = scripts_builder(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    pb_config = processing_block_builder(
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
    beams = beam_configuration_builder(beam_id="vis0", function="visibilities")
    channels = channel_configuration_builder(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = polarization_builder(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = phase_dir_configuration_builder(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = fields_configuration_builder(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = execution_block_configuration_builder(
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
    sdp_config = sdp_builder(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = assign_request_builder(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request == assign_request_builder(
        1,
        dish_allocation=dish_allocation,
        sdp_config=sdp_config,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.1",
        transaction_id="txn-mvp01-20200325-00001",
    )

    assert request != assign_request_builder(
        1,
        dish_allocation=dish_allocation,
        sdp_config=None,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00002",
    )
    assert request != assign_request_builder(1, dish_allocation=None, sdp_config=None)
    assert request != assign_request_builder(
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
    channel = channel_builder(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = eb_scan_type_builder(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = scripts_builder(
        kind="realtime", name="test-receive-addresses", version="0.5.0"
    )
    pb_config = processing_block_builder(
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
    beams = beam_configuration_builder(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = channel_configuration_builder(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = polarization_builder(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = phase_dir_configuration_builder(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = fields_configuration_builder(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = execution_block_configuration_builder(
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
    sdp_config = sdp_builder(
        resources=resource,
        processing_blocks=[pb_config],
        execution_block=execution_block,
        interface="https://schema.skao.int/ska-sdp-assignresources/2.0",
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = assign_request_builder(
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
    channel1 = channel_builder(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type_builder(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    workflow1 = workflow_configuration_builder(
        name="vis_receive", kind="realtime", version="0.1.1"
    )
    pb1 = processing_block_builder(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=None,
    )
    beams = beam_configuration_builder(beam_id="vis0", function="visibilities")
    channels = channel_configuration_builder(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    polarization_config = polarization_builder(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase = phase_dir_configuration_builder(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    field = fields_configuration_builder(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase,
    )
    eb_scan_type = eb_scan_type_builder(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    execution_block = execution_block_configuration_builder(
        eb_id="eb-test-20220916-00000",
        context={},
        max_length=3600,
        beams=[beams],
        channels=[channels],
        polarisations=[polarization_config],
        fields=[field],
        scan_types=[eb_scan_type],
    )
    sdp1 = sdp_builder(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=[scan_type1],
        processing_blocks=[pb1],
        execution_block=execution_block,
    )

    request1 = assign_request_builder(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = assign_request_builder(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request1 == request2
    assert request1 != 1 and request2 != object()
