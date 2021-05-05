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
            interface: str = None,
            subarray_id_low: int = None,
            subarray_id_mid: int = None,
            release_all_low: bool = False,
            release_all_mid: bool = False,
            dish_allocation: Optional[DishAllocation] = None
    ):
        """
        Create a new ReleaseResourcesRequest object.

        :param interface: url string to determine JsonSchema version
        :param subarray_id_low: the numeric SubArray ID (1..16) for LOW
        :param subarray_id_mid: the numeric SubArray ID (1..16) for MID
        :param release_all_mid: True to release all sub-array resources, False to
            release just those resources specified as other arguments for MID
        :param release_all_low: True to release all sub-array resources for LOW
        :param dish_allocation: object holding the DISH resource allocation
            to release for this request.
        """

        if not isinstance(release_all_mid, bool):
            raise ValueError('release_all_mid must be a boolean')

        if not isinstance(release_all_low, bool):
            raise ValueError('release_all_low must be a boolean')

        if (release_all_mid is False and dish_allocation is None) and \
                (release_all_low is False):
            raise ValueError('Either release_all_mid or dish_allocation must be '
                             'defined for MID or release_all_low must be '
                             'defined for LOW request')
        if release_all_mid:
            dish_allocation = None

        self.interface = interface
        self.subarray_id_low = subarray_id_low
        self.subarray_id_mid = subarray_id_mid
        self.release_all_low = release_all_low
        self.release_all_mid = release_all_mid
        self.dish = dish_allocation

    def __eq__(self, other):
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return self.interface == other.interface and \
               self.subarray_id_low == other.subarray_id_low and \
               self.subarray_id_mid == other.subarray_id_mid and \
               self.dish == other.dish and \
               self.release_all_low == other.release_all_low and \
               self.release_all_mid == other.release_all_mid
