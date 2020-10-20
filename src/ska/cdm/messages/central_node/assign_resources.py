"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""

from .mccs import MCCSAllocate
from .sdp import SDPConfiguration
from .common import DishAllocation

__all__ = ["AssignResourcesRequest", "AssignResourcesResponse"]


class AssignResourcesRequest:  # pylint: disable=too-few-public-methods
    """
    AssignResourcesRequest is a Python representation of the structured
    argument for a TMC CentralNode.AssignResourcesRequest request.
    """

    def __init__(
        self,
        subarray_id: int,
        dish_allocation: DishAllocation = None,
        sdp_config: SDPConfiguration = None,
        mccs_allocate: MCCSAllocate = None,
    ):
        """
        Create a new AssignResourcesRequest object.

        :param subarray_id: the numeric SubArray ID (1..16)
        :param dish_allocation: object holding the DISH resource allocation
            for this request.
        :param sdp_config: sdp configuration
        :param mccs_allocate: MCCS subarray allocation
        """
        self.subarray_id = subarray_id
        self.dish = dish_allocation
        self.sdp_config = sdp_config
        self.mccs = mccs_allocate

    def __eq__(self, other):
        if not isinstance(other, AssignResourcesRequest):
            return False
        return (
            self.subarray_id == other.subarray_id
            and self.dish == other.dish
            and self.sdp_config == other.sdp_config
            and self.mccs == other.mccs
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
