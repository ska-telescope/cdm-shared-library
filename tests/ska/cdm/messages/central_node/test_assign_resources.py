"""
Unit tests for the CentralNode.AssignResources request/response mapper module.
"""
from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest, \
    AssignResourcesResponse, DishAllocation


def test_assign_resources_request_eq():
    """
    Verify that two AssignResource request objects for the same sub-array and
    dish allocation are considered equal.
    """
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
