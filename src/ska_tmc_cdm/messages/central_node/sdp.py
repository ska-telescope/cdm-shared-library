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
    "ExecutionBlockConfiguration",
    "ScriptConfiguration",
    "EBScanTypeBeam",
    "EBScanType",
]


class SDPWorkflow:  # pylint: disable=too-few-public-methods
    """
    Class to hold SDPWorkflows for ProcessingBlock
    """

    def __init__(self, name: str, kind: str, version: str) -> object:
        """
        Create a new SDPWorkflow object.

        :param name: The name of the processing script
        :param kind: The kind of processing script
        :param version: Version of the processing script
        """
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
    ) -> object:
        """
        Create a new Channel object.

        :param count: Number of channels
        :param start: First channel ID
        :param stride: Distance between subsequent channel IDs
        :param freq_min: Lower bound of first channel
        :param freq_max: Upper bound of last channel
        :param link_map: Channel map that specifies which network link is going to get used to send channels to SDP.
                         Intended to allow SDP to optimise network and receive node configuration.
        :param spectral_window_id: spectral_window_id
        """

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

    def __init__(
        self,
        scan_type_id,
        reference_frame: str,
        ra: str,
        dec: str,
        channels: List[Channel],
    ) -> object:
        """
         Create a new ScanType object.

        :param scan_type_id:(any scan type)
        :param reference_frame: Specification of the reference frame or system for a set of pointing coordinates
        :param ra: Right Ascension in degrees
        :param dec: Declination in degrees
        :param channels: Expected channel configuration.
        """
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

    def __init__(self, pb_id: str, kind: List[str]) -> object:
        """
        Create a new PbDependency object.

        :param pb_id: Unique identifier for this processing block
        :param kind: The kind of processing script (realtime or batch)
        """
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
        """
        Create a new ScriptConfiguration object.

        :param name: The name of the processing script
        :param kind: The kind of processing script
        :param version: Version of the processing script
        """
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
    ) -> object:

        """
        Create a new ProcessingBlockConfiguration object.

        :param pb_id: Processing block ID
        :param workflow: Specification of the workflow to be executed along with configuration parameters for the workflow.
        :param parameters: Processing script parameters
        :param dependencies: Dependencies on other processing blocks
        :param sbi_ids: List of scheduling block ids
        :param script: Processing script description (dictionary for now)
        """
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
    Class to hold Dependencies for Beam Configuration
    """

    def __init__(
        self,
        beam_id: str = None,
        function: str = None,
        search_beam_id: int = None,
        timing_beam_id: int = None,
        vlbi_beam_id: int = None,
    ) -> object:
        """
        Create a new BeamConfiguration object.

        :param beam_id: Name to identify the beam within the SDP configuration.
        :param function: Identifies the type and origin of the generated beam data.
        :param search_beam_id: search_beam_id
        :param timing_beam_id: timing_beam_id
        :param vlbi_beam_id: vlbi_beam_id
        """
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
    Class to hold Dependencies for Channel Configuration
    """

    def __init__(
        self, channels_id: str = None, spectral_windows: List[Channel] = None
    ) -> object:
        """
        Create a new ChannelConfiguration object.

        :param channels_id: channels_id
        :param spectral_windows: spectral_windows
        """
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
    Class to hold Dependencies for Polarisation Configuration
    """

    def __init__(
        self, polarisations_id: str = None, corr_type: List[str] = None
    ) -> object:
        """
        Create a new PolarisationConfiguration object.

        :param polarisations_id: Polarisation definitions id
        :param corr_type: corr_type
        """
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
    Class to hold PhaseDir configuration
    """

    def __init__(
        self,
        ra: List = None,
        dec: List = None,
        reference_time: str = None,
        reference_frame: str = None,
    ) -> object:
        """
        Create a new PhaseDir object.

        :param ra: Right Ascension in degrees (see ADR-49)
        :param dec: Declination in degrees (see ADR-49)
        :param reference_time: reference_time,
        :param reference_frame: Specification of the reference frame or system for a set of pointing coordinates (see ADR-49)
        """
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
    Class to hold Field configuration
    """

    def __init__(
        self,
        field_id: str = None,
        pointing_fqdn: str = None,
        phase_dir: PhaseDir = None,
    ) -> object:
        """
        Create a new FieldConfiguration object.

        :param field_id: field_id
        :param pointing_fqdn: pointing_fqdn
        :param phase_dir: Phase direction
        """
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


class EBScanTypeBeam:
    """
    Class to hold EBScanTypeBeam Configuration
    """

    def __init__(
        self,
        field_id: str = None,
        channels_id: str = None,
        polarisations_id: str = None,
    ) -> object:
        """
        Create a new EBScanTypeBeam object.

        :param field_id: field_id
        :param channels_id: channels_id
        :param polarisations_id: polarisations_id
        """
        self.field_id = field_id
        self.channels_id = channels_id
        self.polarisations_id = polarisations_id

    def __eq__(self, other):
        if not isinstance(other, EBScanTypeBeam):
            return False
        return (
            self.field_id == other.field_id
            and self.channels_id == other.channels_id
            and self.polarisations_id == other.polarisations_id
        )


class EBScanType:
    """
    Class to hold EBScanType configuration
    """

    def __init__(
        self,
        scan_type_id: str = None,
        beams: Dict[str, EBScanTypeBeam] = None,
        derive_from: str = None,
    ) -> object:
        """
        Create a new EBScanType object.

        :param scan_type_id: scan_type_id
        :param beams: Beam parameters for the purpose of the Science Data Processor.
        :param derive_from: derive_from
        """
        self.scan_type_id = scan_type_id
        self.beams = beams
        self.derive_from = derive_from

    def __eq__(self, other):
        if not isinstance(other, EBScanType):
            return False
        return (
            self.scan_type_id == other.scan_type_id
            and self.beams == other.beams
            and self.derive_from == other.derive_from
        )


class ExecutionBlockConfiguration:
    """
    Class to hold ExecutionBlock configuration
    """

    def __init__(
        self,
        eb_id: str = None,
        max_length: float = None,
        context: Dict = None,
        beams: List[BeamConfiguration] = None,
        channels: List[ChannelConfiguration] = None,
        polarisations: List[PolarisationConfiguration] = None,
        fields: List[FieldConfiguration] = None,
        scan_types: List[EBScanType] = None,
    ) -> object:
        """
        Create a new ExecutionBlockConfiguration object.

        :param eb_id: Execution block ID to associate with processing
        :param max_length: Hint about the maximum observation length to support by the SDP.
        :param context: Free-form information from OET, see ADR-54
        :param beams: Beam parameters for the purpose of the Science Data Processor.
        :param channels: Spectral windows per channel configuration.
        :param polarisations: Polarisation definition.
        :param fields: Fields / Targets
        :param scan_types: Scan types. Associates scans with per-beam fields & channel configurations
        """
        self.eb_id = eb_id
        self.max_length = max_length
        self.context = context
        self.beams = beams
        self.channels = channels
        self.polarisations = polarisations
        self.fields = fields
        self.scan_types = scan_types

    def __eq__(self, other):
        if not isinstance(other, ExecutionBlockConfiguration):
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


class SDPConfiguration:
    """
    Class to hold SDP Configuration
    """

    def __init__(
        self,
        eb_id: str = None,
        max_length: float = None,
        scan_types: List[ScanType] = None,
        processing_blocks: List[ProcessingBlockConfiguration] = None,
        execution_block: ExecutionBlockConfiguration = None,
        resources: Dict = None,
        interface: str = None,
    ) -> object:

        """
        Create a new SDPConfiguration object.

        :param eb_id: Execution block ID to associate with processing
        :param max_length: Hint about the maximum observation length to support by the SDP.
        :param scan_types: Scan types to be supported on subarray
        :param processing_blocks: A Processing Block is an atomic unit of data processing for the purpose of SDP’s internal scheduler
        :param execution_block: execution_block
        :param interface: url string to determine JsonSchema version
        :param resources: resources

        """
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
