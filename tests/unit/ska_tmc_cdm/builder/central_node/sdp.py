import functools
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

ChannelBuilder = functools.partial(
    Channel,
    count=744,
    start=0,
    stride=2,
    freq_min=0.35e9,
    freq_max=1.05e9,
    link_map=((0, 0), (200, 1), (744, 2), (944, 3)),
    spectral_window_id="fsp_2_channels",
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
        """
        Set the scan type id
        :param scan_type_id: Scan type id
        """
        self.scan_type_id = scan_type_id
        return self

    def set_reference_frame(self, reference_frame: str) -> "ScanTypeBuilder":
        """
        Set the reference frame
        :param reference_frame: Reference frame
        """
        self.reference_frame = reference_frame
        return self

    def set_ra(self, ra: str) -> "ScanTypeBuilder":
        """
        Set the right ascension
        :param ra: Right ascension
        """
        self.ra = ra
        return self

    def set_dec(self, dec: str) -> "ScanTypeBuilder":
        """
        Set the declination
        :param dec: Declination
        """
        self.dec = dec
        return self

    def set_channels(self, channels: list) -> "ScanTypeBuilder":
        """
        Set the channels
        :param channels: Channels
        """
        self.channels = channels
        return self

    def build(self) -> ScanType:
        """
        Build or create CDM ScanType object
        :return: CDM ScanType object
        """
        return ScanType(
            scan_type_id=self.scan_type_id,
            reference_frame=self.reference_frame,
            ra=self.ra,
            dec=self.dec,
            channels=self.channels,
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
        """
        Set the name
        :param name: Name
        """
        self.name = name
        return self

    def set_kind(self, kind: str) -> "SDPWorkflowBuilder":
        """
        Set the kind
        :param kind: Kind
        """
        self.kind = kind
        return self

    def set_version(self, version: str) -> "SDPWorkflowBuilder":
        """
        Set the version
        :param version: Version
        """
        self.version = version
        return self

    def build(self) -> SDPWorkflow:
        """
        Build or create CDM SDPWorkflow object
        :return: CDM SDPWorkflow object
        """
        return SDPWorkflow(
            name=self.name, kind=self.kind, version=self.version
        )


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
        """
        Set the pb id
        :param pb_id: PB id
        """
        self.pb_id = pb_id
        return self

    def set_kind(self, kind: list) -> "PbDependencyBuilder":
        """
        Set the kind
        :param kind: Kind
        """
        self.kind = kind
        return self

    def build(self) -> PbDependency:
        """
        Build or create CDM PbDependency object
        :return: CDM PbDependency object
        """
        return PbDependency(pb_id=self.pb_id, kind=self.kind)


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
        """
        Set the kind
        :param kind: Kind
        """
        self.kind = kind
        return self

    def set_name(self, name: str) -> "ScriptConfigurationBuilder":
        """
        Set the name
        :param name: Name
        """
        self.name = name
        return self

    def set_version(self, version: str) -> "ScriptConfigurationBuilder":
        """
        Set the version
        :param version: Version
        """
        self.version = version
        return self

    def build(self) -> ScriptConfiguration:
        """
        Build or create CDM ScriptConfiguration object
        :return: CDM ScriptConfiguration object
        """
        return ScriptConfiguration(
            kind=self.kind, name=self.name, version=self.version
        )


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
        """
        Set the pb id
        :param pb_id: PB id
        """
        self.pb_id = pb_id
        return self

    def set_workflow(
        self, workflow: SDPWorkflow
    ) -> "ProcessingBlockConfigurationBuilder":
        """
        Set the workflow
        :param workflow: Workflow
        """
        self.workflow = workflow
        return self

    def set_parameters(
        self, parameters: dict
    ) -> "ProcessingBlockConfigurationBuilder":
        """
        Set the parameters
        :param parameters: Parameters
        """
        self.parameters = parameters
        return self

    def set_dependencies(
        self, dependencies: List[PbDependency]
    ) -> "ProcessingBlockConfigurationBuilder":
        """
        Set the dependencies
        :param dependencies: Dependencies
        """
        self.dependencies = dependencies
        return self

    def set_sbi_ids(
        self, sbi_ids: list
    ) -> "ProcessingBlockConfigurationBuilder":
        """
        Set the sbi ids
        :param sbi_ids: SBI ids
        """
        self.sbi_ids = sbi_ids
        return self

    def set_script(
        self, script: ScriptConfiguration
    ) -> "ProcessingBlockConfigurationBuilder":
        """
        Set the script
        :param script: Script
        """
        self.script = script
        return self

    def build(self) -> ProcessingBlockConfiguration:
        """
        Build or create CDM ProcessingBlockConfiguration object
        :return: CDM ProcessingBlockConfiguration object
        """
        return ProcessingBlockConfiguration(
            pb_id=self.pb_id,
            workflow=self.workflow,
            parameters=self.parameters,
            dependencies=self.dependencies,
            sbi_ids=self.sbi_ids,
            script=self.script,
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
        """
        Set the eb id
        :param eb_id: EB id
        """
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length: float) -> "SDPConfigurationBuilder":
        """
        Set the max length
        :param max_length: Max length
        """
        self.max_length = max_length
        return self

    def set_scan_types(self, scan_types: list) -> "SDPConfigurationBuilder":
        """
        Set the scan types
        :param scan_types: Scan types
        """
        self.scan_types = scan_types
        return self

    def set_processing_blocks(
        self, processing_blocks: List[ProcessingBlockConfiguration]
    ) -> "SDPConfigurationBuilder":
        """
        Set the processing blocks
        :param processing_blocks: Processing blocks
        """
        self.processing_blocks = processing_blocks
        return self

    def set_execution_block(
        self, execution_block: ExecutionBlockConfiguration
    ) -> "SDPConfigurationBuilder":
        """
        Set the execution block
        :param execution_block: Execution block
        """
        self.execution_block = execution_block
        return self

    def set_resources(self, resources: dict) -> "SDPConfigurationBuilder":
        """
        Set the resources
        :param resources: Resources
        """
        self.resources = resources
        return self

    def set_interface(self, interface: str) -> "SDPConfigurationBuilder":
        """
        Set the interface
        :param interface: Interface
        """
        self.interface = interface
        return self

    def build(self) -> SDPConfiguration:
        """
        Build or create CDM SDPConfiguration object
        :return: CDM SDPConfiguration object
        """
        return SDPConfiguration(
            eb_id=self.eb_id,
            max_length=self.max_length,
            scan_types=self.scan_types,
            processing_blocks=self.processing_blocks,
            execution_block=self.execution_block,
            resources=self.resources,
            interface=self.interface,
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
        """
        Set the beam id
        :param beam_id: Beam id
        """
        self.beam_id = beam_id
        return self

    def set_function(self, function: str) -> "BeamConfigurationBuilder":
        """
        Set the function
        :param function: Function
        """
        self.function = function
        return self

    def set_search_beam_id(
        self, search_beam_id: int
    ) -> "BeamConfigurationBuilder":
        """
        Set the search beam id
        :param search_beam_id: Search beam id
        """
        self.search_beam_id = search_beam_id
        return self

    def set_timing_beam_id(
        self, timing_beam_id: int
    ) -> "BeamConfigurationBuilder":
        """
        Set the timing beam id
        :param timing_beam_id: Timing beam id
        """
        self.timing_beam_id = timing_beam_id
        return self

    def set_vlbi_beam_id(
        self, vlbi_beam_id: int
    ) -> "BeamConfigurationBuilder":
        """
        Set the vlbi beam id
        :param vlbi_beam_id: Vlbi beam id
        """
        self.vlbi_beam_id = vlbi_beam_id
        return self

    def build(self) -> BeamConfiguration:
        """
        Build or create CDM BeamConfiguration object
        :return: CDM BeamConfiguration object
        """
        return BeamConfiguration(
            beam_id=self.beam_id,
            function=self.function,
            search_beam_id=self.search_beam_id,
            timing_beam_id=self.timing_beam_id,
            vlbi_beam_id=self.vlbi_beam_id,
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

    def set_channels_id(
        self, channels_id: str
    ) -> "ChannelConfigurationBuilder":
        """
        Set the channels id
        :param channels_id: Channels id
        """
        self.channels_id = channels_id
        return self

    def set_spectral_windows(
        self, spectral_windows: list
    ) -> "ChannelConfigurationBuilder":
        """
        Set the spectral windows
        :param spectral_windows: Spectral windows
        """
        self.spectral_windows = spectral_windows
        return self

    def build(self) -> ChannelConfiguration:
        """
        Build or create CDM ChannelConfiguration object
        :return: CDM ChannelConfiguration object
        """
        return ChannelConfiguration(
            channels_id=self.channels_id,
            spectral_windows=self.spectral_windows,
        )


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
        """
        Set the polarisations id
        :param polarisations_id: Polarisations id
        """
        self.polarisations_id = polarisations_id
        return self

    def set_corr_type(
        self, corr_type: list
    ) -> "PolarisationConfigurationBuilder":
        """
        Set the correlation type
        :param corr_type: Correlation type
        """
        self.corr_type = corr_type
        return self

    def build(self) -> PolarisationConfiguration:
        """
        Build or create CDM PolarisationConfiguration object
        :return: CDM PolarisationConfiguration object
        """
        return PolarisationConfiguration(
            polarisations_id=self.polarisations_id, corr_type=self.corr_type
        )


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
        """
        Set the right ascension
        :param ra: Right ascension
        """
        self.ra = ra
        return self

    def set_dec(self, dec: list) -> "PhaseDirBuilder":
        """
        Set the declination
        :param dec: Declination
        """
        self.dec = dec
        return self

    def set_reference_time(self, reference_time: str) -> "PhaseDirBuilder":
        """
        Set the reference time
        :param reference_time: Reference time
        """
        self.reference_time = reference_time
        return self

    def set_reference_frame(self, reference_frame: str) -> "PhaseDirBuilder":
        """
        Set the reference frame
        :param reference_frame: Reference frame
        """
        self.reference_frame = reference_frame
        return self

    def build(self) -> PhaseDir:
        """
        Build or create CDM PhaseDir object
        :return: CDM PhaseDir object
        """
        return PhaseDir(
            ra=self.ra,
            dec=self.dec,
            reference_time=self.reference_time,
            reference_frame=self.reference_frame,
        )


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
        """
        Set the field id
        :param field_id: Field id
        """
        self.field_id = field_id
        return self

    def set_pointing_fqdn(
        self, pointing_fqdn: str
    ) -> "FieldConfigurationBuilder":
        """
        Set the pointing fqdn
        :param pointing_fqdn: Pointing fqdn
        """
        self.pointing_fqdn = pointing_fqdn
        return self

    def set_phase_dir(
        self, phase_dir: PhaseDir
    ) -> "FieldConfigurationBuilder":
        """
        Set the phase dir
        :param phase_dir: Phase dir
        """
        self.phase_dir = phase_dir
        return self

    def build(self) -> FieldConfiguration:
        """
        Build or create CDM FieldConfiguration object
        :return: CDM FieldConfiguration object
        """
        return FieldConfiguration(
            field_id=self.field_id,
            pointing_fqdn=self.pointing_fqdn,
            phase_dir=self.phase_dir,
        )


EBScanTypeBuilder = functools.partial(
    EBScanType,
    scan_type_id="science",
    beams={"vis0": {"field_id": "field_a"}},
    derive_from=".default",
)


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
        """
        Set the field id
        :param field_id: Field id
        """
        self.field_id = field_id
        return self

    def set_channels_id(self, channels_id: str) -> "EBScanTypeBeamBuilder":
        """
        Set the channels id
        :param channels_id: Channels id
        """
        self.channels_id = channels_id
        return self

    def set_polarisations_id(
        self, polarisations_id: str
    ) -> "EBScanTypeBeamBuilder":
        """
        Set the polarisations id
        :param polarisations_id: Polarisations id
        """
        self.polarisations_id = polarisations_id
        return self

    def build(self) -> EBScanTypeBeam:
        """
        Build or create CDM EBScanTypeBeam object
        :return: CDM EBScanTypeBeam object
        """
        return EBScanTypeBeam(
            field_id=self.field_id,
            channels_id=self.channels_id,
            polarisations_id=self.polarisations_id,
        )


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
        """
        Set the eb id
        :param eb_id: EB id
        """
        self.eb_id = eb_id
        return self

    def set_max_length(self, max_length: float):
        """
        Set the max length
        :param max_length: Max length
        """
        self.max_length = max_length
        return self

    def set_context(
        self, context: dict
    ) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the context
        :param context: Context
        """
        self.context = context
        return self

    def set_beams(self, beams: list) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the beams
        :param beams: Beams
        """
        self.beams = beams
        return self

    def set_channels(
        self, channels: list
    ) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the channels
        :param channels: Channels
        """
        self.channels = channels
        return self

    def set_polarisations(
        self, polarisations: list
    ) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the polarisations
        :param polarisations: Polarisations
        """
        self.polarisations = polarisations
        return self

    def set_fields(self, fields: list) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the fields
        :param fields: Fields
        """
        self.fields = fields
        return self

    def set_scan_types(
        self, scan_types: list
    ) -> "ExecutionBlockConfigurationBuilder":
        """
        Set the scan types
        :param scan_types: Scan types
        """
        self.scan_types = scan_types
        return self

    def build(self) -> ExecutionBlockConfiguration:
        """
        Build or create CDM ExecutionBlockConfiguration object
        :return: CDM ExecutionBlockConfiguration object
        """
        return ExecutionBlockConfiguration(
            eb_id=self.eb_id,
            max_length=self.max_length,
            context=self.context,
            beams=self.beams,
            channels=self.channels,
            polarisations=self.polarisations,
            fields=self.fields,
            scan_types=self.scan_types,
        )
