"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List
from dataclasses import dataclass

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
    """
    subarray_id: int = None

@dataclass
class ResourceConfiguration:
    """
    Class to contain keys
    for resources under lowcbf
    """
    device: str = None
    shared: bool = None
    fw_image: str = None
    fw_mode: str = None

@dataclass
class LowCbfConfiguration:
    """
    Class to get lowcbf configuration within low csp assign resources


    Creates a new LowCbfConfiguration.
    :param resources: list of objects containing fields from ResourceConfiguration
    """
    resources: List[ResourceConfiguration]

@dataclass
class CSPConfiguration:
    """
    Class to get CSP Configuration
    """
    interface: str = None
    common: CommonConfiguration = None
    lowcbf: LowCbfConfiguration = None