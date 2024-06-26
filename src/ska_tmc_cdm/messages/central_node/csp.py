"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional

from ska_tmc_cdm.messages.base import CdmObject

__all__ = [
    "CSPConfiguration",
    "CommonConfiguration",
    "ResourceConfiguration",
    "LowCbfConfiguration",
]


class CommonConfiguration(CdmObject):
    """
    Class to get common subarray id

    :param subarray_id: Low csp assign resource subarray ID
    """

    subarray_id: Optional[int] = None


class ResourceConfiguration(CdmObject):
    """
    Class to contain keys
    for resources under lowcbf
    """

    device: Optional[str] = None
    shared: Optional[bool] = None
    fw_image: Optional[str] = None
    fw_mode: Optional[str] = None


class LowCbfConfiguration(CdmObject):
    """
    Class to get lowcbf configuration within low csp assign resources


    Creates a new LowCbfConfiguration.
    :param resources: list of objects containing fields from ResourceConfiguration
    """

    resources: list[ResourceConfiguration]


class CSPConfiguration(CdmObject):
    """
    Class to get CSP Configuration
    """

    interface: Optional[str] = None
    common: Optional[CommonConfiguration] = None
    lowcbf: Optional[LowCbfConfiguration] = None
