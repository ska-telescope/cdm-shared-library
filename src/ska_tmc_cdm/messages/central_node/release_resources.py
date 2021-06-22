"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
from typing import Optional

from .common import DishAllocation

__all__ = ['ReleaseResourcesRequest']


class ReleaseResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    ReleaseResourcesRequest is a Python representation of the structured
    request for a TMC CentralNode.ReleaseResources call.
    """

    def __init__(
            self,
            *_,  # force kwargs
            interface: str = None,
            subarray_id: int = None,
            release_all: bool = False,
            dish_allocation: Optional[DishAllocation] = None
    ):
        """
        Create a new ReleaseResourcesRequest object.

        :param interface: url string to determine JsonSchema version
        :param subarray_id: the numeric SubArray ID (1..16)
        :param release_all: True to release all sub-array resources, False to
            release just those resources specified as other arguments
        :param dish_allocation: object holding the DISH resource allocation
            to release for this request.
        """
        if release_all is not None and not isinstance(release_all, bool):
            raise ValueError('release_all_mid must be a boolean')

        if release_all is False and dish_allocation is None:
            raise ValueError(
                'Either release_all or dish_allocation must be defined'
            )
        if release_all:
            dish_allocation = None

        self.interface = interface
        self.subarray_id = subarray_id
        self.release_all = release_all
        self.dish = dish_allocation

    def __eq__(self, other):
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return self.interface == other.interface and \
               self.subarray_id == other.subarray_id and \
               self.dish == other.dish and \
               self.release_all == other.release_all
