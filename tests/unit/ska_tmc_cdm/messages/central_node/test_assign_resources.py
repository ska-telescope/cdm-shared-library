"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
import itertools

import pytest

from ska_tmc_cdm.messages.central_node.assign_resources import (
    LOW_SCHEMA,
    MID_SCHEMA,
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from tests.unit.ska_tmc_cdm.builder.central_node.assign_resources import (
    AssignResourcesRequestBuilder,
)

from ...builder.central_node.common import DishAllocateBuilder
from ...builder.central_node.mccs import MCCSAllocateBuilder
from ...builder.central_node.sdp import (
    BeamConfigurationBuilder,
    ChannelBuilder,
    ChannelConfigurationBuilder,
    EBScanTypeBuilder,
    ExecutionBlockConfigurationBuilder,
    FieldConfigurationBuilder,
    PhaseDirBuilder,
    PolarisationConfigurationBuilder,
    ProcessingBlockConfigurationBuilder,
    ScanTypeBuilder,
    ScriptConfigurationBuilder,
    SDPConfigurationBuilder,
    SDPWorkflowBuilder,
)


def get_parameters():
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


def assign_request_builder(
    subarray_id=None,
    dish_allocation=None,
    sdp_config=None,
    interface=None,
    transaction_id=None,
    mccs=None,
):
    """This assign request configuration builder is a test data builder for CDM assign request configuration"""
    return (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=subarray_id)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_config)
        .set_interface(interface=interface)
        .set_transaction_id(transaction_id=transaction_id)
        .set_mccs(mccs=mccs)
        .build()
    )


@pytest.mark.parametrize(
    "assign_request, expected_interface",
    (
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
                .build()
            )
            .build(),
            MID_SCHEMA,
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_interface(interface="foo")
            .set_dish_allocation(
                dish_allocation=DishAllocateBuilder()
                .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
                .build()
            )
            .build(),
            "foo",
        ),
        (
            AssignResourcesRequestBuilder()
            .set_subarray_id(subarray_id=1)
            .set_mccs(
                mccs=MCCSAllocateBuilder()
                .set_subarray_beam_ids(subarray_beam_ids=[1])
                .set_station_ids(station_ids=[[1, 2]])
                .set_channel_blocks(channel_blocks=[3])
                .build()
            )
            .build(),
            LOW_SCHEMA,
        ),
    ),
)
def test_assign_resources_request_has_interface_set_on_creation(
    assign_request, expected_interface
):
    """
    Verify that the interface is set correctly if not provided
    """
    assert assign_request.interface == expected_interface


def test_assign_resources_request_mccs_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs1 = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1])
        .set_station_ids(station_ids=[[1, 2]])
        .set_channel_blocks(channel_blocks=[3])
        .build()
    )
    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(mccs=mccs1)
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(mccs=mccs1)
        .build()
    )
    assert request1 == request2
    assert (
        request1
        != AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=2)
        .set_mccs(mccs=mccs1)
        .build()
    )


def test_assign_resources_request_from_mccs():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
        .build()
    )

    request = AssignResourcesRequest.from_mccs(subarray_id=1, mccs=mccs_allocate)

    expected = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(
            mccs=MCCSAllocateBuilder()
            .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
            .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
            .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
            .build()
        )
        .build()
    )
    assert request == expected


def test_assign_resources_request_from_dish():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    request = AssignResourcesRequest.from_dish(1, dish_allocation=dish_allocation)
    assert (
        request
        == AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .build()
    )


def test_assign_resources_request_dish_and_mccs_fail():
    """
    Verify that mccs & dish cannot be allocated together
    """
    mccs_allocate = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
        .build()
    )

    with pytest.raises(ValueError):
        dish_allocation = (
            DishAllocateBuilder()
            .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
            .build()
        )
        AssignResourcesRequestBuilder().set_dish_allocation(
            dish_allocation=dish_allocation
        ).set_mccs(mccs=mccs_allocate).build()


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    request = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .build()
    )
    assert request != 1
    assert request != object()


def test_assign_resources_request_eq_mccs_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    mccs = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1])
        .set_station_ids(station_ids=[[1, 2]])
        .set_channel_blocks(channel_blocks=[3])
        .build()
    )
    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(mccs=mccs)
        .build()
    )
    assert request1 != 1
    assert request1 != object()


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    unequal_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["b", "aab"]))
        .build()
    )
    response = AssignResourcesResponse(dish_allocation=dish_allocation)

    assert response == AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != AssignResourcesResponse(
        dish_allocation=DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset())
        .build()
    )
    assert response != AssignResourcesResponse(dish_allocation=unequal_allocation)


def test_assign_resources_response_eq_with_other_objects():
    """
    Verify that an AssignResourcesResponse object is not considered equal to
    objects of other types.
    """
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != 1
    assert response != object()


def test_assign_resources_request_for_low_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs1 = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1])
        .set_station_ids(station_ids=[[1, 2]])
        .set_channel_blocks(channel_blocks=[3])
        .build()
    )
    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(mccs=mccs1)
        .set_interface(
            interface="https://schema.skao.int/ska-low-tmc-assignresources/2.0"
        )
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_mccs(mccs=mccs1)
        .set_interface(
            interface="https://schema.skao.int/ska-low-tmc-assignresources/2.0"
        )
        .build()
    )
    request3 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=2)
        .set_mccs(mccs=mccs1)
        .set_interface(
            interface="https://schema.skao.int/ska-low-tmc-assignresources/4.0"
        )
        .build()
    )
    assert request1 == request2
    assert request1 != request3


def test_assign_resources_if_no_subarray_id_argument():
    """
    Verify that the boolean release_all_mid argument is required.
    """
    mccs = (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=[1, 2, 3, 4, 5, 6])
        .set_station_ids(station_ids=list(zip(itertools.count(1, 1), 1 * [2])))
        .set_channel_blocks(channel_blocks=[1, 2, 3, 4, 5])
        .build()
    )
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", " b", "aab"]))
        .build()
    )

    with pytest.raises(ValueError):
        _ = AssignResourcesRequestBuilder().set_mccs(mccs=mccs).build()

    with pytest.raises(ValueError):
        _ = (
            AssignResourcesRequestBuilder()
            .set_dish_allocation(dish_allocation=dish_allocation)
            .build()
        )


def test_modified_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """

    channel = (
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

    scan_type = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"field_id": "field_a"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    sbi_ids = "sbi-mvp01-20200325-00001"

    script = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )

    pb_config = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(parameters=get_parameters())
        .set_sbi_ids(sbi_ids=[sbi_ids])
        .set_script(script=script)
        .build()
    )

    beams = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="vis0")
        .set_function(function="visibilities")
        .build()
    )

    channels = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel])
        .build()
    )

    polarisation = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )

    phase_dir = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )

    fields = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir)
        .build()
    )

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisation])
        .set_fields(fields=[fields])
        .set_scan_types(scan_types=[scan_type])
        .build()
    )

    resource = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }

    sdp_config = (
        SDPConfigurationBuilder()
        .set_processing_blocks(processing_blocks=[pb_config])
        .set_execution_block(execution_block=execution_block)
        .set_resources(resources=resource)
        .set_interface(interface="https://schema.skao.int/ska-sdp-assignresources/2.0")
        .build()
    )

    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )

    request = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_config)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert (
        request
        == AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_config)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert (
        request
        != AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    assert (
        request
        != AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .build()
    )
    assert (
        request
        != AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp_config)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )


def test_modified_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """

    channel = (
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
    scan_type = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"field_id": "field_a"}})
        .set_derive_from(derive_from=".default")
        .build()
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = (
        ScriptConfigurationBuilder()
        .set_kind(kind="realtime")
        .set_name(name="test-receive-addresses")
        .set_version(version="0.5.0")
        .build()
    )
    pb_config = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00003")
        .set_parameters(parameters=get_parameters())
        .set_sbi_ids(sbi_ids=[sbi_ids])
        .set_script(script=script)
        .build()
    )

    beams = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="vis0")
        .set_function(function="visibilities")
        .build()
    )
    channels = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel])
        .build()
    )
    polarisation = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    fields = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir)
        .build()
    )

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarisation])
        .set_fields(fields=[fields])
        .set_scan_types(scan_types=[scan_type])
        .build()
    )
    resource = {
        "csp_links": [1, 2, 3, 4],
        "receptors": ["FS4", "FS8"],
        "receive_nodes": 10,
    }
    sdp_config = (
        SDPConfigurationBuilder()
        .set_processing_blocks(processing_blocks=[pb_config])
        .set_execution_block(execution_block=execution_block)
        .set_resources(resources=resource)
        .set_interface(interface="https://schema.skao.int/ska-sdp-assignresources/2.0")
        .build()
    )
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["ac", "b", "aab"]))
        .build()
    )
    request = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp_config)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    assert request != 1
    assert request != object()


def test_low_assign_resources_request():
    """
    Verify creation of Low AssignResources request objects
    with both sdp & csp blocks and check equality
    """
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

    workflow1 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.1")
        .build()
    )

    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_workflow(workflow=workflow1)
        .set_parameters(parameters={})
        .build()
    )

    beams = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="vis0")
        .set_function(function="visibilities")
        .build()
    )

    channels = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )
    polarization_config = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )
    phase_dir = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    field = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase_dir)
        .build()
    )

    eb_scan_type = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"field_id": "field_a"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_context(context={})
        .set_max_length(max_length=100)
        .set_context(context={})
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarization_config])
        .set_fields(fields=[field])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    sdp1 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=[scan_type1])
        .set_processing_blocks(processing_blocks=[pb1])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()


def test_mid_assign_resource_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """

    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.0")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.0")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    request3 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=2)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.0")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    assert request1 == request2
    assert request1 != request3


def test_mid_assign_resources_request():
    """
    Verify creation of Mid AssignResources request objects
    with both sdp & csp blocks and check equality
    """

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
    workflow1 = (
        SDPWorkflowBuilder()
        .set_name(name="vis_receive")
        .set_kind(kind="realtime")
        .set_version(version="0.1.1")
        .build()
    )

    pb1 = (
        ProcessingBlockConfigurationBuilder()
        .set_pb_id(pb_id="pb-mvp01-20200325-00001")
        .set_workflow(workflow=workflow1)
        .set_parameters(parameters={})
        .build()
    )
    dish_allocation = (
        DishAllocateBuilder()
        .set_receptor_ids(receptor_ids=frozenset(["SKA001"]))
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

    phase = (
        PhaseDirBuilder()
        .set_ra(ra=[123, 0.1])
        .set_dec(dec=[123, 0.1])
        .set_reference_time(reference_time="...")
        .set_reference_frame(reference_frame="ICRF3")
        .build()
    )
    field = (
        FieldConfigurationBuilder()
        .set_field_id(field_id="field_a")
        .set_pointing_fqdn(pointing_fqdn="low-tmc/telstate/0/pointing")
        .set_phase_dir(phase_dir=phase)
        .build()
    )

    eb_scan_type = (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id="science")
        .set_beams(beams={"vis0": {"field_id": "field_a"}})
        .set_derive_from(derive_from=".default")
        .build()
    )

    beams = (
        BeamConfigurationBuilder()
        .set_beam_id(beam_id="vis0")
        .set_function(function="visibilities")
        .build()
    )

    channels = (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id="vis_channels")
        .set_spectral_windows(spectral_windows=[channel1])
        .build()
    )

    polarization_config = (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id="all")
        .set_corr_type(corr_type=["XX", "XY", "YY", "YX"])
        .build()
    )

    execution_block = (
        ExecutionBlockConfigurationBuilder()
        .set_eb_id(eb_id="eb-mvp01-20200325-00001")
        .set_context(context={})
        .set_max_length(max_length=3600)
        .set_beams(beams=[beams])
        .set_channels(channels=[channels])
        .set_polarisations(polarisations=[polarization_config])
        .set_fields(fields=[field])
        .set_scan_types(scan_types=[eb_scan_type])
        .build()
    )

    sdp1 = (
        SDPConfigurationBuilder()
        .set_eb_id(eb_id="sbi-mvp01-20200325-00001")
        .set_max_length(max_length=100.0)
        .set_scan_types(scan_types=[scan_type1])
        .set_processing_blocks(processing_blocks=[pb1])
        .set_execution_block(execution_block=execution_block)
        .build()
    )

    request1 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )
    request2 = (
        AssignResourcesRequestBuilder()
        .set_subarray_id(subarray_id=1)
        .set_dish_allocation(dish_allocation=dish_allocation)
        .set_sdp_config(sdp_config=sdp1)
        .set_interface(interface="https://schema.skao.int/ska-tmc-assignresources/2.1")
        .set_transaction_id(transaction_id="txn-mvp01-20200325-00001")
        .build()
    )

    assert request1 == request2
    assert request1 != 1 and request2 != object()
