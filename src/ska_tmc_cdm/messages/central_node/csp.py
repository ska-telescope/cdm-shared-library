"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Optional

from pydantic.dataclasses import dataclass

__all__ = [
    "CSPConfiguration",
    "CommonConfiguration",
    "ResourceConfiguration",
    "LowCbfConfiguration",
]


@dataclass
class CommonConfiguration:
    """
    Class to get common subarray id

    :param subarray_id: Low csp assign resource subarray ID
    """

    subarray_id: Optional[int] = None


@dataclass
class ResourceConfiguration:
    """
    Class to contain keys
    for resources under lowcbf
    """

    device: Optional[str] = None
    shared: Optional[bool] = None
    fw_image: Optional[str] = None
    fw_mode: Optional[str] = None


@dataclass
class LowCbfConfiguration:
    """
    Class to get lowcbf configuration within low csp assign resources


    Creates a new LowCbfConfiguration.
    :param resources: list of objects containing fields from ResourceConfiguration
    """

    resources: list[ResourceConfiguration]


@dataclass
class CSPConfiguration:
    """
    Class to get CSP Configuration
    """

    interface: Optional[str] = None
    common: Optional[CommonConfiguration] = None
    lowcbf: Optional[LowCbfConfiguration] = None
