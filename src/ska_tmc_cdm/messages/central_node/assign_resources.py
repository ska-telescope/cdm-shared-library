"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from pydantic import model_validator

from .common import DishAllocation
from .csp import CSPConfiguration
from .mccs import MCCSAllocate
from .sdp import SDPConfiguration

__all__ = ["AssignResourcesRequest", "AssignResourcesResponse"]


class AssignResourcesRequest(BaseModel):
    """
    AssignResourcesRequest is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest request.

    :param subarray_id: the numeric SubArray ID (1..16)
    :param dish_allocation: object holding the DISH resource allocation
        for this request.
    :param sdp_config: sdp configuration
    :param csp_config: csp configuration
    :param mccs: MCCS subarray allocation
    :param interface: url string to determine JsonSchema version
    :param transaction_id: ID for tracking requests

    :raises ValueError: if mccs is allocated with dish and sdp_config
    """

    subarray_id: Optional[int] = None
    dish: Optional[DishAllocation] = Field(default=None, alias='dish_allocation')
    sdp_config: Optional[SDPConfiguration] = None
    csp_config: Optional[CSPConfiguration] = None
    mccs: Optional[MCCSAllocate] = None
    interface: Optional[str] = None
    transaction_id: Optional[str] = None

    @model_validator(mode="after")
    def validate_exclusive_fields(self) -> "AssignResourcesRequest":
        if self.mccs is not None and self.subarray_id is None:
            raise ValueError("subarray_id must be defined for LOW request")
        if self.dish is not None and self.subarray_id is None:
            raise ValueError("subarray_id must be defined for MID request")
        if self.mccs is not None and self.dish is not None:
            raise ValueError("Can't allocate dish in the same call as mccs")

    @classmethod
    def from_dish(
        cls,
        subarray_id: int,
        dish_allocation: DishAllocation,
        sdp_config: SDPConfiguration = None,
        interface: str = None,
        transaction_id: str = None,
    ):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param dish_allocation: object holding the DISH resource allocation
            for this request.
        :param sdp_config: sdp configuration
        :return: AssignResourcesRequest object
        """
        return cls(**locals())

    @classmethod
    def from_mccs(
        cls,
        subarray_id: int,
        mccs: MCCSAllocate,
        sdp_config: SDPConfiguration = None,
        csp_config: CSPConfiguration = None,
        interface: str = None,
        transaction_id: str = None,
    ):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param mccs: MCCS subarray allocation
        :param sdp_config: SDP configuration
        :param csp_config: CSP configuration
        :param interface: url string to determine JsonSchema version

        :return: AssignResourcesRequest object
        """
        return cls(**locals())


@dataclass
class AssignResourcesResponse:
    """
    AssignResourcesResponse is a Python representation of the structured
    response from a TMC CentralNode.AssignResources request.
    """
    dish: Optional[DishAllocation] = Field(default=None, alias='dish_allocation')