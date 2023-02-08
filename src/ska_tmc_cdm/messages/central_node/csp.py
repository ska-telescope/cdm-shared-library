"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List

__all__ = [
    "CSPConfiguration",
    "CommonConfiguration",
    "ResourceConfiguration",
    "LowCbfConfiguration",
]


class CommonConfiguration:
    """
    Class to get common subarray id
    """

    def __init__(
        self,
        subarray_id: int = None,
    ) -> object:
        """
        Create a new CommonConfiguration.
        :param subarray_id: Low csp assign resource subarray ID
        """
        self.subarray_id = subarray_id

    def __eq__(self, other):
        if not isinstance(other, CommonConfiguration):
            return False
        return self.subarray_id == other.subarray_id


class ResourceConfiguration:
    """
    Class to contain keys
    for resources under lowcbf
    """

    def __init__(
        self,
        device: str = None,
        shared: bool = None,
        fw_image: str = None,
        fw_mode: str = None,
    ) -> object:

        """
        Create a new ResourceConfiguration object.
        :param device:
        :param shared:
        :param fw_image:
        :param fw_mode:
        """
        self.device = device
        self.shared = shared
        self.fw_image = fw_image
        self.fw_mode = fw_mode

    def __eq__(self, other):
        if not isinstance(other, ResourceConfiguration):
            return False
        return (
            self.device == other.device
            and self.shared == other.shared
            and self.fw_image == other.fw_image
            and self.fw_mode == other.fw_mode
        )


class LowCbfConfiguration:
    """
    Class to get lowcbf configuration within low csp assign resources
    """

    def __init__(
        self,
        resources: List[ResourceConfiguration],
    ) -> object:
        """
        Create a new LowCbfConfiguration.
        :param resources: list of objects
        containing fields from ResourceConfiguration
        """
        self.resources = resources

    def __eq__(self, other):
        if not isinstance(other, LowCbfConfiguration):
            return False
        return self.resources == other.resources


class CSPConfiguration:
    """
    Class to get CSP Configuration
    """

    def __init__(
        self,
        interface: str = None,
        common: CommonConfiguration = None,
        lowcbf: LowCbfConfiguration = None,
    ) -> object:

        """
        Create a new CSPConfiguration object.
        :param interface:
        :param common:
        :param lowcbf:
        """
        self.interface = interface
        self.common = common
        self.lowcbf = lowcbf

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return (
            self.interface == other.interface
            and self.common == other.common
            and self.lowcbf == other.lowcbf
        )
