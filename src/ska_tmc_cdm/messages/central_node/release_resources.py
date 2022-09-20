"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
from typing import Optional

from .common import DishAllocation

__all__ = ["ReleaseResourcesRequest"]


class ReleaseResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    ReleaseResourcesRequest is a Python representation of the structured
    request for a TMC CentralNode.ReleaseResources call.
    """

    def __init__(
        self,
        *_,  # force non-keyword args
        interface: str = None,
        transaction_id: str = None,
        subarray_id: int = None,
        release_all: bool = False,
        dish_allocation: Optional[DishAllocation] = None,
        sdp_id: str = None,
        sdp_max_length: float = None,
        **kwargs,  # arbitary keyword-value pairs
    ):
        """
        Create a new ReleaseResourcesRequest object.

        :param interface: url string to determine JsonSchema version
        :param transaction_id: ID for tracking requests
        :param subarray_id: the numeric SubArray ID (1..16)
        :param release_all: True to release all sub-array resources, False to
            release just those resources specified as other arguments
        :param dish_allocation: object holding the DISH resource allocation
                                to release for this request.
        # 2 new dummy parameters
        :param sdp_id: string denoting id for science data processor in use.
        :param sdp_max_length: float denoting max length required in seconds.

        :Any other parameter is also captured by kwargs
        """
        # init existing keys
        self.interface = interface
        self.transaction_id = transaction_id
        self.subarray_id = subarray_id
        self.release_all = release_all
        self.dish = dish_allocation
        self.sdp_id = sdp_id
        self.sdp_max_length = sdp_max_length
        # update new keywords-value pairs.
        self.__dict__.update(kwargs)
        # value errors
        if self.release_all is not None and not isinstance(self.release_all, bool):
            raise ValueError("release_all_mid must be a boolean")

        if self.release_all is False and self.dish is None:
            raise ValueError("Either release_all or dish_allocation must be defined")
        if self.release_all is True:
            self.dish = None

    def __eq__(self, other):
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return (
            self.interface == other.interface
            and self.transaction_id == other.transaction_id
            and self.subarray_id == other.subarray_id
            and self.dish == other.dish
            and self.release_all == other.release_all
            and self.sdp_id == other.sdp_id
            and self.sdp_max_length == other.sdp_max_length
        )
