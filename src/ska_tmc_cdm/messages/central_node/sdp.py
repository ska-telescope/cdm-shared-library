"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import Dict, List

__all__ = [
    "SDPWorkflow",
    "SDPConfiguration",
    "ProcessingBlockConfiguration",
    "PbDependency",
    "ScanType",
    "Channel",
    "BeamConfiguration",
    "ChannelConfiguration",
    "PolarisationConfiguration",
    "PhaseDir",
    "FieldConfiguration",
    "ExecutionBlockConfuguration",
    "ResourceBlockConfiguration",
]


class SDPWorkflow:  # pylint: disable=too-few-public-methods
    """
    Class to hold SDPWorkflows for ProcessingBlock
    """

    def __init__(self, name: str, kind: str, version: str):
        self.name = name
        self.kind = kind
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, SDPWorkflow):
            return False
        return (
            self.name == other.name
            and self.kind == other.kind
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
        spectral_window_id: str = None
    ):
        self.count = count
        self.start = start
        self.stride = stride
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.link_map = link_map
        self.spectral_window_id = spectral_window_id

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
            and self.spectral_window_id == other.spectral_window_id
        )


class ScanType:
    """
    Class to hold ScanType configuration
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scan_type_id,
        reference_frame: str,
        ra: str,
        dec: str,
        channels: List[Channel],
    ):
        self.scan_type_id = scan_type_id
        self.reference_frame = reference_frame
        self.ra = ra  # pylint: disable=invalid-name
        self.dec = dec
        self.channels = channels

    def __eq__(self, other):
        if not isinstance(other, ScanType):
            return False
        return (
            self.scan_type_id == other.scan_type_id
            and self.reference_frame == other.reference_frame
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
        pb_id: str = None,
        workflow: SDPWorkflow = None,
        parameters: Dict = None,
        dependencies = None,  # how to handel datatype change for now added new key dependencies_new
        sbi_ids: List = None,
        script: Dict = None,
        # dependencies_new: Dict = None,
    ):
        self.pb_id = pb_id
        self.workflow = workflow
        self.parameters = parameters
        self.dependencies = dependencies
        self.sbi_ids = sbi_ids
        self.script = script
        # self.dependencies_new = dependencies_new

    def __eq__(self, other):
        if not isinstance(other, ProcessingBlockConfiguration):
            return False
        return (
            self.pb_id == other.pb_id
            and self.workflow == other.workflow
            and self.parameters == other.parameters
            and self.dependencies == other.dependencies
            and self.sbi_ids == other.sbi_ids
            and self.script == other.script
            # and self.dependencies_new == other.dependencies_new
        )


class BeamConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(
        self,
        beam_id: str,
        function: str,
        search_beam_id: int = None,
        timing_beam_id: int = None,
        vlbi_beam_id: int = None,
    ):
        self.beam_id = beam_id
        self.function = function
        self.search_beam_id = search_beam_id
        self.timing_beam_id = timing_beam_id
        self.vlbi_beam_id = vlbi_beam_id

    def __eq__(self, other):
        if not isinstance(other, BeamConfiguration):
            return False
        return (
            self.beam_id == other.beam_id
            and self.function == other.function
            and self.search_beam_id == other.search_beam_id
            and self.timing_beam_id == other.timing_beam_id
            and self.vlbi_beam_id == other.vlbi_beam_id
        )


class ChannelConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(self, channels_id: str, spectral_windows: List[Channel] = None):
        self.channels_id = channels_id
        self.spectral_windows = spectral_windows

    def __eq__(self, other):
        if not isinstance(other, ChannelConfiguration):
            return False
        return (
            self.channels_id == other.channels_id
            and self.spectral_windows == other.spectral_windows
        )


class PolarisationConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(self, polarisation_id: str, corr_type: List[str] = None):
        self.polarisation_id = polarisation_id
        self.corr_type = corr_type

    def __eq__(self, other):
        if not isinstance(other, PolarisationConfiguration):
            return False
        return (
            self.polarisation_id == other.polarisation_id
            and self.corr_type == other.corr_type
        )


class PhaseDir:
    """
    Class to hold Dependencies for FieldConfiguration
    """

    def __init__(self, ra: List, dec: List, reference_time: str, reference_frame: str):
        self.ra = ra
        self.dec = dec
        self.reference_time = reference_time
        self.reference_frame = reference_frame

    def __eq__(self, other):
        if not isinstance(other, PhaseDir):
            return False
        return (
            self.ra == other.ra
            and self.dec == other.dec
            and self.reference_time == other.reference_time
            and self.reference_frame == other.reference_frame
        )


class FieldConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(self, field_id: str, pointing_fqdn: str, phase_dir: PhaseDir = None):
        self.field_id = field_id
        self.pointing_fqdn = pointing_fqdn
        self.phase_dir = phase_dir

    def __eq__(self, other):
        if not isinstance(other, FieldConfiguration):
            return False
        return (
            self.field_id == other.field_id
            and self.phase_dir == other.phase_dir
            and self.pointing_fqdn == other.pointing_fqdn
        )


class ExecutionBlockConfuguration:
    """
    Class to hold ExecutionBlock configuration
    """

    def __init__(
        self,
        eb_id: str,
        max_length: int,
        context: Dict,
        beams: List[BeamConfiguration] = None,
        channels: List[ChannelConfiguration] = None,
        polarisation: List[PolarisationConfiguration] = None,
        fields: List[FieldConfiguration] = None,
    ):
        self.eb_id = eb_id
        self.max_length = max_length
        self.context = context
        self.beams = beams
        self.channels = channels
        self.polarisation = polarisation
        self.fields = fields

    def __eq__(self, other):
        if not isinstance(other, ExecutionBlockConfuguration):
            return False
        return (
            self.eb_id == other.eb_id
            and self.max_length == other.max_length
            and self.context == other.context
            and self.beams == other.beams
            and self.channels == other.channels
            and self.polarisation == other.polarisation
            and self.fields == other.fields
        )


class ResourceBlockConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(self, csp_links: List, receptors: List, receive_nodes: int):
        self.csp_links = csp_links
        self.receptors = receptors
        self.receive_nodes = receive_nodes

    def __eq__(self, other):
        if not isinstance(other, ResourceBlockConfiguration):
            return False
        return (
            self.csp_links == other.csp_links
            and self.receptors == other.receptors
            and self.receive_nodes == other.receive_nodes
        )


class SDPConfiguration:
    """
    Class to hold SDPConfiguration
    """

    def __init__(
        self,
        eb_id: str = None,
        max_length: float = None,
        scan_types: List[ScanType] = None,
        processing_blocks: List[ProcessingBlockConfiguration] = None,
        execution_block: ExecutionBlockConfuguration = None,
        interface: str = None,
        resources: ResourceBlockConfiguration = None,
    ):
        self.eb_id = eb_id
        self.max_length = max_length
        self.scan_types = scan_types
        self.processing_blocks = processing_blocks
        self.interface = (interface,)
        self.execution_block = (execution_block,)
        self.resources = resources

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return (
            self.eb_id == other.eb_id
            and self.max_length == other.max_length
            and self.scan_types == other.scan_types
            and self.processing_blocks == other.processing_blocks
            and self.interface == other.interface
            and self.resources == other.resources
        )
