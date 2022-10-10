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
    "ScriptConfiguration",
    "ExecutionConfiguration",
    "ResourceConfiguration",
    "ScanTypesBeams",
    "ScanType",
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
        spectral_window_id: str = None,
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

    def __init__(self, pb_id: str, kind: List[str]):
        self.pb_id = pb_id
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, PbDependency):
            return False
        return self.pb_id == other.pb_id and self.kind == other.kind


class ScriptConfiguration:
    """
    Class to hold ScriptConfiguration
    """

    def __init__(self, kind: str = None, name: str = None, version: str = None):
        self.kind = kind
        self.name = name
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, ScriptConfiguration):
            return False
        return (
            self.kind == other.kind
            and self.name == other.name
            and self.version == other.version
        )


class ProcessingBlockConfiguration:
    """
    Class to hold ProcessingBlock configuration
    """

    def __init__(
        self,
        pb_id: str = None,
        workflow: SDPWorkflow = None,
        parameters: Dict = None,
        dependencies: List[PbDependency] = None,
        sbi_ids: List = None,
        script: ScriptConfiguration = None,
    ):
        self.pb_id = pb_id
        self.workflow = workflow
        self.parameters = parameters
        self.dependencies = dependencies
        self.sbi_ids = sbi_ids
        self.script = script

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
        )


class BeamConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(
        self,
        beam_id: str = None,
        function: str = None,
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

    def __init__(self, channels_id: str = None, spectral_windows: List[Channel] = None):
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

    def __init__(self, polarisations_id: str = None, corr_type: List[str] = None):
        self.polarisations_id = polarisations_id
        self.corr_type = corr_type

    def __eq__(self, other):
        if not isinstance(other, PolarisationConfiguration):
            return False
        return (
            self.polarisations_id == other.polarisations_id
            and self.corr_type == other.corr_type
        )


class PhaseDir:
    """
    Class to hold Dependencies for FieldConfiguration
    """

    def __init__(
        self,
        ra: List = None,
        dec: List = None,
        reference_time: str = None,
        reference_frame: str = None,
    ):
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

    def __init__(
        self,
        field_id: str = None,
        pointing_fqdn: str = None,
        phase_dir: PhaseDir = None,
    ):
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


class ScanTypesBeams:
    def __init__(
        self,
        field_id: str = None,
        channels_id: str = None,
        polarisations_id: str = None,
    ):
        self.field_id = field_id
        self.channels_id = channels_id
        self.polarisations_id = polarisations_id

    def __eq__(self, other):
        if not isinstance(other, ScanTypesBeams):
            return False
        return (
            self.field_id == other.field_id
            and self.channels_id == other.channels_id
            and self.polarisations_id == other.polarisations_id
        )


class ScanTypes:
    def __init__(
        self, scan_type_id: str = None, beams: Dict = None, derive_from: str = None
    ):
        self.scan_type_id = scan_type_id
        self.beams = beams
        self.derive_from = derive_from

    def __eq__(self, other):
        if not isinstance(other, ScanTypes):
            return False
        return (
            self.scan_type_id == other.scan_type_id
            and self.beams == other.beams
            and self.derive_from == other.derive_from
        )


class ExecutionConfiguration:
    """
    Class to hold ExecutionBlock configuration
    """

    def __init__(
        self,
        eb_id: str = None,
        max_length: int = None,
        context: Dict = None,
        beams: List[BeamConfiguration] = None,
        channels: List[ChannelConfiguration] = None,
        polarisations: List[PolarisationConfiguration] = None,
        fields: List[FieldConfiguration] = None,
        scan_types: ScanTypes = None,
    ):
        self.eb_id = eb_id
        self.max_length = max_length
        self.context = context
        self.beams = beams
        self.channels = channels
        self.polarisations = polarisations
        self.fields = fields
        self.scan_types = scan_types

    def __eq__(self, other):
        if not isinstance(other, ExecutionConfiguration):
            return False
        return (
            self.eb_id == other.eb_id
            and self.max_length == other.max_length
            and self.context == other.context
            and self.beams == other.beams
            and self.channels == other.channels
            and self.polarisations == other.polarisations
            and self.fields == other.fields
        )


class ResourceConfiguration:
    """
    Class to hold Dependencies for ExecutionBlock
    """

    def __init__(
        self, csp_links: List = None, receptors: List = None, receive_nodes: int = None
    ):
        self.csp_links = csp_links
        self.receptors = receptors
        self.receive_nodes = receive_nodes

    def __eq__(self, other):
        if not isinstance(other, ResourceConfiguration):
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
        execution_block: ExecutionConfiguration = None,
        interface: str = None,
        resources: ResourceConfiguration = None,
    ):
        self.eb_id = eb_id
        self.max_length = max_length
        self.scan_types = scan_types
        self.processing_blocks = processing_blocks
        self.interface = interface
        self.execution_block = execution_block
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
