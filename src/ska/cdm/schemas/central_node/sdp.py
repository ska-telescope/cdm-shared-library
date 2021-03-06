"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska.cdm.messages.central_node.sdp import (
    SDPConfiguration,
    ScanType,
    Channel,
    ProcessingBlockConfiguration,
    SDPWorkflow,
    PbDependency,
)
from ska.cdm.schemas import CODEC

__all__ = [
    "ScanTypeSchema",
    "SDPWorkflowSchema",
    "PbDependencySchema",
    "ChannelSchema",
    "ProcessingBlockSchema",
    "SDPConfigurationSchema",
]


class ChannelSchema(Schema):
    """
    Marshmallow schema for the SubBand class.
    """

    count = fields.Integer(data_key="count", required=True)
    start = fields.Integer(data_key="start", required=True)
    stride = fields.Integer(data_key="stride", required=True)
    freq_min = fields.Float(data_key="freq_min", required=True)
    freq_max = fields.Float(data_key="freq_max", required=True)
    link_map = fields.List(fields.List(fields.Int), data_key="link_map", required=True)

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
        stride = data["stride"]
        freq_min = data["freq_min"]
        freq_max = data["freq_max"]
        link_map = data["link_map"]
        return Channel(count, start, stride, freq_min, freq_max, link_map)


class ScanTypeSchema(Schema):
    """
    Marshmallow schema for the ScanType class.
    """

    st_id = fields.String(data_key="id", required=True)
    coordinate_system = fields.String(data_key="coordinate_system", required=True)
    ra = fields.String(data_key="ra", required=True)
    dec = fields.String(data_key="dec", required=True)
    channels = fields.Nested(ChannelSchema, data_key="channels", many=True)

    @post_load
    def create_scan_type(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanType object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanType object populated from data
        """
        st_id = data["st_id"]
        coordinate_system = data["coordinate_system"]
        ra = data["ra"]  # pylint: disable=invalid-name
        dec = data["dec"]
        channels = data["channels"]
        return ScanType(st_id, coordinate_system, ra, dec, channels)


class SDPWorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents the type of workflow being configured on the SDP
    """

    workflow_id = fields.String(data_key="id", required=True)
    workflow_type = fields.String(data_key="type", required=True)
    version = fields.String(data_key="version", required=True)

    @post_load
    def create_sdp_wf(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDP Workflow object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDP Workflow object populated from data
        """
        wf_id = data["workflow_id"]
        wf_type = data["workflow_type"]
        version = data["version"]
        return SDPWorkflow(wf_id, wf_type, version)


class PbDependencySchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the PbDepedency class.
    """

    pb_id = fields.String(data_key="pb_id")
    pb_type = fields.List(fields.String, data_key="type")

    @post_load
    def create_pb_dependency(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PbDependency object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PbDependency object populated from data
        """
        pb_id = data["pb_id"]
        pb_type = data["pb_type"]
        return PbDependency(pb_id, pb_type)


class ProcessingBlockSchema(Schema):
    """
    Marshmallow schema for the ProcessingBlock class.
    """

    pb_id = fields.String(data_key="id", required=True)
    workflow = fields.Nested(SDPWorkflowSchema)
    parameters = fields.Dict()
    dependencies = fields.Nested(PbDependencySchema, many=True, missing=None)

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
        Convert parsed JSON back into a PB object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PB object populated from data
        """
        return ProcessingBlockConfiguration(**data)


@CODEC.register_mapping(SDPConfiguration)
class SDPConfigurationSchema(Schema):
    """
    Marsmallow class for the SDPConfiguration class
    """

    sdp_id = fields.String(data_key="id", required=True)
    max_length = fields.Float(data_key="max_length", required=True)
    scan_types = fields.Nested(ScanTypeSchema, many=True)
    processing_blocks = fields.Nested(ProcessingBlockSchema, many=True)

    @post_load
    def create_sdp_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return SDPConfiguration(**data)
