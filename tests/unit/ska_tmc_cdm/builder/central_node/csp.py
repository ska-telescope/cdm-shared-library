from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourceConfiguration,
)


class CommonConfigurationBuilder:
    """
    CommonConfigurationBuilder is a test data builder for CDM CommonConfiguration objects.

    By default, CommonConfigurationBuilder will build an CommonConfiguration

    for low observation command.
    """

    def __init__(self) -> "CommonConfigurationBuilder":
        self.subarray_id = None

    def set_subarray_id(self, subarray_id: int) -> "CommonConfigurationBuilder":
        """
        Set the subarray_id
        :param subarray_id: Subarray ID
        """
        self.subarray_id = subarray_id
        return self

    def build(self) -> CommonConfiguration:
        """
        Build or create CDM CommonConfiguration object
        :return: CDM CommonConfiguration object
        """
        return CommonConfiguration(self.subarray_id)


class ResourceConfigurationBuilder:
    """
    ResourceConfigurationBuilder is a test data builder for CDM ResourceConfiguration objects.

    By default, ResourceConfigurationBuilder will build an ResourceConfiguration

    for low observation command.
    """

    def __init__(self) -> "ResourceConfigurationBuilder":
        self.device = None
        self.shared = None
        self.fw_image = None
        self.fw_mode = None

    def set_device(self, device: str) -> "ResourceConfigurationBuilder":
        """
        Set the device
        :param device: Device
        """
        self.device = device
        return self

    def set_shared(self, shared: bool) -> "ResourceConfigurationBuilder":
        """
        Set the shared
        :param shared: Shared
        """
        self.shared = shared
        return self

    def set_fw_image(self, fw_image: str) -> "ResourceConfigurationBuilder":
        """
        Set the fw_image
        :param fw_image: Fw image
        """
        self.fw_image = fw_image
        return self

    def set_fw_mode(self, fw_mode: str) -> "ResourceConfigurationBuilder":
        """
        Set the fw_mode
        :param fw_mode: Fw mode
        """
        self.fw_mode = fw_mode
        return self

    def build(self) -> ResourceConfiguration:
        """
        Build or create CDM ResourceConfiguration object
        :return: CDM ResourceConfiguration object
        """
        return ResourceConfiguration(
            self.device,
            self.shared,
            self.fw_image,
            self.fw_mode,
        )


class LowCbfConfigurationBuilder:
    """
    LowCbfConfigurationBuilder is a test data builder for CDM LowCbfConfiguration objects.

    By default, LowCbfConfigurationBuilder will build an LowCbfConfiguration

    for low observation command.
    """

    def __init__(self) -> "LowCbfConfigurationBuilder":
        self.resources = None

    def set_resources(self, resources: list) -> "LowCbfConfigurationBuilder":
        """
        Set the resources
        :param resources: Resources
        """
        self.resources = resources
        return self

    def build(self) -> LowCbfConfiguration:
        """
        Build or create CDM LowCbfConfiguration object
        :return: CDM LowCbfConfiguration object
        """
        return LowCbfConfiguration(self.resources)


class CSPConfigurationBuilder:
    """
    CSPConfigurationBuilder is a test data builder for CDM CSPConfiguration objects.

    By default, CSPConfigurationBuilder will build an CSPConfiguration

    for low observation command.
    """

    def __init__(self) -> "CSPConfigurationBuilder":
        self.interface = None
        self.common = None
        self.lowcbf = None

    def set_interface(self, interface: str) -> "CSPConfigurationBuilder":
        """
        Set the interface
        :param interface: Interface
        """
        self.interface = interface
        return self

    def set_common(self, common: CommonConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the common
        :param common: Common
        """
        self.common = common
        return self

    def set_lowcbf(self, lowcbf: LowCbfConfiguration) -> "CSPConfigurationBuilder":
        """
        Set the lowcbf
        :param lowcbf: Lowcbf
        """
        self.lowcbf = lowcbf
        return self

    def build(self) -> CSPConfiguration:
        """
        Build or create CDM CSPConfiguration object
        :return: CDM CSPConfiguration object
        """
        return CSPConfiguration(
            self.interface,
            self.common,
            self.lowcbf,
        )
