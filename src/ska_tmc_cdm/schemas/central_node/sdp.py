"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""


from marshmallow import Schema, fields, post_dump, post_load
from ska_tmc_cdm.jsonschema.json_schema import JsonSchema

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
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "ScanTypeSchema",
    "SDPWorkflowSchema",
    "PbDependencySchema",
    "ChannelSchema",
    "ProcessingBlockSchema",
    "SDPConfigurationSchema",
    "ExecutionBlockConfigurationSchema",
    "BeamConfigurationSchema",
    "ChannelConfigurationSchema",
    "PolarisationConfigurationSchema",
    "FieldConfigurationSchema",
    "PhaseDirSchema",
    "ScriptConfigurationSchema",
    "EBScanTypeBeamSchema",
    "EBScanTypeSchema",
]


class ChannelSchema(Schema):
    """
    Marshmallow schema for the SubBand class.
    """

    count = fields.Integer(data_key="count", required=True)
    start = fields.Integer(data_key="start", required=True)
    stride = fields.Integer()
    freq_min = fields.Float(data_key="freq_min", required=True)
    freq_max = fields.Float(data_key="freq_max", required=True)
    link_map = fields.List(fields.List(fields.Integer()))
    spectral_window_id = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_channel(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Channel object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SubBand object populated from data
        """
        count = data["count"]
        start = data["start"]
        stride = data.get("stride")
        freq_min = data["freq_min"]
        freq_max = data["freq_max"]
        link_map = data.get("link_map")
        spectral_window_id = data.get("spectral_window_id")
        return Channel(
            count, start, stride, freq_min, freq_max, link_map, spectral_window_id
        )


class ScanTypeSchema(Schema):
    """
    Marshmallow schema for the ScanType class.
    """

    scan_type_id = fields.String(data_key="scan_type_id", required=True)
    reference_frame = fields.String(data_key="reference_frame", required=True)
    ra = fields.String(data_key="ra", required=True)
    dec = fields.String(data_key="dec", required=True)
    channels = fields.Nested(ChannelSchema, data_key="channels", many=True)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_scan_type(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanType object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanType object populated from data
        """
        scan_type_id = data["scan_type_id"]
        reference_frame = data["reference_frame"]
        ra = data["ra"]  # pylint: disable=invalid-name
        dec = data["dec"]
        channels = data["channels"]
        return ScanType(scan_type_id, reference_frame, ra, dec, channels)


class SDPWorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents the type of workflow being configured on the SDP
    """

    name = fields.String(data_key="name", required=True)
    kind = fields.String(data_key="kind", required=True)
    version = fields.String(data_key="version", required=True)

    @post_load
    def create_sdp_wf(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDP Workflow object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDP Workflow object populated from data
        """
        name = data["name"]
        kind = data["kind"]
        version = data["version"]
        return SDPWorkflow(name, kind, version)


class PbDependencySchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the PbDepedency class.
    """

    pb_id = fields.String(data_key="pb_id")
    kind = fields.List(fields.String())

    @post_load
    def create_pb_dependency(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PbDependency object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PbDependency object populated from data
        """
        pb_id = data["pb_id"]
        kind = data["kind"]
        return PbDependency(pb_id, kind)


class ScriptConfigurationSchema(Schema):
    """
    Marshmallow schema for the ScriptConfiguration class.
    """

    kind = fields.String()
    name = fields.String()
    version = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_executionblock_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScriptConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return ScriptConfiguration(**data)


class ProcessingBlockSchema(Schema):
    """
    Marshmallow schema for the ProcessingBlock class.
    """

    pb_id = fields.String(data_key="pb_id", required=True)
    workflow = fields.Nested(SDPWorkflowSchema)
    parameters = fields.Dict()
    dependencies = fields.List(fields.Nested(PbDependencySchema))
    sbi_ids = fields.List(fields.String())
    script = fields.Nested(ScriptConfigurationSchema)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_processing_block_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ProcessingBlock object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PB object populated from data
        """
        return ProcessingBlockConfiguration(**data)


class BeamConfigurationSchema(Schema):
    """
    Marsmallow class for the BeamConfiguration class
    """

    beam_id = fields.String()
    function = fields.String()
    search_beam_id = fields.Integer()
    timing_beam_id = fields.Integer()
    vlbi_beam_id = fields.Integer()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_beam_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a BeamConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return BeamConfiguration(**data)


class ChannelConfigurationSchema(Schema):
    """
    Marsmallow class for the ChannelConfiguration class
    """

    channels_id = fields.String()
    spectral_windows = fields.Nested(ChannelSchema, many=True)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_channel_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ChannelConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return ChannelConfiguration(**data)


class PolarisationConfigurationSchema(Schema):
    """
    Marsmallow class for the PolarisationConfiguration class
    """

    polarisations_id = fields.String()
    corr_type = fields.List(fields.String())

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_polarisation_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PolarisationConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return PolarisationConfiguration(**data)


class PhaseDirSchema(Schema):
    """
    Marsmallow class for the PhaseDir class
    """

    ra = fields.List(fields.Float())
    dec = fields.List(fields.Number())
    reference_time = fields.String()
    reference_frame = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_phase_dir_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PhaseDir object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return PhaseDir(**data)


class FieldConfigurationSchema(Schema):
    """
    Marsmallow class for the FieldConfiguration class
    """

    field_id = fields.String()
    phase_dir = fields.Nested(PhaseDirSchema)
    pointing_fqdn = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_polarisation_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a FieldConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return FieldConfiguration(**data)


class EBScanTypeBeamSchema(Schema):
    """
    Marsmallow class for the EBScanTypeBeam class
    """

    field_id = fields.String()
    channels_id = fields.String()
    polarisations_id = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_ebscantypebeams_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a EBScanTypeBeam object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return EBScanTypeBeam(**data)


class EBScanTypeSchema(Schema):
    """
    Marsmallow class for the EBScanTypeBeam class
    """

    scan_type_id = fields.String()
    beams = fields.Dict(
        keys=fields.String(), values=fields.Nested(EBScanTypeBeamSchema)
    )
    derive_from = fields.String()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """

        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_ebscantype_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a EBScanType object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """

        return EBScanType(**data)


class ExecutionBlockConfigurationSchema(Schema):
    """
    Marsmallow class for the ExecutionBlockConfiguration class
    """

    eb_id = fields.String(data_key="eb_id")
    max_length = fields.Float(data_key="max_length")
    context = fields.Dict()
    beams = fields.List(fields.Nested(BeamConfigurationSchema))
    channels = fields.List(fields.Nested(ChannelConfigurationSchema))
    polarisations = fields.List(fields.Nested(PolarisationConfigurationSchema))
    scan_types = fields.List(fields.Nested(EBScanTypeSchema))
    fields = fields.List(fields.Nested(FieldConfigurationSchema))

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_executionblock_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ExecutionBlockConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return ExecutionBlockConfiguration(**data)


@CODEC.register_mapping(SDPConfiguration)
class SDPConfigurationSchema(Schema):
    """
    Marsmallow class for the SDPConfiguration class
    """

    interface = fields.String()
    execution_block = fields.Nested(ExecutionBlockConfigurationSchema)

    eb_id = fields.String(data_key="eb_id")
    max_length = fields.Float(data_key="max_length")
    scan_types = fields.Nested(ScanTypeSchema, many=True)
    processing_blocks = fields.Nested(ProcessingBlockSchema, many=True)
    resources = fields.Dict()

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_sdp_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return SDPConfiguration(**data)
    
    def validate_json(self, data, process_fn=lambda x: x):
        """
        validating the structure of JSON against schemas

        :param data: Marshmallow-provided dict containing parsed object values
        :param lambda function: use for converting list of tuples to list of list
        :return:
        """
        # return early unless custom_validate is defined and True
        if not self.context.get("custom_validate", False):
            return

        interface = data.get("interface", None)
        if interface:
            JsonSchema.validate_schema(interface, process_fn(data))

