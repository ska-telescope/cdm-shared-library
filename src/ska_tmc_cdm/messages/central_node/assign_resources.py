"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional

from pydantic import Field, model_validator

from ska_tmc_cdm.messages.base import CdmObject

from .common import DishAllocation
from .mccs import MCCSAllocate
from .sdp import SDPConfiguration

__all__ = ["AssignResourcesRequest", "AssignResourcesResponse"]

MID_SCHEMA = "https://schema.skao.int/ska-tmc-assignresources/2.1"
LOW_SCHEMA = "https://schema.skao.int/ska-low-tmc-assignresources/3.2"


class AssignResourcesRequest(CdmObject):
    """
    AssignResourcesRequest is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest request.

    :param subarray_id: the numeric SubArray ID (1..16)
    :param dish_allocation: object holding the DISH resource allocation
        for this request.
    :param sdp_config: sdp configuration
    :param mccs: MCCS subarray allocation
    :param interface: url string to determine JsonSchema version, defaults to
        https://schema.skao.int/ska-tmc-assignresources/2.1 for Mid and
        https://schema.skao.int/ska-low-tmc-assignresources/3.2 for Low if not set
    :param transaction_id: ID for tracking requests

    :raises ValueError: if mccs is allocated with dish and sdp_config
    """

    subarray_id: Optional[int] = None
    dish: Optional[DishAllocation] = None
    sdp_config: Optional[SDPConfiguration] = None
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
        if self.mccs is None and self.dish is None and self.interface is None:
            raise ValueError("mccs, dish or interface kwarg must be set")
        return self

    @model_validator(mode="after")
    def set_default_schema(self) -> "AssignResourcesRequest":
        if self.interface is None:
            if self.mccs is not None:
                self.interface = LOW_SCHEMA
            else:
                self.interface = MID_SCHEMA
        return self

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
        return cls(
            subarray_id=subarray_id,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            interface=interface,
            transaction_id=transaction_id,
        )

    @classmethod
    def from_mccs(
        cls,
        subarray_id: int,
        mccs: MCCSAllocate,
        sdp_config: SDPConfiguration = None,
        interface: str = None,
        transaction_id: str = None,
    ):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param mccs: MCCS subarray allocation
        :param sdp_config: SDP configuration
        :param interface: url string to determine JsonSchema version

        :return: AssignResourcesRequest object
        """
        return cls(
            subarray_id=subarray_id,
            mccs=mccs,
            sdp_config=sdp_config,
            interface=interface,
            transaction_id=transaction_id,
        )


class AssignResourcesResponse(CdmObject):
    """
    AssignResourcesResponse is a Python representation of the structured
    response from a TMC CentralNode.AssignResources request.
    """

    dish: Optional[DishAllocation] = Field(default=None, alias="dish_allocation")
