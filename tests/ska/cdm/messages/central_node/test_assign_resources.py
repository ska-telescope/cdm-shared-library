"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.assign_resources import AssignResourcesResponse
from ska.cdm.messages.central_node.common import DishAllocation
from ska.cdm.messages.central_node.sdp import (
    SDPWorkflow,
    SDPConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    Channel,
)
from ska.cdm.messages.central_node.mccs import MCCSAllocate


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    channel = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [[0, 0], [200, 1], [744, 2], [944, 3]]
    )
    scan_type = ScanType("science_A", "ICRS", "02:42:40.771", "-00:00:47.84", [channel])
    sdp_workflow = SDPWorkflow(
        workflow_id="vis_receive", workflow_type="realtime", version="0.1.0"
    )
    pb_config = ProcessingBlockConfiguration(
        "pb-mvp01-20200325-00001", sdp_workflow, {}
    )
    sdp_config = SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, [scan_type], [pb_config]
    )
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    request = AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=sdp_config
    )

    assert request == AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=sdp_config
    )

    assert request != AssignResourcesRequest(
        1, dish_allocation=dish_allocation, sdp_config=None
    )
    assert request != AssignResourcesRequest(1, dish_allocation=None, sdp_config=None)
    assert request != AssignResourcesRequest(
        1, dish_allocation=None, sdp_config=sdp_config
    )

    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    request = AssignResourcesRequest(1, mccs_allocate=mccs_allocate)
    assert request == AssignResourcesRequest(1, mccs_allocate=mccs_allocate)
    assert request != AssignResourcesRequest(2, mccs_allocate=mccs_allocate)
    assert request != AssignResourcesRequest(
        1,
        mccs_allocate=MCCSAllocate(
            2, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ),
    )
    assert request != AssignResourcesRequest(
        1,
        mccs_allocate=MCCSAllocate(
            1, [3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ),
    )
    assert request != AssignResourcesRequest(
        1, mccs_allocate=MCCSAllocate(1, [1, 2, 3, 4], [3, 4, 5], [1, 2, 3, 4, 5, 6])
    )
    assert request != AssignResourcesRequest(
        1,
        mccs_allocate=MCCSAllocate(
            1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]
        ),
    )


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

    mccs_allocate = MCCSAllocate(
        1, [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    request = AssignResourcesRequest(1, mccs_allocate=mccs_allocate)
    assert request != 1
    assert request != object()


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
