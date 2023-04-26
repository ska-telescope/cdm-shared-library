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

"""
Create a sdp block using builder pattern
"""


class ChannelBuilder:
    """
    ChannelBuilder is a test data builder for CDM Channel objects.

    By default, ChannelBuilder will build an Channel

    for low observation command.
    """

    def __init__(self) -> object:
        self.channel = None

    def set_count(self, count):
        self.count = count
        return self

    def set_start(self, start):
        self.start = start
        return self

    def set_stride(self, stride):
        self.stride = stride
        return self

    def set_freq_min(self, freq_min):
        self.freq_min = freq_min
        return self

    def set_freq_max(self, freq_max):
        self.freq_max = freq_max
        return self

    def set_link_map(self, link_map):
        self.link_map = link_map
        return self

    def set_spectral_window_id(self, spectral_window_id):
        self.spectral_window_id = spectral_window_id
        return self

    def build(self):
        self.channel = Channel(
            self.count,
            self.start,
            self.stride,
            self.freq_min,
            self.freq_max,
            self.link_map,
        )
        return self.channel


class ScanTypeBuilder:
    """
    ScanTypeBuilder is a test data builder for CDM ScanType objects.

    By default, ScanTypeBuilder will build an ScanType

    for low observation command.
    """

    def __init__(self) -> object:
        self.scan_type = None

    def set_scan_type_id(self, scan_type_id):
        self.scan_type_id = scan_type_id
        return self

    def set_reference_frame(self, reference_frame):
        self.reference_frame = reference_frame
        return self

    def set_ra(self, ra):
        self.ra = ra
        return self

    def set_dec(self, dec):
        self.dec = dec
        return self

    def set_channels(self, channels):
        self.channels = channels
        return self

    def build(self):
        self.scan_type = ScanType(
            self.scan_type_id, self.reference_frame, self.ra, self.dec, self.channels
        )
        return self.scan_type


class SDPWorkflowBuilder:
    """
    SDPWorkflowBuilder is a test data builder for CDM SDPWorkflow objects.

    By default, SDPWorkflowBuilder will build an SDPWorkflow

    for low observation command.
    """

    def __init__(self) -> object:
        self.work = None

    def set_name(self, name):
        self.name = name
        return self

    def set_kind(self, kind):
        self.kind = kind
        return self

    def set_version(self, version):
        self.version = version
        return self

    def build(self):
        self.work = SDPWorkflow(self.name, self.kind, self.version)
        return self.work


class PbDependencyBuilder:
    """
    PbDependencyBuilder is a test data builder for CDM PbDependency objects.

    By default, PbDependencyBuilder will build an PbDependency

    for low observation command.
    """

    def __init__(self) -> object:
        self.depend = None

    def set_pb_id(self, pb_id):
        self.pb_id = pb_id
        return self

    def set_kind(self, kind):
        self.kind = kind
        return self

    def build(self):
        self.depend = PbDependency(self.pb_id, self.kind)
        return self.depend


class ScriptConfigurationBuilder:
    """
    ScriptConfigurationBuilder is a test data builder for CDM ScriptConfiguration objects.

    By default, ScriptConfigurationBuilder will build an ScriptConfiguration

    for low observation command.
    """

    def __init__(
        self,
    ) -> object:
        self.script = None

    def set_kind(self, kind):
        self.kind = kind
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_version(self, version):
        self.version = version
        return self

    def build(self):
        self.script = ScriptConfiguration(self.kind, self.name, self.version)
        return self.script


class ProcessingBlockConfigurationBuilder:
    """
    ProcessingBlockConfigurationBuilder is a test data builder for CDM ProcessingBlockConfiguration objects.

    By default, ProcessingBlockConfigurationBuilder will build an ProcessingBlockConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.process = None

    def set_pb_id(self, pb_id):
        self.pb_id = pb_id
        return self

    def set_workflow(self, workflow):
        self.workflow = workflow
        return self

    def set_parameters(self, parameters):
        self.parameters = parameters
        return self

    def set_dependencies(self, dependencies):
        self.dependencies = dependencies
        return self

    def set_sbi_ids(self, sbi_ids):
        self.sbi_ids = sbi_ids
        return self

    def set_script(self, script):
        self.script = script
        return self

    def build(self):
        self.process = ProcessingBlockConfiguration(
            self.pb_id,
            self.workflow,
            self.parameters,
            self.dependencies,
            self.sbi_ids,
            self.script,
        )
        return self.process


class SDPConfigurationBuilder:
    """
    SDPConfigurationBuilder is a test data builder for CDM SDPConfiguration objects.

    By default, SDPConfigurationBuilder will build an SDPConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.sdp = None

    def set_eb_id(self, eb_id):
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length):
        self.max_length = max_length
        return self

    def set_scan_types(self, scan_types):
        self.scan_types = scan_types
        return self

    def set_processing_blocks(self, processing_blocks):
        self.processing_blocks = processing_blocks
        return self

    def set_execution_block(self, execution_block):
        self.execution_block = execution_block
        return self

    def set_resources(self, resources):
        self.resources = resources
        return self

    def set_interface(self, interface):
        self.interface = interface
        return self

    def build(self):
        self.sdp = SDPConfiguration(
            self.eb_id,
            self.max_length,
            self.scan_types,
            self.processing_blocks,
            self.execution_block,
            self.resources,
            self.interface,
        )
        return self.sdp


class BeamConfigurationBuilder:
    """
    BeamConfigurationBuilder is a test data builder for CDM BeamConfiguration objects.

    By default, BeamConfigurationBuilder will build an BeamConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.beam = None

    def set_beam_id(self, beam_id):
        self.beam_id = beam_id
        return self

    def set_function(self, function):
        self.function = function
        return self

    def set_search_beam_id(self, search_beam_id):
        self.search_beam_id = search_beam_id
        return self

    def set_timing_beam_id(self, timing_beam_id):
        self.timing_beam_id = timing_beam_id
        return self

    def set_vlbi_beam_id(self, vlbi_beam_id):
        self.vlbi_beam_id = vlbi_beam_id
        return self

    def build(self):
        self.beam = BeamConfiguration(
            self.beam_id,
            self.function,
            self.search_beam_id,
            self.timing_beam_id,
            self.vlbi_beam_id,
        )
        return self.beam


class ChannelConfigurationBuilder:
    """
    ChannelConfigurationBuilder is a test data builder for CDM ChannelConfiguration objects.

    By default, ChannelConfigurationBuilder will build an ChannelConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.channel_conf = None

    def set_channels_id(self, channels_id):
        self.channels_id = channels_id
        return self

    def set_spectral_windows(self, spectral_windows):
        self.spectral_windows = spectral_windows
        return self

    def build(self):
        self.channel_conf = ChannelConfiguration(
            self.channels_id, self.spectral_windows
        )
        return self.channel_conf


class PolarisationConfigurationBuilder:
    """
    PolarisationConfigurationBuilder is a test data builder for CDM PolarisationConfiguration objects.

    By default, PolarisationConfigurationBuilder will build an PolarisationConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.polar = None

    def set_polarisations_id(self, polarisations_id):
        self.polarisations_id = polarisations_id
        return self

    def set_corr_type(self, corr_type):
        self.corr_type = corr_type
        return self

    def build(self):
        self.polar = PolarisationConfiguration(self.polarisations_id, self.corr_type)
        return self.polar


class PhaseDirBuilder:
    """
    PhaseDirBuilder is a test data builder for CDM PhaseDir objects.

    By default, PhaseDirBuilder will build an PhaseDir

    for low observation command.
    """

    def __init__(self) -> object:
        self.phase = None

    def set_ra(self, ra):
        self.ra = ra
        return self

    def set_dec(self, dec):
        self.dec = dec
        return self

    def set_reference_time(self, reference_time):
        self.reference_time = reference_time
        return self

    def set_reference_frame(self, reference_frame):
        self.reference_frame = reference_frame
        return self

    def build(self):
        self.phase = PhaseDir(
            self.ra, self.dec, self.reference_time, self.reference_frame
        )
        return self.phase


class FieldConfigurationBuilder:
    """
    FieldConfigurationBuilder is a test data builder for CDM FieldConfiguration objects.

    By default, FieldConfigurationBuilder will build an FieldConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.field = None

    def set_field_id(self, field_id):
        self.field_id = field_id
        return self

    def set_pointing_fqdn(self, pointing_fqdn):
        self.pointing_fqdn = pointing_fqdn
        return self

    def set_phase_dir(self, phase_dir):
        self.phase_dir = phase_dir
        return self

    def build(self):
        self.field = FieldConfiguration(
            self.field_id, self.pointing_fqdn, self.phase_dir
        )
        return self.field


class EBScanTypeBuilder:
    """
    EBScanTypeBuilder is a test data builder for CDM EBScanType objects.

    By default, EBScanTypeBuilder will build an EBScanType

    for low observation command.
    """

    def __init__(self) -> object:
        self.ebscan = None

    def set_scan_type_id(self, scan_type_id):
        self.scan_type_id = scan_type_id
        return self

    def set_beams(self, beams):
        self.beams = beams
        return self

    def set_derive_from(self, derive_from):
        self.derive_from = derive_from
        return self

    def build(self):
        self.ebscan = EBScanType(self.scan_type_id, self.beams, self.derive_from)
        return self.ebscan


class EBScanTypeBeamBuilder:
    """
    EBScanTypeBeamBuilder is a test data builder for CDM EBScanTypeBeam objects.

    By default, EBScanTypeBeamBuilder will build an EBScanTypeBeam

    for low observation command.
    """

    def __init__(self) -> object:
        self.ebscan_type = None

    def set_field_id(self, field_id):
        self.field_id = field_id
        return self

    def set_channels_id(self, channels_id):
        self.channels_id = channels_id
        return self

    def set_polarisations_id(self, polarisations_id):
        self.polarisations_id = polarisations_id
        return self

    def build(self):
        self.ebscan_type = EBScanTypeBeam(
            self.field_id, self.channels_id, self.polarisations_id
        )
        return self.ebscan_type


class ExecutionBlockConfigurationBuilder:
    """
    ExecutionBlockConfigurationBuilder is a test data builder for CDM ExecutionBlockConfiguration objects.

    By default, ExecutionBlockConfigurationBuilder will build an ExecutionBlockConfiguration

    for low observation command.
    """

    def __init__(self) -> object:
        self.execution = None

    def set_eb_id(self, eb_id):
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length):
        self.max_length = max_length
        return self

    def set_context(self, context):
        self.context = context
        return self

    def set_beams(self, beams):
        self.beams = beams
        return self

    def set_channels(self, channels):
        self.channels = channels
        return self

    def set_polarisations(self, polarisations):
        self.polarisations = polarisations
        return self

    def set_fields(self, fields):
        self.fields = fields
        return self

    def set_scan_types(self, scan_types):
        self.scan_types = scan_types
        return self

    def build(self):
        self.execution = ExecutionBlockConfiguration(
            self.eb_id,
            self.max_length,
            self.context,
            self.beams,
            self.channels,
            self.polarisations,
            self.fields,
            self.scan_types,
        )
        return self.execution
