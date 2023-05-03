from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest

from .csp import CSPConfigurationBuilder
from .mccs import MCCSAllocateBuilder
from .sdp import SDPConfigurationBuilder

_all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    """
    AssignResourcesRequestBuilder is a test data builder for CDM AssignResourcesRequest objects.

    By default, AssignResourcesRequestBuilder will build an AssignResourcesRequest

    for low observation command.
    """

    def __init__(self):
        self.subarry_id = None
        self.dish_allocation = None
        self.sdp_config = None
        self.csp_config = None
        self.mccs = None
        self.interface = None
        self.transaction_id = None

    def set_subarray_id(self, subarray_id: int) -> "AssignResourcesRequestBuilder":
        self.subarray_id = subarray_id
        return self

    def set_dish_allocation(
        self, dish_allocation: object
    ) -> "AssignResourcesRequestBuilder":
        self.dish_allocation = dish_allocation
        return self

    def set_sdp_config(
        self, sdp_config: SDPConfigurationBuilder
    ) -> "AssignResourcesRequestBuilder":
        self.sdp_config = sdp_config
        return self

    def set_csp_config(
        self, csp_config: CSPConfigurationBuilder
    ) -> "AssignResourcesRequestBuilder":
        self.csp_config = csp_config
        return self

    def set_mccs(self, mccs: MCCSAllocateBuilder) -> "AssignResourcesRequestBuilder":
        self.mccs = mccs
        return self

    def set_interface(self, interface: str) -> "AssignResourcesRequestBuilder":
        self.interface = interface
        return self

    def set_transaction_id(
        self, transaction_id: str
    ) -> "AssignResourcesRequestBuilder":
        self.transaction_id = transaction_id
        return self

    def build(self) -> AssignResourcesRequest:
        return AssignResourcesRequest(
            self.subarray_id,
            self.dish_allocation,
            self.sdp_config,
            self.csp_config,
            self.mccs,
            self.interface,
            self.transaction_id,
        )
