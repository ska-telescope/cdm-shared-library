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
from tests.unit.ska_tmc_cdm.builder.central_node.assign_resources import (
    AssignResourcesRequestBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.csp import (
    CommonConfigurationBuilder,
    CSPConfigurationBuilder,
    LowCbfConfigurationBuilder,
    ResourceConfigurationBuilder,
)
from tests.unit.ska_tmc_cdm.builder.central_node.mccs import MCCSAllocateBuilder
from tests.unit.ska_tmc_cdm.builder.central_node.sdp import (
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


def csp_configuration(interface=None, common=None, lowcbf=None):
    return (
        CSPConfigurationBuilder()
        .set_interface(interface=interface)
        .set_common(common=common)
        .set_lowcbf(lowcbf=lowcbf)
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


def common_configuration(subarray_id=None):
    return CommonConfigurationBuilder().set_subarray_id(subarray_id=subarray_id).build()


def lowcbf_configuration(resources=None):
    return LowCbfConfigurationBuilder().set_resources(resources=resources).build()


def resource_configuration(device=None, shared=None, fw_image=None, fw_mode=None):
    return (
        ResourceConfigurationBuilder()
        .set_device(device=device)
        .set_shared(shared=shared)
        .set_fw_image(fw_image=fw_image)
        .set_fw_mode(fw_mode=fw_mode)
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


def eb_scan(scan_type_id=None, beams=None, derive_from=None):
    return (
        EBScanTypeBuilder()
        .set_scan_type_id(scan_type_id=scan_type_id)
        .set_beams(beams=beams)
        .set_derive_from(derive_from=derive_from)
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


def phase_d(ra=None, dec=None, reference_time=None, reference_frame=None):
    return (
        PhaseDirBuilder()
        .set_ra(ra=ra)
        .set_dec(dec=dec)
        .set_reference_time(reference_time=reference_time)
        .set_reference_frame(reference_frame=reference_frame)
        .build()
    )


def mccs_allocate_conf(subarray_beam_ids=None, station_ids=None, channel_blocks=None):
    return (
        MCCSAllocateBuilder()
        .set_subarray_beam_ids(subarray_beam_ids=subarray_beam_ids)
        .set_station_ids(station_ids=station_ids)
        .set_channel_blocks(channel_blocks=channel_blocks)
        .build()
    )


def channel_configuration(
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


def polarization(polarisations_id=None, corr_type=None):
    return (
        PolarisationConfigurationBuilder()
        .set_polarisations_id(polarisations_id=polarisations_id)
        .set_corr_type(corr_type=corr_type)
        .build()
    )


def channel_configure(channels_id=None, spectral_windows=None):
    return (
        ChannelConfigurationBuilder()
        .set_channels_id(channels_id=channels_id)
        .set_spectral_windows(spectral_windows=[spectral_windows])
        .build()
    )


def scan_type_conf(
    scan_type_id=None, reference_frame=None, ra=None, dec=None, channel=None
):
    return (
        ScanTypeBuilder()
        .set_scan_type_id(scan_type_id=scan_type_id)
        .set_reference_frame(reference_frame=reference_frame)
        .set_ra(ra=ra)
        .set_dec(dec=dec)
        .set_channels(channels=channel)
        .build()
    )


def workflow_conf(name=None, kind=None, version=None):
    return (
        SDPWorkflowBuilder()
        .set_name(name=name)
        .set_kind(kind=kind)
        .set_version(version=version)
        .build()
    )


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


def assign_request(
    subarray_id=None,
    dish_allocation=None,
    sdp_config=None,
    interface=None,
    transaction_id=None,
    mccs=None,
    csp=None,
):
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


def beam_configuration(
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


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel1 = channel_configuration(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type_conf(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    workflow1 = workflow_conf(name="vis_receive", kind="realtime", version="0.1.1")
    pb1 = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=None,
    )
    sdp1 = sdp(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=scan_type1,
        processing_blocks=pb1,
    )

    request1 = assign_request(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = assign_request(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-tmc-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request3 = assign_request(
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
    mccs1 = mccs_allocate_conf(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request(subarray_id=1, mccs=mccs1)
    request2 = assign_request(subarray_id=1, mccs=mccs1)
    assert request1 == request2
    assert request1 != AssignResourcesRequest(subarray_id=2, mccs=mccs1)


def test_assign_resources_request_from_mccs():
    """
    Verify that two AssignResource request objects for the same sub-array and
    mccs allocation are considered equal.
    """
    mccs_allocate = MCCSAllocate(
        list(zip(itertools.count(1, 1), 1 * [2])), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]
    )
    request = AssignResourcesRequest.from_mccs(subarray_id=1, mccs=mccs_allocate)

    expected = AssignResourcesRequest(
        subarray_id=1,
        mccs=MCCSAllocate(
            list(zip(itertools.count(1, 1), 1 * [2])),
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 6],
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
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
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
    mccs = mccs_allocate_conf(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request(subarray_id=1, mccs=mccs)
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
    mccs1 = mccs_allocate_conf(
        subarray_beam_ids=[1], station_ids=[[1, 2]], channel_blocks=[3]
    )
    request1 = assign_request(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request2 = assign_request(
        subarray_id=1,
        mccs=mccs1,
        interface="https://schema.skao.int/" "ska-low-tmc-assignresources/2.0",
    )
    request3 = assign_request(
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
        list(zip(itertools.count(1, 1), 1 * [2])),
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
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
    channel = channel_configuration(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )

    scan_type = eb_scan(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    pb_config = processing_block(
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
    beams = beam_configuration(beam_id="vis0", function="visibilities")
    channels = channel_configure(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = phase_d(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = execution(
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
    sdp_config = sdp(
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
    channel = channel_configuration(
        spectral_window_id="fsp_2_channels",
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=0.368e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
    )
    scan_type = eb_scan(
        scan_type_id="science",
        beams={"vis0": {"field_id": "field_a"}},
        derive_from=".default",
    )
    sbi_ids = "sbi-mvp01-20200325-00001"
    script = scripts(kind="realtime", name="test-receive-addresses", version="0.5.0")
    pb_config = processing_block(
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
    beams = beam_configuration(
        beam_id="pss1", search_beam_id=1, function="pulsar search"
    )
    channels = channel_configure(
        channels_id="vis_channels",
        spectral_windows=[channel],
    )
    polarisation = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase_dir = phase_d(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    fields = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase_dir,
    )

    execution_block = execution(
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
    sdp_config = sdp(
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
    channel1 = channel_configuration(
        count=744,
        start=0,
        stride=2,
        freq_min=0.35e9,
        freq_max=1.05e9,
        link_map=[[0, 0], [200, 1], [744, 2], [944, 3]],
        spectral_window_id="fsp_2_channels",
    )
    scan_type1 = scan_type_conf(
        scan_type_id="science_A",
        reference_frame="ICRS",
        ra="02:42:40.771",
        dec="-00:00:47.84",
        channel=[channel1],
    )
    workflow1 = workflow_conf(name="vis_receive", kind="realtime", version="0.1.1")
    pb1 = processing_block(
        pb_id="pb-mvp01-20200325-00001",
        workflow=workflow1,
        parameters={},
        dependencies=None,
    )
    beams = beam_configuration(beam_id="vis0", function="visibilities")
    channels = channel_configure(
        channels_id="vis_channels", spectral_windows=[channel1]
    )
    polarization_config = polarization(
        polarisations_id="all", corr_type=["XX", "XY", "YY", "YX"]
    )
    phase = phase_d(
        ra=[123, 0.1], dec=[123, 0.1], reference_time="...", reference_frame="ICRF3"
    )
    field = fields_configuration(
        field_id="field_a",
        pointing_fqdn="low-tmc/telstate/0/pointing",
        phase_dir=phase,
    )
    execution_block = execution(
        eb_id="eb-test-20220916-00000",
        context={},
        max_length=3600,
        beams=[beams],
        channels=[channels],
        polarisations=[polarization_config],
        fields=[field],
        scan_types=[scan_type1],
    )
    sdp1 = sdp(
        eb_id="sbi-mvp01-20200325-00001",
        max_length=100.0,
        scan_types=scan_type1,
        processing_blocks=pb1,
        execution_block=execution_block,
    )

    request1 = assign_request(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )

    request2 = assign_request(
        subarray_id=1,
        dish_allocation=None,
        sdp_config=sdp1,
        interface="https://schema.skao.int/ska-low-csp-assignresources/2.0",
        transaction_id="txn-mvp01-20200325-00001",
    )
    assert request1 == request2
    assert request1 != 1 and request2 != object()
