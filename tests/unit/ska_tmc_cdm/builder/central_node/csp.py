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
    """
    CommonConfigurationBuilder is a test data builder for CDM CommonConfiguration objects.

    By default, CommonConfigurationBuilder will build an CommonConfiguration

    for low observation command.
    """

    def __init__(
        self,
        common=CommonConfiguration(
            subarray_id=int,
        ),
    ) -> object:
        self.common = common
        self.subarray_id = common.subarray_id

    def set_subarray_id(self, subarray_id):
        self.common.subarray_id = subarray_id
        return self

    def build(self):
        return self.common


class ResourceConfigurationBuilder:
    """
    ResourceConfigurationBuilder is a test data builder for CDM ResourceConfiguration objects.

    By default, ResourceConfigurationBuilder will build an ResourceConfiguration

    for low observation command.
    """

    def __init__(
        self,
        resource=ResourceConfiguration(
            device=str,
            shared=bool,
            fw_image=str,
            fw_mode=str,
        ),
    ) -> object:
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
    """
    LowCbfConfigurationBuilder is a test data builder for CDM LowCbfConfiguration objects.

    By default, LowCbfConfigurationBuilder will build an LowCbfConfiguration

    for low observation command.
    """

    def __init__(
        self, lowcbf=LowCbfConfiguration(resources=ResourceConfiguration())
    ) -> object:
        self.lowcbf = lowcbf

    def set_resources(self, resources):
        self.lowcbf.resources = resources
        return self

    def build(self):
        return self.lowcbf


class CSPConfigurationBuilder:
    """
    CSPConfigurationBuilder is a test data builder for CDM CSPConfiguration objects.

    By default, CSPConfigurationBuilder will build an CSPConfiguration

    for low observation command.
    """

    def __init__(self, csp=CSPConfiguration()) -> object:
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
