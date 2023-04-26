from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest

_all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    """
    AssignResourcesRequestBuilder is a test data builder for CDM AssignResourcesRequest objects.

    By default, AssignResourcesRequestBuilder will build an AssignResourcesRequest

    for low observation command.
    """

    def __init__(self, assign=AssignResourcesRequest()) -> object:
        self.assign = assign

    def set_subarray_id(self, subarray_id):
        self.assign.subarray_id = subarray_id
        return self

    def set_dish(self, dish):
        self.assign.dish = dish
        return self

    def set_sdp_config(self, sdp_config):
        self.assign.sdp_config = sdp_config
        return self

    def set_csp_config(self, csp_config):
        self.assign.csp_config = csp_config
        return self

    def set_mccs(self, mccs):
        self.assign.mccs = mccs
        return self

    def set_interface(self, interface):
        self.assign.interface = interface
        return self

    def set_transaction_id(self, transaction_id):
        self.assign.transaction_id = transaction_id
        return self

    def build(self):
        return self.assign
