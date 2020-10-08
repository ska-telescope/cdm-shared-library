"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
from typing import Optional

from .csp import DishAllocation

__all__ = ['ReleaseResourcesRequest']


class ReleaseResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    ReleaseResourcesRequest is a Python representation of the structured
    request for a TMC CentralNode.ReleaseResources call.
    """

    def __init__(self, subarray_id: int, release_all: bool = False,
                 dish_allocation: Optional[DishAllocation] = None):
        """
        Create a new ReleaseResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param release_all: True to release all sub-array resources, False to
            release just those resources specified as other arguments
        :param dish_allocation: object holding the DISH resource allocation
            to release for this request.
        """
        if not isinstance(release_all, bool):
            raise ValueError('release_all must be a boolean')
        if release_all is False and dish_allocation is None:
            raise ValueError('Either release_all or dish_allocation must be defined')
        if release_all:
            dish_allocation = None

        self.subarray_id = subarray_id
        self.dish = dish_allocation
        self.release_all = release_all

    def __eq__(self, other):
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return all([self.subarray_id == other.subarray_id,
                    self.dish == other.dish,
                    self.release_all == other.release_all])
