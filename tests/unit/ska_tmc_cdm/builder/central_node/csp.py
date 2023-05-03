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

    def __init__(self) -> "CommonConfigurationBuilder":
        self.common = None
        self.subarray_id = None

    def set_subarray_id(self, subarray_id=int) -> "CommonConfigurationBuilder":
        self.subarray_id = subarray_id
        return self

    def build(self) -> CommonConfiguration:
        self.common = CommonConfiguration(self.subarray_id)
        return self.common


class ResourceConfigurationBuilder:
    """
    ResourceConfigurationBuilder is a test data builder for CDM ResourceConfiguration objects.

    By default, ResourceConfigurationBuilder will build an ResourceConfiguration

    for low observation command.
    """

    def __init__(self) -> "ResourceConfigurationBuilder":
        self.resource = None
        self.device = None
        self.shared = None
        self.fw_image = None
        self.fw_mode = None

    def set_device(self, device=str) -> "ResourceConfigurationBuilder":
        self.device = device
        return self

    def set_shared(self, shared=bool) -> "ResourceConfigurationBuilder":
        self.shared = shared
        return self

    def set_fw_image(self, fw_image=str) -> "ResourceConfigurationBuilder":
        self.fw_image = fw_image
        return self

    def set_fw_mode(self, fw_mode=str) -> "ResourceConfigurationBuilder":
        self.fw_mode = fw_mode
        return self

    def build(self) -> ResourceConfiguration:
        self.resource = ResourceConfiguration(
            self.device,
            self.shared,
            self.fw_image,
            self.fw_mode,
        )
        return self.resource


class LowCbfConfigurationBuilder:
    """
    LowCbfConfigurationBuilder is a test data builder for CDM LowCbfConfiguration objects.

    By default, LowCbfConfigurationBuilder will build an LowCbfConfiguration

    for low observation command.
    """

    def __init__(self) -> "LowCbfConfigurationBuilder":
        self.lowcbf = None
        self.resources = None

    def set_resources(self, resources=list) -> "LowCbfConfigurationBuilder":
        self.resources = resources
        return self

    def build(self) -> LowCbfConfiguration:
        self.lowcbf = LowCbfConfiguration(self.resources)
        return self.lowcbf


class CSPConfigurationBuilder:
    """
    CSPConfigurationBuilder is a test data builder for CDM CSPConfiguration objects.

    By default, CSPConfigurationBuilder will build an CSPConfiguration

    for low observation command.
    """

    def __init__(self) -> "CSPConfigurationBuilder":
        self.csp = None
        self.interface = None
        self.common = None
        self.lowcbf = None

    def set_interface(self, interface=str) -> "CSPConfigurationBuilder":
        self.interface = interface
        return self

    def set_common(self, common) -> "CSPConfigurationBuilder":
        self.common = common
        return self

    def set_lowcbf(self, lowcbf) -> "CSPConfigurationBuilder":
        self.lowcbf = lowcbf
        return self

    def build(self) -> CSPConfiguration:
        self.csp = CSPConfiguration(
            self.interface,
            self.common,
            self.lowcbf,
        )
        return self.csp
