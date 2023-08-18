"""
The release_resources module provides simple Python representations of the
structured request and response for a TMC CentralNode.ReleaseResources call.
"""
from typing import Optional

from pydantic import Field, StrictBool, model_validator
from pydantic.dataclasses import dataclass

from .common import DishAllocation

__all__ = ["ReleaseResourcesRequest"]


@dataclass
class ReleaseResourcesRequest:
    """
    ReleaseResourcesRequest is a Python representation of the structured
    request for a TMC CentralNode.ReleaseResources call.

    :param interface: url string to determine JsonSchema version
    :param transaction_id: ID for tracking requests
    :param subarray_id: the numeric SubArray ID (1..16)
    :param release_all: True to release all sub-array resources, False to
    release just those resources specified as other arguments
    :param dish_allocation: object holding the DISH resource allocation
    to release for this request.
    """

    interface: str = None
    transaction_id: str = None
    subarray_id: int = None
    release_all: StrictBool = False
    dish: Optional[DishAllocation] = Field(default=None, alias="dish_allocation")

    @model_validator(mode="after")
    def validate_release_all_ignores_dish_allocation(self) -> "ReleaseResourcesRequest":
        if self.release_all is False and self.dish is None:
            raise ValueError("Either release_all or dish_allocation must be defined")
        if self.release_all:
            self.dish = None
        return self
