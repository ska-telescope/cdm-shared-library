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
    def __init__(
        self,
        channel=Channel(
            count=None,
            start=None,
            stride=None,
            freq_min=None,
            freq_max=None,
            link_map=None,
            spectral_window_id=None,
        ),
    ):
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
    def __init__(
        self,
        scan_type=ScanType(
            scan_type_id=None,
            reference_frame=None,
            ra=None,
            dec=None,
            channels=[Channel, Channel],
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
    def __init__(self, work=SDPWorkflow(name=None, kind=None, version=None)):
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
    def __init__(self, depend=PbDependency(pb_id=None, kind=None)):
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
    def __init__(self, script=ScriptConfiguration(kind=None, name=None, version=None)):
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
