"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
import json

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
        *_,
        interface: str = None,
        transaction_id: str = None,
        subarray_id: int = None,
        release_all: bool = False,
        dish_allocation: Optional[DishAllocation] = None,
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
        """
        if release_all is not None and not isinstance(release_all, bool):
            raise ValueError("release_all_mid must be a boolean")

        if release_all is False and dish_allocation is None:
            raise ValueError("Either release_all or dish_allocation must be defined")
        if release_all:
            dish_allocation = None
        # existing keys
        self.interface = interface
        self.transaction_id = transaction_id
        self.subarray_id = subarray_id
        self.release_all = release_all
        self.dish_allocation = dish_allocation

    # a class method to initialize the default constructor then update key-value pairs 
    @classmethod
    def from_any_schema_keyvalue(cls,json_keyValuePair='{}',**kwargs):
        """Two ways of initializing object with keyword-values
        1. json_keyValuePair (recommended) : json input key-value pair or,
        2. keyword1=value1, keyword2=value2 ...
        """
        self=cls(release_all=None) 
        # Should init as cls() but here to avoid any thrown value error ...
        # for either release_all or dish_allocation. 
        # Correct values are anyway updated in next lines.
        self.__dict__.update(kwargs)
        self.__dict__.update(json.loads(json_keyValuePair))
        # check the value errors same as constructor
        if self.release_all is not None and not isinstance(self.release_all, bool):
            raise ValueError("release_all_mid must be a boolean")
        if self.release_all is False and self.dish_allocation is None:
            raise ValueError("Either release_all or dish_allocation must be defined")
        #if no value error occur then only return the object
        return self

    def __eq__(self, other):
        if not isinstance(other, ReleaseResourcesRequest):
            return False
        return (
            self.interface == other.interface
            and self.transaction_id == other.transaction_id
            and self.subarray_id == other.subarray_id
            and self.dish_allocation == other.dish_allocation
            and self.release_all == other.release_all
        )