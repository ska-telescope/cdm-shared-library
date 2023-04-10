from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourceConfiguration,
)


class CommonConfigurationBuilder:
    def __init__(self, common=CommonConfiguration()):
        self.common = common

    def setsubarray_id(self, subarray_id):
        self.common.subarray_id = subarray_id
        return self

    def build(self):
        return self.common


class ResourceConfigurationBuilder:
    def __init__(self, resource=ResourceConfiguration()):
        self.resource = resource

    def setdevice(self, device):
        self.resource.device = device
        return self

    def setshared(self, shared):
        self.resource.shared = shared
        return self

    def setfw_image(self, fw_image):
        self.resource.fw_image = fw_image
        return self

    def setfw_mode(self, fw_mode):
        self.resource.fw_mode = fw_mode
        return self

    def build(self):
        return self.resource


class LowCbfConfigurationBuilder:
    def __init__(self, lowcbf=LowCbfConfiguration(resources=[ResourceConfiguration])):
        self.lowcbf = lowcbf

    def setresources(self, resources):
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

    def setinterface(self, interface):
        self.csp.interface = interface
        return self

    def setcommon(self, common):
        self.csp.common = common
        return self

    def setlowcbf(self, lowcbf):
        self.csp.lowcbf = lowcbf
        return self

    def build(self):
        return self.csp
