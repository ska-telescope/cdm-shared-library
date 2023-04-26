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

    def __init__(
        self,
        channel=Channel(
            count=int,
            start=int,
            stride=int,
            freq_min=float,
            freq_max=float,
            link_map=list(list()),
        ),
    ) -> object:
        self.channel = channel

    def set_count(self, count):
        self.channel.count = count
        return self

    def set_start(self, start):
        self.channel.start = start
        return self

    def set_stride(self, stride):
        self.channel.stride = stride
        return self

    def set_freq_min(self, freq_min):
        self.channel.freq_min = freq_min
        return self

    def set_freq_max(self, freq_max):
        self.channel.freq_max = freq_max
        return self

    def set_link_map(self, link_map):
        self.channel.link_map = link_map
        return self

    def set_spectral_window_id(self, spectral_window_id):
        self.channel.spectral_window_id = spectral_window_id
        return self

    def build(self):
        return self.channel


class ScanTypeBuilder:
    """
    ScanTypeBuilder is a test data builder for CDM ScanType objects.

    By default, ScanTypeBuilder will build an ScanType

    for low observation command.
    """

    def __init__(
        self,
        scan_type=ScanType(
            scan_type_id=int, reference_frame=str, ra=str, dec=str, channels=list()
        ),
    ):
        self.scan_type = scan_type

    def set_scan_type_id(self, scan_type_id):
        self.scan_type.scan_type_id = scan_type_id
        return self

    def set_reference_frame(self, reference_frame):
        self.scan_type.reference_frame = reference_frame
        return self

    def set_ra(self, ra):
        self.scan_type.ra = ra
        return self

    def set_dec(self, dec):
        self.scan_type.dec = dec
        return self

    def set_channels(self, channels):
        self.scan_type.channels = channels
        return self

    def build(self):
        return self.scan_type


class SDPWorkflowBuilder:
    """
    SDPWorkflowBuilder is a test data builder for CDM SDPWorkflow objects.

    By default, SDPWorkflowBuilder will build an SDPWorkflow

    for low observation command.
    """

    def __init__(self, work=SDPWorkflow(name=str, kind=str, version=str)):
        self.work = work

    def set_name(self, name):
        self.work.name = name
        return self

    def set_kind(self, kind):
        self.work.kind = kind
        return self

    def set_version(self, version):
        self.work.version = version
        return self

    def build(self):
        return self.work


class PbDependencyBuilder:
    """
    PbDependencyBuilder is a test data builder for CDM PbDependency objects.

    By default, PbDependencyBuilder will build an PbDependency

    for low observation command.
    """

    def __init__(self, depend=PbDependency(pb_id=str, kind=list())):
        self.depend = depend

    def set_pb_id(self, pb_id):
        self.depend.pb_id = pb_id
        return self

    def set_kind(self, kind):
        self.depend.kind = kind
        return self

    def build(self):
        return self.depend


class ScriptConfigurationBuilder:
    """
    ScriptConfigurationBuilder is a test data builder for CDM ScriptConfiguration objects.

    By default, ScriptConfigurationBuilder will build an ScriptConfiguration

    for low observation command.
    """

    def __init__(self, script=ScriptConfiguration()) -> object:
        self.script = script

    def set_kind(self, kind):
        self.script.kind = kind
        return self

    def set_name(self, name):
        self.script.name = name
        return self

    def set_version(self, version):
        self.script.version = version
        return self

    def build(self):
        return self.script


class ProcessingBlockConfigurationBuilder:
    """
    ProcessingBlockConfigurationBuilder is a test data builder for CDM ProcessingBlockConfiguration objects.

    By default, ProcessingBlockConfigurationBuilder will build an ProcessingBlockConfiguration

    for low observation command.
    """

    def __init__(self, process=ProcessingBlockConfiguration()):
        self.process = process

    def set_pb_id(self, pb_id):
        self.process.pb_id = pb_id
        return self

    def set_workflow(self, workflow):
        self.process.workflow = workflow
        return self

    def set_parameters(self, parameters):
        self.process.parameters = parameters
        return self

    def set_dependencies(self, dependencies):
        self.process.dependencies = dependencies
        return self

    def set_sbi_ids(self, sbi_ids):
        self.process.sbi_ids = sbi_ids
        return self

    def set_script(self, script):
        self.process.script = script
        return self

    def build(self):
        return self.process


class SDPConfigurationBuilder:
    """
    SDPConfigurationBuilder is a test data builder for CDM SDPConfiguration objects.

    By default, SDPConfigurationBuilder will build an SDPConfiguration

    for low observation command.
    """

    def __init__(self, sdp=SDPConfiguration()):
        self.sdp = sdp

    def set_eb_id(self, eb_id):
        self.sdp.eb_id = eb_id
        return self

    def set_max_length(self, max_length):
        self.sdp.max_length = max_length
        return self

    def set_scan_types(self, scan_types):
        self.sdp.scan_types = scan_types
        return self

    def set_processing_blocks(self, processing_blocks):
        self.sdp.processing_blocks = processing_blocks
        return self

    def set_execution_block(self, execution_block):
        self.sdp.execution_block = execution_block
        return self

    def set_resources(self, resources):
        self.sdp.resources = resources
        return self

    def set_interface(self, interface):
        self.sdp.interface = interface
        return self

    def build(self):
        return self.sdp


class BeamConfigurationBuilder:
    """
    BeamConfigurationBuilder is a test data builder for CDM BeamConfiguration objects.

    By default, BeamConfigurationBuilder will build an BeamConfiguration

    for low observation command.
    """

    def __init__(self, beam=BeamConfiguration()):
        self.beam = beam

    def set_beam_id(self, beam_id):
        self.beam.beam_id = beam_id
        return self

    def set_function(self, function):
        self.beam.function = function
        return self

    def set_search_beam_id(self, search_beam_id):
        self.beam.search_beam_id = search_beam_id
        return self

    def set_timing_beam_id(self, timing_beam_id):
        self.beam.timing_beam_id = timing_beam_id
        return self

    def set_vlbi_beam_id(self, vlbi_beam_id):
        self.beam.vlbi_beam_id = vlbi_beam_id
        return self

    def build(self):
        return self.beam


class ChannelConfigurationBuilder:
    """
    ChannelConfigurationBuilder is a test data builder for CDM ChannelConfiguration objects.

    By default, ChannelConfigurationBuilder will build an ChannelConfiguration

    for low observation command.
    """

    def __init__(self, channel_conf=ChannelConfiguration()):
        self.channel_conf = channel_conf

    def set_channels_id(self, channels_id):
        self.channel_conf.channels_id = channels_id
        return self

    def set_spectral_windows(self, spectral_windows):
        self.channel_conf.spectral_windows = spectral_windows
        return self

    def build(self):
        return self.channel_conf


class PolarisationConfigurationBuilder:
    """
    PolarisationConfigurationBuilder is a test data builder for CDM PolarisationConfiguration objects.

    By default, PolarisationConfigurationBuilder will build an PolarisationConfiguration

    for low observation command.
    """

    def __init__(self, polar=PolarisationConfiguration()):
        self.polar = polar

    def set_polarisations_id(self, polarisations_id):
        self.polar.polarisations_id = polarisations_id
        return self

    def set_corr_type(self, corr_type):
        self.polar.corr_type = corr_type
        return self

    def build(self):
        return self.polar


class PhaseDirBuilder:
    """
    PhaseDirBuilder is a test data builder for CDM PhaseDir objects.

    By default, PhaseDirBuilder will build an PhaseDir

    for low observation command.
    """

    def __init__(self, phase=PhaseDir()):
        self.phase = phase

    def set_ra(self, ra):
        self.phase.ra = ra
        return self

    def set_dec(self, dec):
        self.phase.dec = dec
        return self

    def set_reference_time(self, reference_time):
        self.phase.reference_time = reference_time
        return self

    def set_reference_frame(self, reference_frame):
        self.phase.reference_frame = reference_frame
        return self

    def build(self):
        return self.phase


class FieldConfigurationBuilder:
    """
    FieldConfigurationBuilder is a test data builder for CDM FieldConfiguration objects.

    By default, FieldConfigurationBuilder will build an FieldConfiguration

    for low observation command.
    """

    def __init__(self, field=FieldConfiguration()):
        self.field = field

    def set_field_id(self, field_id):
        self.field.field_id = field_id
        return self

    def set_pointing_fqdn(self, pointing_fqdn):
        self.field.pointing_fqdn = pointing_fqdn
        return self

    def set_phase_dir(self, phase_dir):
        self.field.phase_dir = phase_dir
        return self

    def build(self):
        return self.field


class EBScanTypeBuilder:
    """
    EBScanTypeBuilder is a test data builder for CDM EBScanType objects.

    By default, EBScanTypeBuilder will build an EBScanType

    for low observation command.
    """

    def __init__(self, ebscan=EBScanType()):
        self.ebscan = ebscan

    def set_scan_type_id(self, scan_type_id):
        self.ebscan.scan_type_id = scan_type_id
        return self

    def set_beams(self, beams):
        self.ebscan.beams = beams
        return self

    def set_derive_from(self, derive_from):
        self.ebscan.derive_from = derive_from
        return self

    def build(self):
        return self.ebscan


class EBScanTypeBeamBuilder:
    """
    EBScanTypeBeamBuilder is a test data builder for CDM EBScanTypeBeam objects.

    By default, EBScanTypeBeamBuilder will build an EBScanTypeBeam

    for low observation command.
    """

    def __init__(self, ebscan_type=EBScanTypeBeam()):
        self.ebscan_type = ebscan_type

    def set_field_id(self, field_id):
        self.ebscan_type.field_id = field_id
        return self

    def set_channels_id(self, channels_id):
        self.ebscan_type.channels_id = channels_id
        return self

    def set_polarisations_id(self, polarisations_id):
        self.ebscan_type.polarisations_id = polarisations_id
        return self

    def build(self):
        return self.ebscan_type


class ExecutionBlockConfigurationBuilder:
    """
    ExecutionBlockConfigurationBuilder is a test data builder for CDM ExecutionBlockConfiguration objects.

    By default, ExecutionBlockConfigurationBuilder will build an ExecutionBlockConfiguration

    for low observation command.
    """

    def __init__(self, execution=ExecutionBlockConfiguration()):
        self.execution = execution

    def set_eb_id(self, eb_id):
        self.execution.eb_id = eb_id
        return self

    def set_max_length(self, max_length):
        self.execution.max_length = max_length
        return self

    def set_context(self, context):
        self.execution.context = context
        return self

    def set_beams(self, beams):
        self.execution.beams = beams
        return self

    def set_channels(self, channels):
        self.execution.channels = channels
        return self

    def set_polarisations(self, polarisations):
        self.execution.polarisations = polarisations
        return self

    def set_fields(self, fields):
        self.execution.fields = fields
        return self

    def set_scan_types(self, scan_types):
        self.execution.scan_types = scan_types
        return self

    def build(self):
        return self.execution
