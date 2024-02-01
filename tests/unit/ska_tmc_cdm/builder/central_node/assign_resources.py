from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska_tmc_cdm.messages.central_node.common import DishAllocation
from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate
from ska_tmc_cdm.messages.central_node.sdp import SDPConfiguration

_all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    """
    AssignResourcesRequestBuilder is a test data builder for CDM AssignResourcesRequest objects.

    By default, AssignResourcesRequestBuilder will build an AssignResourcesRequest

    for low observation command.
    """

    def __init__(self):
        """
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
        self.subarray_id = None
        self.dish_allocation = None
        self.sdp_config = None
        self.mccs = None
        self.interface = None
        self.transaction_id = None

    def set_subarray_id(self, subarray_id: int) -> "AssignResourcesRequestBuilder":
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
