from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import SDPConfiguration

__all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    """
    AssignResourcesRequestBuilder is a test data builder for CDM AssignResourcesRequest objects.

    By default, AssignResourcesRequestBuilder will build an AssignResourcesRequest

    for low observation command.
    """

    def __init__(self):
        self.subarray_id = None
        self.dish_allocation = None
        self.sdp_config = None
        self.mccs = None
        self.interface = None
        self.transaction_id = None

    def set_subarray_id(
        self, subarray_id: int
    ) -> "AssignResourcesRequestBuilder":
        """
        Set subarray id
        :param: subarray_id: Subarray ID
        """
        self.subarray_id = subarray_id
        return self

    def set_dish_allocation(
        self, dish_allocation: DishAllocation
    ) -> "AssignResourcesRequestBuilder":
        """
        Set dish allocation
        :param: dish_allocation: Dish Allocation instance
        """
        self.dish_allocation = dish_allocation
        return self

    def set_sdp_config(
        self, sdp_config: SDPConfiguration
    ) -> "AssignResourcesRequestBuilder":
        """
        Set Configuration for SDP
        :param: sdp_config: SDP Configuration instance
        """
        self.sdp_config = sdp_config
        return self

    def set_mccs(self, mccs: MCCSAllocate) -> "AssignResourcesRequestBuilder":
        """
        Set mccs configuration
        :param: mccs: MCCS Allocation instance
        """
        self.mccs = mccs
        return self

    def set_interface(self, interface: str) -> "AssignResourcesRequestBuilder":
        """
        Set interface version
        :param: interface: Interface version
        """
        self.interface = interface
        return self

    def set_transaction_id(
        self, transaction_id: str
    ) -> "AssignResourcesRequestBuilder":
        """
        Set transaction ID
        :param: transaction_id: Transaction ID
        """
        self.transaction_id = transaction_id
        return self

    @classmethod
    def from_dish(
        cls,
        subarray_id: int,
        dish_allocation: DishAllocation,
        sdp_config: SDPConfiguration = None,
        interface: str = None,
        transaction_id: str = None,
    ) -> "AssignResourcesRequestBuilder":
        """
        Initialize the builder for Mid Assign Resource request
        :param subarray_id: the numeric SubArray ID (1..16)
        :param dish_allocation: object holding the DISH resource allocation for this request.
        :param sdp_config: sdp configuration
        :param interface: Mid Assign Resource Interface version
        :param: transaction_id: Transaction ID

        """
        builder = cls()
        builder.subarray_id = subarray_id
        builder.dish_allocation = dish_allocation
        builder.sdp_config = sdp_config
        builder.interface = interface
        builder.transaction_id = transaction_id
        return builder

    @classmethod
    def from_mccs(
        cls,
        subarray_id: int,
        mccs: MCCSAllocate,
        sdp_config: SDPConfiguration = None,
        interface: str = None,
        transaction_id: str = None,
    ) -> "AssignResourcesRequestBuilder":
        """
        Initialize the builder for Low Assign Resource request
        :param subarray_id: the numeric SubArray ID (1..16)
        :param mccs: MCCS subarray allocation
        :param sdp_config: SDP configuration
        :param interface: url string to determine JsonSchema version
        :param: transaction_id: Transaction ID

        """
        builder = cls()
        builder.subarray_id = subarray_id
        builder.mccs = mccs
        builder.sdp_config = sdp_config
        builder.interface = interface
        builder.transaction_id = transaction_id
        return builder

    def build(self) -> AssignResourcesRequest:
        """
        Builds or creates instance of CDM Assign Resource Request
        """
        return AssignResourcesRequest(
            self.subarray_id,
            self.dish_allocation,
            self.sdp_config,
            self.mccs,
            self.interface,
            self.transaction_id,
        )


class AssignResourcesResponseBuilder:
    """
    AssignResourcesResponseBuilder is a test data builder for CDM AssignResourcesResponse objects.
    """

    def __init__(self):
        self.dish_allocation = None

    def set_dish(
        self, dish_allocation: DishAllocation
    ) -> "AssignResourcesResponseBuilder":
        """
        Set dish allocation
        :param: dish: Dish Allocation instance
        """
        self.dish_allocation = dish_allocation
        return self

    def build(self) -> AssignResourcesResponse:
        """
        Builds or creates instance of CDM Assign Resource Response
        """
        return AssignResourcesResponse(dish_allocation=self.dish_allocation)
