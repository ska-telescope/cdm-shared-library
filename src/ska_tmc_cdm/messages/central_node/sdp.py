"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass

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


@dataclass
class SDPWorkflow:
    """
    Class to hold SDPWorkflows for ProcessingBlock

    Create a new SDPWorkflow object.

    :param name: The name of the processing script
    :param kind: The kind of processing script
    :param version: Version of the processing script
    """

    name: str
    kind: str
    version: str


@dataclass
class Channel:
    """
    Class to hold Channels for ScanType

    Create a new Channel object.

    :param count: Number of channels
    :param start: First channel ID
    :param stride: Distance between subsequent channel IDs
    :param freq_min: Lower bound of first channel
    :param freq_max: Upper bound of last channel
    :param link_map: Channel map that specifies which network link is going to get used to send channels to SDP.
                     Intended to allow SDP to optimize network and receive node configuration.
    :param spectral_window_id: spectral_window_id
    """

    # TODO: double-check what's optional here:
    count: int
    start: int
    stride: Optional[int]
    freq_min: float
    freq_max: float
    link_map: Optional[list[list]]
    spectral_window_id: Optional[str] = None


@dataclass
class ScanType:
    """
    Class to hold ScanType configuration

    :param scan_type_id: (any scan type)
    :param reference_frame: Specification of the reference frame or system for a set of pointing coordinates
    :param ra: Right Ascension in degrees
    :param dec: Declination in degrees
    :param channels: Expected channel configuration.
    """

    scan_type_id: str
    reference_frame: str
    ra: str
    dec: str
    channels: list[Channel]


@dataclass
class PbDependency:
    """
    Class to hold Dependencies for ProcessingBlock

    :param pb_id: Unique identifier for this processing block
    :param kind: The kind of processing script (realtime or batch)
    """

    pb_id: str
    kind: list[str]


@dataclass
class ScriptConfiguration:
    """
    Class to hold ScriptConfiguration

    :param name: The name of the processing script
    :param kind: The kind of processing script
    :param version: Version of the processing script
    """

    kind: str = None
    name: str = None
    version: str = None


@dataclass
class ProcessingBlockConfiguration:
    """
    Class to hold ProcessingBlock configuration

    :param pb_id: Processing block ID
    :param workflow: Specification of the workflow to be executed along with configuration parameters for the workflow.
    :param parameters: Processing script parameters
    :param dependencies: Dependencies on other processing blocks
    :param sbi_ids: list of scheduling block ids
    :param script: Processing script description (dictionary for now)
    """

    pb_id: str = None
    workflow: SDPWorkflow = None
    parameters: dict = field(default_factory=dict)
    # FIXME: should probably be `field(default_factory=list)` not `None`
    dependencies: Optional[list[PbDependency]] = None
    # FIXME: should probably be `field(default_factory=list)` not `None`
    sbi_ids: Optional[list[str]] = None
    script: ScriptConfiguration = None


@dataclass
class BeamConfiguration:
    """
    Class to hold Dependencies for Beam Configuration

    :param beam_id: Name to identify the beam within the SDP configuration.
    :param function: Identifies the type and origin of the generated beam data.
    :param search_beam_id: search_beam_id
    :param timing_beam_id: timing_beam_id
    :param vlbi_beam_id: vlbi_beam_id
    """

    beam_id: str = None
    function: str = None
    search_beam_id: int = None
    timing_beam_id: int = None
    vlbi_beam_id: int = None


@dataclass
class ChannelConfiguration:
    """
    Class to hold Dependencies for Channel Configuration

    :param channels_id: channels_id
    :param spectral_windows: spectral_windows
    """

    channels_id: str = None
    spectral_windows: list[Channel] = field(default_factory=list)


@dataclass
class PolarisationConfiguration:
    """
    Class to hold Dependencies for Polarisation Configuration

    :param polarisations_id: Polarisation definitions id
    :param corr_type: corr_type
    """

    polarisations_id: str = None
    corr_type: list[str] = field(default_factory=list)


@dataclass
class PhaseDir:
    """
    Class to hold PhaseDir configuration

    :param ra: Right Ascension in degrees (see ADR-49)
    :param dec: Declination in degrees (see ADR-49)
    :param reference_time: reference_time,
    :param reference_frame: Specification of the reference frame or system for a set of pointing coordinates (see ADR-49)
    """

    ra: list = None
    dec: list = None
    reference_time: str = None
    reference_frame: str = None


@dataclass
class FieldConfiguration:
    """
    Class to hold Field configuration

    :param field_id: field_id
    :param pointing_fqdn: pointing_fqdn
    :param phase_dir: Phase direction
    """

    field_id: str = None
    pointing_fqdn: str = None
    phase_dir: PhaseDir = None


@dataclass
class EBScanTypeBeam:
    """
    Class to hold EBScanTypeBeam Configuration

    :param field_id: field_id
    :param channels_id: channels_id
    :param polarisations_id: polarisations_id
    """

    field_id: str = None
    channels_id: str = None
    polarisations_id: str = None


@dataclass
class EBScanType:
    """
    Class to hold EBScanType configuration

    :param scan_type_id: scan_type_id
    :param beams: Beam parameters for the purpose of the Science Data Processor.
    :param derive_from: derive_from
    """

    scan_type_id: str = None
    beams: dict[str, EBScanTypeBeam] = field(default_factory=dict)
    derive_from: str = None


@dataclass
class ExecutionBlockConfiguration:
    """
    Class to hold ExecutionBlock configuration

    :param eb_id: Execution block ID to associate with processing
    :param max_length: Hint about the maximum observation length to support by the SDP.
    :param context: Free-form information from OET, see ADR-54
    :param beams: Beam parameters for the purpose of the Science Data Processor.
    :param channels: Spectral windows per channel configuration.
    :param polarisations: Polarisation definition.
    :param fields: Fields / Targets
    :param scan_types: Scan types. Associates scans with per-beam fields & channel configurations
    """

    eb_id: str = None
    max_length: float = None
    context: dict = field(default_factory=dict)
    beams: list[BeamConfiguration] = field(default_factory=list)
    channels: list[ChannelConfiguration] = field(default_factory=list)
    polarisations: list[PolarisationConfiguration] = field(default_factory=list)
    fields: list[FieldConfiguration] = field(default_factory=list)
    scan_types: Optional[
        list[EBScanType]
    ] = None  # FIXME: `field(default_factory=list)`?


@dataclass
class SDPConfiguration:
    """
    Class to hold SDP Configuration

    :param eb_id: Execution block ID to associate with processing
    :param max_length: Hint about the maximum observation length to support by the SDP.
    :param scan_types: Scan types to be supported on subarray
    :param processing_blocks: A Processing Block is an atomic unit of data processing for the purpose of SDP’s internal scheduler
    :param execution_block: execution_block
    :param interface: url string to determine JsonSchema version
    :param resources: resources
    """

    eb_id: str = None
    max_length: float = None
    # FIXME: should probably be `field(default_factory=list)` not `None`
    scan_types: Optional[list[ScanType]] = None
    processing_blocks: list[ProcessingBlockConfiguration] = field(default_factory=list)
    execution_block: ExecutionBlockConfiguration = None
    # FIXME: should probably be `field(default_factory=dict)` not `None`
    resources: Optional[dict] = None
    interface: Optional[str] = None
