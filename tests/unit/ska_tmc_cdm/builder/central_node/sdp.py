from typing import List

from ska_tmc_cdm.messages.central_node.sdp import (
    BeamConfiguration,
    Channel,
    ChannelConfiguration,
    EBScanType,
    EBScanTypeBeam,
    ExecutionBlockConfiguration,
    FieldConfiguration,
    PbDependency,
    PhaseDir,
    PolarisationConfiguration,
    ProcessingBlockConfiguration,
    ScanType,
    ScriptConfiguration,
    SDPConfiguration,
    SDPWorkflow,
)


class ChannelBuilder:
    """
    ChannelBuilder is a test data builder for CDM Channel objects.

    By default, ChannelBuilder will build an Channel

    for low observation command.
    """

    def __init__(self) -> "ChannelBuilder":
        self.count = None
        self.start = None
        self.stride = None
        self.freq_min = None
        self.freq_max = None
        self.link_map = None
        self.spectral_window_id = None

    def set_count(self, count: int) -> "ChannelBuilder":
        self.count = count
        return self

    def set_start(self, start: int) -> "ChannelBuilder":
        self.start = start
        return self

    def set_stride(self, stride: int) -> "ChannelBuilder":
        self.stride = stride
        return self

    def set_freq_min(self, freq_min: float) -> "ChannelBuilder":
        self.freq_min = freq_min
        return self

    def set_freq_max(self, freq_max: float) -> "ChannelBuilder":
        self.freq_max = freq_max
        return self

    def set_link_map(self, link_map: list) -> "ChannelBuilder":
        self.link_map = link_map
        return self

    def set_spectral_window_id(self, spectral_window_id: str) -> "ChannelBuilder":
        self.spectral_window_id = spectral_window_id
        return self

    def build(self) -> Channel:
        return Channel(
            self.count,
            self.start,
            self.stride,
            self.freq_min,
            self.freq_max,
            self.link_map,
            self.spectral_window_id,
        )


class ScanTypeBuilder:
    """
    ScanTypeBuilder is a test data builder for CDM ScanType objects.

    By default, ScanTypeBuilder will build an ScanType

    for low observation command.
    """

    def __init__(self) -> "ScanTypeBuilder":
        self.scan_type_id = None
        self.reference_frame = None
        self.ra = None
        self.dec = None
        self.channels = None

    def set_scan_type_id(self, scan_type_id: str) -> "ScanTypeBuilder":
        self.scan_type_id = scan_type_id
        return self

    def set_reference_frame(self, reference_frame: str) -> "ScanTypeBuilder":
        self.reference_frame = reference_frame
        return self

    def set_ra(self, ra: str) -> "ScanTypeBuilder":
        self.ra = ra
        return self

    def set_dec(self, dec: str) -> "ScanTypeBuilder":
        self.dec = dec
        return self

    def set_channels(self, channels: list) -> "ScanTypeBuilder":
        self.channels = channels
        return self

    def build(self) -> ScanType:
        return ScanType(
            self.scan_type_id, self.reference_frame, self.ra, self.dec, self.channels
        )


class SDPWorkflowBuilder:
    """
    SDPWorkflowBuilder is a test data builder for CDM SDPWorkflow objects.

    By default, SDPWorkflowBuilder will build an SDPWorkflow

    for low observation command.
    """

    def __init__(self) -> "SDPWorkflowBuilder":
        self.name = None
        self.kind = None
        self.version = None

    def set_name(self, name: str) -> "SDPWorkflowBuilder":
        self.name = name
        return self

    def set_kind(self, kind: str) -> "SDPWorkflowBuilder":
        self.kind = kind
        return self

    def set_version(self, version: str) -> "SDPWorkflowBuilder":
        self.version = version
        return self

    def build(self) -> SDPWorkflow:
        return SDPWorkflow(self.name, self.kind, self.version)


class PbDependencyBuilder:
    """
    PbDependencyBuilder is a test data builder for CDM PbDependency objects.

    By default, PbDependencyBuilder will build an PbDependency

    for low observation command.
    """

    def __init__(self) -> "PbDependencyBuilder":
        self.pb_id = None
        self.kind = None

    def set_pb_id(self, pb_id: str) -> "PbDependencyBuilder":
        self.pb_id = pb_id
        return self

    def set_kind(self, kind: list) -> "PbDependencyBuilder":
        self.kind = kind
        return self

    def build(self) -> PbDependency:
        return PbDependency(self.pb_id, self.kind)


class ScriptConfigurationBuilder:
    """
    ScriptConfigurationBuilder is a test data builder for CDM ScriptConfiguration objects.

    By default, ScriptConfigurationBuilder will build an ScriptConfiguration

    for low observation command.
    """

    def __init__(self) -> "ScriptConfigurationBuilder":
        self.kind = None
        self.name = None
        self.version = None

    def set_kind(self, kind: str) -> "ScriptConfigurationBuilder":
        self.kind = kind
        return self

    def set_name(self, name: str) -> "ScriptConfigurationBuilder":
        self.name = name
        return self

    def set_version(self, version: str) -> "ScriptConfigurationBuilder":
        self.version = version
        return self

    def build(self) -> ScriptConfiguration:
        return ScriptConfiguration(self.kind, self.name, self.version)


class ProcessingBlockConfigurationBuilder:
    """
    ProcessingBlockConfigurationBuilder is a test data builder for CDM ProcessingBlockConfiguration objects.

    By default, ProcessingBlockConfigurationBuilder will build an ProcessingBlockConfiguration

    for low observation command.
    """

    def __init__(self) -> "ProcessingBlockConfigurationBuilder":
        self.pb_id = None
        self.workflow = None
        self.parameters = {}
        self.dependencies = None
        self.sbi_ids = None
        self.script = None

    def set_pb_id(self, pb_id: str) -> "ProcessingBlockConfigurationBuilder":
        self.pb_id = pb_id
        return self

    def set_workflow(
        self, workflow: SDPWorkflow
    ) -> "ProcessingBlockConfigurationBuilder":
        self.workflow = workflow
        return self

    def set_parameters(self, parameters: dict) -> "ProcessingBlockConfigurationBuilder":
        self.parameters = parameters
        return self

    def set_dependencies(
        self, dependencies: List[PbDependency]
    ) -> "ProcessingBlockConfigurationBuilder":
        self.dependencies = dependencies
        return self

    def set_sbi_ids(self, sbi_ids: list) -> "ProcessingBlockConfigurationBuilder":
        self.sbi_ids = sbi_ids
        return self

    def set_script(
        self, script: ScriptConfiguration
    ) -> "ProcessingBlockConfigurationBuilder":
        self.script = script
        return self

    def build(self) -> ProcessingBlockConfiguration:
        return ProcessingBlockConfiguration(
            self.pb_id,
            self.workflow,
            self.parameters,
            self.dependencies,
            self.sbi_ids,
            self.script,
        )


class SDPConfigurationBuilder:
    """
    SDPConfigurationBuilder is a test data builder for CDM SDPConfiguration objects.

    By default, SDPConfigurationBuilder will build an SDPConfiguration

    for low observation command.
    """

    def __init__(self) -> "SDPConfigurationBuilder":
        self.eb_id = None
        self.max_length = None
        self.scan_types = None
        self.processing_blocks = None
        self.execution_block = None
        self.resources = None
        self.interface = None

    def set_eb_id(self, eb_id: str) -> "SDPConfigurationBuilder":
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length: float) -> "SDPConfigurationBuilder":
        self.max_length = max_length
        return self

    def set_scan_types(self, scan_types: list) -> "SDPConfigurationBuilder":
        self.scan_types = scan_types
        return self

    def set_processing_blocks(
        self, processing_blocks: List[ProcessingBlockConfiguration]
    ) -> "SDPConfigurationBuilder":
        self.processing_blocks = processing_blocks
        return self

    def set_execution_block(
        self, execution_block: ExecutionBlockConfiguration
    ) -> "SDPConfigurationBuilder":
        self.execution_block = execution_block
        return self

    def set_resources(self, resources: dict) -> "SDPConfigurationBuilder":
        self.resources = resources
        return self

    def set_interface(self, interface: str) -> "SDPConfigurationBuilder":
        self.interface = interface
        return self

    def build(self) -> SDPConfiguration:
        return SDPConfiguration(
            self.eb_id,
            self.max_length,
            self.scan_types,
            self.processing_blocks,
            self.execution_block,
            self.resources,
            self.interface,
        )


class BeamConfigurationBuilder:
    """
    BeamConfigurationBuilder is a test data builder for CDM BeamConfiguration objects.

    By default, BeamConfigurationBuilder will build an BeamConfiguration

    for low observation command.
    """

    def __init__(self) -> "BeamConfigurationBuilder":
        self.beam_id = None
        self.function = None
        self.search_beam_id = None
        self.timing_beam_id = None
        self.vlbi_beam_id = None

    def set_beam_id(self, beam_id: str) -> "BeamConfigurationBuilder":
        self.beam_id = beam_id
        return self

    def set_function(self, function: str) -> "BeamConfigurationBuilder":
        self.function = function
        return self

    def set_search_beam_id(self, search_beam_id: int) -> "BeamConfigurationBuilder":
        self.search_beam_id = search_beam_id
        return self

    def set_timing_beam_id(self, timing_beam_id: int) -> "BeamConfigurationBuilder":
        self.timing_beam_id = timing_beam_id
        return self

    def set_vlbi_beam_id(self, vlbi_beam_id: int) -> "BeamConfigurationBuilder":
        self.vlbi_beam_id = vlbi_beam_id
        return self

    def build(self) -> BeamConfiguration:
        return BeamConfiguration(
            self.beam_id,
            self.function,
            self.search_beam_id,
            self.timing_beam_id,
            self.vlbi_beam_id,
        )


class ChannelConfigurationBuilder:
    """
    ChannelConfigurationBuilder is a test data builder for CDM ChannelConfiguration objects.

    By default, ChannelConfigurationBuilder will build an ChannelConfiguration

    for low observation command.
    """

    def __init__(self) -> "ChannelConfigurationBuilder":
        self.channels_id = None
        self.spectral_windows = None

    def set_channels_id(self, channels_id: str) -> "ChannelConfigurationBuilder":
        self.channels_id = channels_id
        return self

    def set_spectral_windows(
        self, spectral_windows: list
    ) -> "ChannelConfigurationBuilder":
        self.spectral_windows = spectral_windows
        return self

    def build(self) -> ChannelConfiguration:
        return ChannelConfiguration(self.channels_id, self.spectral_windows)


class PolarisationConfigurationBuilder:
    """
    PolarisationConfigurationBuilder is a test data builder for CDM PolarisationConfiguration objects.

    By default, PolarisationConfigurationBuilder will build an PolarisationConfiguration

    for low observation command.
    """

    def __init__(self) -> "PolarisationConfigurationBuilder":
        self.polarisations_id = None
        self.corr_type = None

    def set_polarisations_id(
        self, polarisations_id: str
    ) -> "PolarisationConfigurationBuilder":
        self.polarisations_id = polarisations_id
        return self

    def set_corr_type(self, corr_type: list) -> "PolarisationConfigurationBuilder":
        self.corr_type = corr_type
        return self

    def build(self) -> PolarisationConfiguration:
        return PolarisationConfiguration(self.polarisations_id, self.corr_type)


class PhaseDirBuilder:
    """
    PhaseDirBuilder is a test data builder for CDM PhaseDir objects.

    By default, PhaseDirBuilder will build an PhaseDir

    for low observation command.
    """

    def __init__(self) -> "PhaseDirBuilder":
        self.ra = None
        self.dec = None
        self.reference_time = None
        self.reference_frame = None

    def set_ra(self, ra: list) -> "PhaseDirBuilder":
        self.ra = ra
        return self

    def set_dec(self, dec: list) -> "PhaseDirBuilder":
        self.dec = dec
        return self

    def set_reference_time(self, reference_time: str) -> "PhaseDirBuilder":
        self.reference_time = reference_time
        return self

    def set_reference_frame(self, reference_frame: str) -> "PhaseDirBuilder":
        self.reference_frame = reference_frame
        return self

    def build(self) -> PhaseDir:
        return PhaseDir(self.ra, self.dec, self.reference_time, self.reference_frame)


class FieldConfigurationBuilder:
    """
    FieldConfigurationBuilder is a test data builder for CDM FieldConfiguration objects.

    By default, FieldConfigurationBuilder will build an FieldConfiguration

    for low observation command.
    """

    def __init__(self) -> "FieldConfigurationBuilder":
        self.field_id = None
        self.pointing_fqdn = None
        self.phase_dir = None

    def set_field_id(self, field_id: str) -> "FieldConfigurationBuilder":
        self.field_id = field_id
        return self

    def set_pointing_fqdn(self, pointing_fqdn: str) -> "FieldConfigurationBuilder":
        self.pointing_fqdn = pointing_fqdn
        return self

    def set_phase_dir(self, phase_dir: PhaseDir) -> "FieldConfigurationBuilder":
        self.phase_dir = phase_dir
        return self

    def build(self) -> FieldConfiguration:
        return FieldConfiguration(self.field_id, self.pointing_fqdn, self.phase_dir)


class EBScanTypeBuilder:
    """
    EBScanTypeBuilder is a test data builder for CDM EBScanType objects.

    By default, EBScanTypeBuilder will build an EBScanType

    for low observation command.
    """

    def __init__(self) -> "EBScanTypeBuilder":
        self.scan_type_id = None
        self.beams = None
        self.derive_from = None

    def set_scan_type_id(self, scan_type_id: str) -> "EBScanTypeBuilder":
        self.scan_type_id = scan_type_id
        return self

    def set_beams(self, beams: dict) -> "EBScanTypeBuilder":
        self.beams = beams
        return self

    def set_derive_from(self, derive_from: str) -> "EBScanTypeBuilder":
        self.derive_from = derive_from
        return self

    def build(self) -> EBScanType:
        return EBScanType(self.scan_type_id, self.beams, self.derive_from)


class EBScanTypeBeamBuilder:
    """
    EBScanTypeBeamBuilder is a test data builder for CDM EBScanTypeBeam objects.

    By default, EBScanTypeBeamBuilder will build an EBScanTypeBeam

    for low observation command.
    """

    def __init__(self) -> "EBScanTypeBeamBuilder":
        self.field_id = None
        self.channels_id = None
        self.polarisations_id = None

    def set_field_id(self, field_id: str) -> "EBScanTypeBeamBuilder":
        self.field_id = field_id
        return self

    def set_channels_id(self, channels_id: str) -> "EBScanTypeBeamBuilder":
        self.channels_id = channels_id
        return self

    def set_polarisations_id(self, polarisations_id: str) -> "EBScanTypeBeamBuilder":
        self.polarisations_id = polarisations_id
        return self

    def build(self) -> EBScanTypeBeam:
        return EBScanTypeBeam(self.field_id, self.channels_id, self.polarisations_id)


class ExecutionBlockConfigurationBuilder:
    """
    ExecutionBlockConfigurationBuilder is a test data builder for CDM ExecutionBlockConfiguration objects.

    By default, ExecutionBlockConfigurationBuilder will build an ExecutionBlockConfiguration

    for low observation command.
    """

    def __init__(self) -> "ExecutionBlockConfigurationBuilder":
        self.eb_id = None
        self.max_length = None
        self.context = {}
        self.beams = None
        self.channels = None
        self.polarisations = None
        self.fields = None
        self.scan_types = None

    def set_eb_id(self, eb_id: str) -> "ExecutionBlockConfigurationBuilder":
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length: float):
        self.max_length = max_length
        return self

    def set_context(self, context: dict) -> "ExecutionBlockConfigurationBuilder":
        self.context = context
        return self

    def set_beams(self, beams: list) -> "ExecutionBlockConfigurationBuilder":
        self.beams = beams
        return self

    def set_channels(self, channels: list) -> "ExecutionBlockConfigurationBuilder":
        self.channels = channels
        return self

    def set_polarisations(
        self, polarisations: list
    ) -> "ExecutionBlockConfigurationBuilder":
        self.polarisations = polarisations
        return self

    def set_fields(self, fields: list) -> "ExecutionBlockConfigurationBuilder":
        self.fields = fields
        return self

    def set_scan_types(self, scan_types: list) -> "ExecutionBlockConfigurationBuilder":
        self.scan_types = scan_types
        return self

    def build(self) -> ExecutionBlockConfiguration:
        return ExecutionBlockConfiguration(
            self.eb_id,
            self.max_length,
            self.context,
            self.beams,
            self.channels,
            self.polarisations,
            self.fields,
            self.scan_types,
        )
