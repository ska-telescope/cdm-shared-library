"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest, \
    AssignResourcesResponse, DishAllocation

from ska.cdm.messages.subarray_node.configure.sdp import NewProcessingBlockConfiguration, SDPWorkflow, NewSDPConfiguration, ScanType, SubBand


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
    sub_bands = SubBand(0.35e9, 1.05e9, 372, [[1,0], [101,1]])
    scan_type_a = ScanType('science_A', coordinate_system= "ICRS", ra= "02:42:40.771", dec= "-00:00:47.84", sub_bands= [sub_bands])
    sdp_workflow = SDPWorkflow("vis_receive", "realtime", "0.1.0")
    pb_a = NewProcessingBlockConfiguration("pb-mvp01-20200325-00001", workflow=sdp_workflow, dependencies=[], parameters=[])
    sdp_config = NewSDPConfiguration(scan_types = [], processing_blocks=[pb_a])
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    request = AssignResourcesRequest(1, dish_allocation=dish_allocation)

    assert request == AssignResourcesRequest(1, dish_allocation=dish_allocation)
    assert request != AssignResourcesRequest(1, dish_allocation=DishAllocation())
    assert request != AssignResourcesRequest(2, dish_allocation=dish_allocation)


def test_assign_resources_request_eq_with_other_objects():
    """
    Verify that an AssignResources request object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    request = AssignResourcesRequest(1, dish_allocation=dish_allocation)
    assert request != 1
    assert request != object()


def test_assign_resources_response_eq():
    """
    Verify that two AssignResource response objects with the same successful
    dish allocation are considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    unequal_allocation = DishAllocation(receptor_ids=['b', 'aab'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)

    assert response == AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != AssignResourcesResponse(dish_allocation=DishAllocation())
    assert response != AssignResourcesResponse(dish_allocation=unequal_allocation)


def test_assign_resources_response_eq_with_other_objects():
    """
    Verify that an AssignResourcesRequest response object is not considered equal to
    objects of other types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    response = AssignResourcesResponse(dish_allocation=dish_allocation)
    assert response != 1
    assert response != object()


def test_dish_allocation_repr():
    """
    Verify that the DishAllocation repr is formatted correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert repr(dish_allocation) == "<DishAllocation(receptor_ids=['ac', 'b', 'aab'])>"


def test_dish_allocation_eq():
    """
    Verify that two DishAllocations with the same allocated receptors are
    considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation == DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation == DishAllocation(receptor_ids=['b', 'ac', 'aab'])
    assert dish_allocation != DishAllocation(receptor_ids=['ac'])
    assert dish_allocation != DishAllocation(receptor_ids=['ac', 'b', 'aab', 'd'])


def test_dish_allocation_eq_with_other_objects():
    """
    Verify that a DishAllocation is considered unequal to objects of other
    types.
    """
    dish_allocation = DishAllocation(receptor_ids=['ac', 'b', 'aab'])
    assert dish_allocation != 1
    assert dish_allocation != object()
