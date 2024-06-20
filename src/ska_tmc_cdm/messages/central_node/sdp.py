"""
The messages module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
import math
from typing import Optional

from pydantic import Field

from ska_tmc_cdm.messages.base import CdmObject

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


class SDPWorkflow(CdmObject):
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


class Channel(CdmObject):
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
    stride: Optional[int] = None
    freq_min: float
    freq_max: float
    link_map: Optional[list[list]] = None
    spectral_window_id: Optional[str] = None


class ScanType(CdmObject):
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


class PbDependency(CdmObject):
    """
    Class to hold Dependencies for ProcessingBlock

    :param pb_id: Unique identifier for this processing block
    :param kind: The kind of processing script (realtime or batch)
    """

    pb_id: str
    kind: list[str]


class ScriptConfiguration(CdmObject):
    """
    Class to hold ScriptConfiguration

    :param name: The name of the processing script
    :param kind: The kind of processing script
    :param version: Version of the processing script
    """

    kind: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None


class ProcessingBlockConfiguration(CdmObject):
    """
    Class to hold ProcessingBlock configuration

    :param pb_id: Processing block ID
    :param workflow: Specification of the workflow to be executed along with configuration parameters for the workflow.
    :param parameters: Processing script parameters
    :param dependencies: Dependencies on other processing blocks
    :param sbi_ids: list of scheduling block ids
    :param script: Processing script description (dictionary for now)
    """

    pb_id: Optional[str] = None
    workflow: Optional[SDPWorkflow] = None
    # FIXME: should probably be `Field(default_factory=dict)` not `None`
    parameters: Optional[dict] = None
    # FIXME: should probably be `Field(default_factory=list)` not `None`
    dependencies: Optional[list[PbDependency]] = None
    # FIXME: should probably be `Field(default_factory=list)` not `None`
    sbi_ids: Optional[list[str]] = None
    script: Optional[ScriptConfiguration] = None


class BeamConfiguration(CdmObject):
    """
    Class to hold Dependencies for Beam Configuration

    :param beam_id: Name to identify the beam within the SDP configuration.
    :param function: Identifies the type and origin of the generated beam data.
    :param search_beam_id: search_beam_id
    :param timing_beam_id: timing_beam_id
    :param vlbi_beam_id: vlbi_beam_id
    """

    beam_id: Optional[str] = None
    function: Optional[str] = None
    search_beam_id: Optional[int] = None
    timing_beam_id: Optional[int] = None
    vlbi_beam_id: Optional[int] = None


class ChannelConfiguration(CdmObject):
    """
    Class to hold Dependencies for Channel Configuration

    :param channels_id: channels_id
    :param spectral_windows: spectral_windows
    """

    channels_id: Optional[str] = None
    spectral_windows: list[Channel] = Field(default_factory=list)


class PolarisationConfiguration(CdmObject):
    """
    Class to hold Dependencies for Polarisation Configuration

    :param polarisations_id: Polarisation definitions id
    :param corr_type: corr_type
    """

    polarisations_id: Optional[str] = None
    corr_type: list[str] = Field(default_factory=list)


class PhaseDir(CdmObject):
    """
    Class to hold PhaseDir configuration

    :param ra: Right Ascension in degrees (see ADR-49)
    :param dec: Declination in degrees (see ADR-49)
    :param reference_time: reference_time,
    :param reference_frame: Specification of the reference frame or system for a set of pointing coordinates (see ADR-49)
    """

    ra: Optional[list[float]] = None
    dec: Optional[list[float]] = None
    reference_time: Optional[str] = None
    reference_frame: Optional[str] = None

    @staticmethod
    def _floatlist_eq(list_a: list[float], list_b: list[float]) -> bool:
        tol = 1e-15
        return all((math.isclose(x, y, abs_tol=tol) for x, y in zip(list_a, list_b)))

    def __eq__(self, other):
        if not isinstance(other, PhaseDir):
            return False
        return (
            self.reference_frame == other.reference_frame
            and self.reference_time == other.reference_time
            and self._floatlist_eq(self.ra, other.ra)
            and self._floatlist_eq(self.dec, other.dec)
        )


class FieldConfiguration(CdmObject):
    """
    Class to hold Field configuration

    :param field_id: field_id
    :param pointing_fqdn: pointing_fqdn
    :param phase_dir: Phase direction
    """

    field_id: Optional[str] = None
    pointing_fqdn: Optional[str] = None
    phase_dir: Optional[PhaseDir] = None


class EBScanTypeBeam(CdmObject):
    """
    Class to hold EBScanTypeBeam Configuration

    :param field_id: field_id
    :param channels_id: channels_id
    :param polarisations_id: polarisations_id
    """

    field_id: Optional[str] = None
    channels_id: Optional[str] = None
    polarisations_id: Optional[str] = None


class EBScanType(CdmObject):
    """
    Class to hold EBScanType configuration

    :param scan_type_id: scan_type_id
    :param beams: Beam parameters for the purpose of the Science Data Processor.
    :param derive_from: derive_from
    """

    scan_type_id: Optional[str] = None
    beams: dict[str, EBScanTypeBeam] = Field(default_factory=dict)
    derive_from: Optional[str] = None


class ExecutionBlockConfiguration(CdmObject):
    """
    Class to hold ExecutionBlock configuration

    :param eb_id: Execution block ID to associate with processing
    :param max_length: Hint about the maximum observation length to support by the SDP.
    :param context: Free-form information from OET, see ADR-54
    :param beams: Beam parameters for the purpose of the Science Data Processor.
    :param channels: Spectral windows per channel configuration.
    :param polarisations: Polarisation definition.
    :param fields: fields / Targets
    :param scan_types: Scan types. Associates scans with per-beam fields & channel configurations
    """

    eb_id: Optional[str] = None
    max_length: Optional[float] = None
    context: dict = Field(default_factory=dict)
    # FIXME: should these all be `Field(default_factory=list)` instead of `None`?
    beams: Optional[list[BeamConfiguration]] = None
    channels: Optional[list[ChannelConfiguration]] = None
    polarisations: Optional[list[PolarisationConfiguration]] = None
    fields: Optional[list[FieldConfiguration]] = None
    scan_types: Optional[list[EBScanType]] = None


class SDPConfiguration(CdmObject):
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

    eb_id: Optional[str] = None
    max_length: Optional[float] = None
    # FIXME: should probably be `Field(default_factory=list)` not `None`
    scan_types: Optional[list[ScanType]] = None
    # FIXME: should probably be `Field(default_factory=list)` not `None`
    processing_blocks: Optional[list[ProcessingBlockConfiguration]] = None
    execution_block: Optional[ExecutionBlockConfiguration] = None
    # FIXME: should probably be `Field(default_factory=dict)` not `None`
    resources: Optional[dict] = None
    interface: Optional[str] = None
