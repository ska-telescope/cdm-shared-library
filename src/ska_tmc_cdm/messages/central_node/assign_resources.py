"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""

from .common import DishAllocation
from .mccs import MCCSAllocate
from .sdp import SDPConfiguration

__all__ = ["AssignResourcesRequest", "AssignResourcesResponse"]


class AssignResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    AssignResourcesRequest is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest request.
    """

    def __init__(
        self,
        subarray_id: int = None,
        dish_allocation: DishAllocation = None,
        sdp_config: SDPConfiguration = None,
        mccs: MCCSAllocate = None,
        interface: str = None,
        transaction_id: str = None,
    ):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param dish_allocation: object holding the DISH resource allocation
            for this request.
        :param sdp_config: sdp configuration
        :param mccs: MCCS subarray allocation
        :param interface: url string to determine JsonSchema version
        :param transaction_id: ID for tracking requests

        :raises ValueError: if mccs is allocated with dish and sdp_config
        """
        self.subarray_id = subarray_id
        self.dish = dish_allocation
        self.sdp_config = sdp_config
        self.mccs = mccs
        self.interface = interface
        self.transaction_id = transaction_id

        if self.mccs is not None and self.subarray_id is None:
            raise ValueError("subarray_id must be " "defined for LOW request")
        if self.dish is not None and self.subarray_id is None:
            raise ValueError("subarray_id must be " "defined for MID request")
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
        obj = cls.__new__(cls)
        obj.__init__(
            subarray_id,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            interface=interface,
            transaction_id=transaction_id,
        )
        return obj

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

    def __eq__(self, other):
        if not isinstance(other, AssignResourcesRequest):
            return False
        return (
            self.subarray_id == other.subarray_id
            and self.dish == other.dish
            and self.sdp_config == other.sdp_config
            and self.mccs == other.mccs
            and self.interface == other.interface
            and self.transaction_id == other.transaction_id
        )


class AssignResourcesResponse:  # pylint: disable=too-few-public-methods
    """
    AssignResourcesResponse is a Python representation of the structured
    response from a TMC CentralNode.AssignResources request.
    """

    def __init__(self, dish_allocation: DishAllocation = None):
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
