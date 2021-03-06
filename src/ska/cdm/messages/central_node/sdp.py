"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List, Dict

__all__ = [
    "SDPWorkflow",
    "SDPConfiguration",
    "ProcessingBlockConfiguration",
    "PbDependency",
    "ScanType",
    "Channel",
]


class SDPWorkflow:  # pylint: disable=too-few-public-methods
    """
    Class to hold SDPWorkflows for ProcessingBlock
    """

    def __init__(self, workflow_id: str, workflow_type: str, version: str):
        self.workflow_id = workflow_id
        self.workflow_type = workflow_type
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        return (
            self.workflow_id == other.workflow_id
            and self.workflow_type == other.workflow_type
            and self.version == other.version
        )


class Channel:
    """
    Class to hold Channels for ScanType
    """

    def __init__(
        self,
        count: int,
        start: int,
        stride: int,
        freq_min: float,
        freq_max: float,
        link_map: List[List],
    ):
        self.count = count
        self.start = start
        self.stride = stride
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.link_map = link_map

    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        return (
            self.count == other.count
            and self.start == other.start
            and self.stride == other.stride
            and self.freq_min == other.freq_min
            and self.freq_max == other.freq_max
            and self.link_map == other.link_map
        )


class ScanType:
    """
    Class to hold ScanType configuration
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, st_id, coordinate_system: str, ra: str, dec: str, channels: List[Channel]
    ):
        self.st_id = st_id
        self.coordinate_system = coordinate_system
        self.ra = ra  # pylint: disable=invalid-name
        self.dec = dec
        self.channels = channels

    def __eq__(self, other):
        if not isinstance(other, ScanType):
            return False
        return (
            self.st_id == other.st_id
            and self.coordinate_system == other.coordinate_system
            and self.ra == other.ra
            and self.dec == other.dec
            and self.channels == other.channels
        )


class PbDependency:
    """
    Class to hold Dependencies for ProcessingBlock
    """

    def __init__(self, pb_id: str, pb_type: List[str]):
        self.pb_id = pb_id
        self.pb_type = pb_type

    def __eq__(self, other):
        if not isinstance(other, PbDependency):
            return False
        return self.pb_id == other.pb_id and self.pb_type == other.pb_type


class ProcessingBlockConfiguration:
    """
    Class to hold ProcessingBlock configuration
    """

    def __init__(
        self,
        pb_id: str,
        workflow: SDPWorkflow,
        parameters: Dict,
        dependencies: List[PbDependency] = None,
    ):
        self.pb_id = pb_id
        self.workflow = workflow
        self.parameters = parameters
        self.dependencies = dependencies

    def __eq__(self, other):
        if not isinstance(other, ProcessingBlockConfiguration):
            return False
        return (
            self.pb_id == other.pb_id
            and self.workflow == other.workflow
            and self.parameters == other.parameters
            and self.dependencies == other.dependencies
        )


class SDPConfiguration:
    """
    Class to hold SDPConfiguration
    """

    def __init__(
        self,
        sdp_id: str,
        max_length: float,
        scan_types: List[ScanType],
        processing_blocks: List[ProcessingBlockConfiguration],
    ):
        self.sdp_id = sdp_id
        self.max_length = max_length
        self.scan_types = scan_types
        self.processing_blocks = processing_blocks

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return (
            self.sdp_id == other.sdp_id
            and self.max_length == other.max_length
            and self.scan_types == other.scan_types
            and self.processing_blocks == other.processing_blocks
        )
