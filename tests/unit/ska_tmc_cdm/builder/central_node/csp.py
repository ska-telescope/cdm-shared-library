from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourceConfiguration,
)

"""
Create a csp block using builder pattern
"""


class CommonConfigurationBuilder:
    def __init__(self, common=CommonConfiguration()):
        self.common = common

    def set_subarray_id(self, subarray_id):
        self.common.subarray_id = subarray_id
        return self

    def build(self):
        return self.common


class ResourceConfigurationBuilder:
    def __init__(self, resource=ResourceConfiguration()):
        self.resource = resource

    def set_device(self, device):
        self.resource.device = device
        return self

    def set_shared(self, shared):
        self.resource.shared = shared
        return self

    def set_fw_image(self, fw_image):
        self.resource.fw_image = fw_image
        return self

    def set_fw_mode(self, fw_mode):
        self.resource.fw_mode = fw_mode
        return self

    def build(self):
        return self.resource


class LowCbfConfigurationBuilder:
    def __init__(self, lowcbf=LowCbfConfiguration(resources=[ResourceConfiguration])):
        self.lowcbf = lowcbf

    def set_resources(self, resources):
        self.lowcbf.resources = resources
        return self

    def build(self):
        return self.lowcbf


class CSPConfigurationBuilder:
    def __init__(
        self,
        csp=CSPConfiguration(
            interface=str, common=CommonConfiguration, lowcbf=LowCbfConfiguration
        ),
    ):
        self.csp = csp

    def set_interface(self, interface):
        self.csp.interface = interface
        return self

    def set_common(self, common):
        self.csp.common = common
        return self

    def set_lowcbf(self, lowcbf):
        self.csp.lowcbf = lowcbf
        return self

    def build(self):
        return self.csp
