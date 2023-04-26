from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest

_all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    """
    AssignResourcesRequestBuilder is a test data builder for CDM AssignResourcesRequest objects.

    By default, AssignResourcesRequestBuilder will build an AssignResourcesRequest

    for low observation command.
    """

    def __init__(self) -> object:
        self.assign = None

    def set_subarray_id(self, subarray_id):
        self.subarray_id = subarray_id
        return self

    def set_dish_allocation(self, dish_allocation):
        self.dish_allocation = dish_allocation
        return self

    def set_sdp_config(self, sdp_config):
        self.sdp_config = sdp_config
        return self

    def set_csp_config(self, csp_config):
        self.csp_config = csp_config
        return self

    def set_mccs(self, mccs):
        self.mccs = mccs
        return self

    def set_interface(self, interface):
        self.interface = interface
        return self

    def set_transaction_id(self, transaction_id):
        self.transaction_id = transaction_id
        return self

    def build(self):
        self.assign = AssignResourcesRequest(
            subarray_id=self.subarray_id,
            dish_allocation=self.dish_allocation,
            sdp_config=self.sdp_config,
            csp_config=self.csp_config,
            mccs=self.mccs,
            interface=self.interface,
            transaction_id=self.transaction_id,
        )
        return self.assign
