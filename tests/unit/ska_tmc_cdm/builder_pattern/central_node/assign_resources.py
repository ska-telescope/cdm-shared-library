"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""

from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest

_all__ = ["AssignResourcesRequestBuilder"]


class AssignResourcesRequestBuilder:
    def __init__(self, assign=AssignResourcesRequest()):
        self.assign = assign

    def setsubarray_id(self, subarray_id):
        self.assign.subarray_id = subarray_id
        return self

    def setdish(self, dish):
        self.assign.dish = dish
        return self

    def setsdp_config(self, sdp_config):
        self.assign.sdp_config = sdp_config
        return self

    def setcsp_config(self, csp_config):
        self.assign.csp_config = csp_config
        return self

    def setmccs(self, mccs):
        self.assign.mccs = mccs
        return self

    def setinterface(self, interface):
        self.assign.interface = interface
        return self

    def settransaction_id(self, transaction_id):
        self.assign.transaction_id = transaction_id
        return self

    def build(self):
        return self.assign
