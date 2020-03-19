"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List, Optional

__all__ = ['AssignResourcesRequest', 'AssignResourcesResponse', 'DishAllocation']


class DishAllocation:
    """
    DishAllocation represents the DISH allocation part of an
    AssignResources request and response.
    """

    def __init__(self, receptor_ids: Optional[List[str]] = None):
        """
        Create a new DishAllocation for the specified receptors.

        :param receptor_ids: (optional) IDs of the receptors to add to this
            allocation
        """
        if receptor_ids is None:
            receptor_ids = []
        self.receptor_ids = list(receptor_ids)

    def __eq__(self, other):
        if not isinstance(other, DishAllocation):
            return False
        return set(self.receptor_ids) == set(other.receptor_ids)

    def __repr__(self):
        return '<DishAllocation(receptor_ids={!r})>'.format(self.receptor_ids)


class AssignResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    AssignResourcesRequest is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest request.
    """

    def __init__(self, subarray_id: int, dish_allocation: DishAllocation):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param dish_allocation: object holding the DISH resource allocation
            for this request.
        """
        self.subarray_id = subarray_id
        self.dish = dish_allocation

    def __eq__(self, other):
        if not isinstance(other, AssignResourcesRequest):
            return False
        return self.subarray_id == other.subarray_id and self.dish == other.dish


class AssignResourcesResponse:  # pylint: disable=too-few-public-methods
    """
    AssignResourcesResponse is a Python representation of the structured
    response from a TMC CentralNode.AssignResources request.
    """

    def __init__(self, dish_allocation: DishAllocation):
        """
        Create a new AssignResourcesRequest response object.

        :param dish_allocation: a DishAllocation corresponding to the
            successfully allocated dishes
        """
        self.dish = dish_allocation

    def __eq__(self, other):
        if not isinstance(other, AssignResourcesResponse):
            return False
        return self.dish == other.dish
