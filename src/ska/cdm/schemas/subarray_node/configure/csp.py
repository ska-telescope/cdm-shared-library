"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode CSP configuration to/from JSON.
"""
import copy
import json
from marshmallow import Schema, fields, post_load, pre_dump, post_dump, pre_load
from marshmallow.validate import OneOf
from ska.cdm.jsonschema.json_schema import JsonSchema
from ska.cdm.messages.subarray_node.configure.csp import (
    FSPFunctionMode,
    FSPConfiguration,
    SubarrayConfiguration,
    CommonConfiguration,
    CBFConfiguration,
    CSPConfiguration
)
from ska.cdm.messages.subarray_node.configure.core import ReceiverBand
from ska.cdm.schemas import CODEC
from ska.cdm.schemas.shared import ValidatingSchema

__all__ = ["CSPConfigurationSchema", "FSPConfigurationSchema",
           "SubarrayConfigurationSchema", "CommonConfigurationSchema",
           "CBFConfigurationSchema"]


@CODEC.register_mapping(SubarrayConfiguration)
class SubarrayConfigurationSchema(Schema):
    subarray_name = fields.String(data_key="subarrayName", required=True)

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a SubarrayConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayConfiguration instance populated to match JSON
        :rtype: SubarrayConfiguration
        """
        subarray_name = data["subarray_name"]
        return SubarrayConfiguration(subarray_name)


@CODEC.register_mapping(CommonConfiguration)
class CommonConfigurationSchema(Schema):
    csp_id = fields.String(data_key="id", required=True)
    frequency_band = fields.String(data_key="frequencyBand", required=True)
    subarray_id = fields.Integer(data_key="subarrayID", required=True)

    @pre_dump
    def convert(
            self, common_configuration: CommonConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process CommonConfiguration instance so that it is ready for conversion
        to JSON.

        :param CommonConfiguration: Common configuration to process
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        copied = copy.deepcopy(common_configuration)
        if hasattr(copied, 'frequency_band'):
            copied.frequency_band = common_configuration.frequency_band.value
        return copied

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration instance populated to match JSON
        """
        csp_id = data["csp_id"]
        frequency_band = data["frequency_band"]
        frequency_band_enum = ReceiverBand(frequency_band)
        subarray_id = data["subarray_id"]

        return CommonConfiguration(csp_id, frequency_band_enum, subarray_id)


@CODEC.register_mapping(FSPConfiguration)
class FSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.FSPConfiguration class
    """

    fsp_id = fields.Integer(data_key="fspID", required=True)
    function_mode = fields.String(
        data_key="functionMode",
        validate=OneOf(["CORR", "PSS-BF", "PST-BF", "VLBI"]),
        required=True,
    )
    frequency_slice_id = fields.Integer(data_key="frequencySliceID", required=True)
    corr_bandwidth = fields.Integer(data_key="corrBandwidth", required=True)
    integration_time = fields.Integer(data_key="integrationTime", required=True)
    channel_averaging_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="channelAveragingMap"
    )
    output_link_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="outputLinkMap"
    )
    fsp_channel_offset = fields.Integer(data_key="fspChannelOffset")
    zoom_window_tuning = fields.Integer(data_key="zoomWindowTuning")

    @pre_dump
    def convert(
            self, fsp_configuration: FSPConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process FSPConfiguration instance so that it is ready for conversion
        to JSON.

        :param fsp_configuration: FSP configuration to process
        :param _: kwargs passed by Marshmallow
        :return: FspConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        fsp_configuration.function_mode = fsp_configuration.function_mode.value
        return fsp_configuration

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for FSP configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a FSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: FSPConfiguration instance populated to match JSON
        """
        fsp_id = data["fsp_id"]
        function_mode = data["function_mode"]
        function_mode_enum = FSPFunctionMode(function_mode)
        frequency_slice_id = int(data["frequency_slice_id"])
        corr_bandwidth = data["corr_bandwidth"]
        integration_time = data["integration_time"]

        # optional arguments
        channel_averaging_map = data.get("channel_averaging_map", None)
        output_link_map = data.get("output_link_map", None)
        fsp_channel_offset = data.get("fsp_channel_offset", None)
        zoom_window_tuning = data.get("zoom_window_tuning", None)

        return FSPConfiguration(
            fsp_id,
            function_mode_enum,
            frequency_slice_id,
            integration_time,
            corr_bandwidth,
            channel_averaging_map=channel_averaging_map,
            output_link_map=output_link_map,
            fsp_channel_offset=fsp_channel_offset,
            zoom_window_tuning=zoom_window_tuning,
        )


@CODEC.register_mapping(CBFConfiguration)
class CBFConfigurationSchema(Schema):
    fsp_configs = fields.Nested(FSPConfigurationSchema, many=True, data_key="fsp")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a CBFConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: CBFConfiguration instance populated to match JSON
        :rtype: CBFConfiguration
        """
        fsp_configs = data["fsp_configs"]
        return CBFConfiguration(fsp_configs)


@CODEC.register_mapping(CSPConfiguration)
class CSPConfigurationSchema(ValidatingSchema):
    """
    Marshmallow schema for the subarray_node.CSPConfiguration class
    """

    interface = fields.String()
    csp_id = fields.String(data_key="id")
    frequency_band = fields.String(data_key="frequencyBand")
    fsp_configs = fields.Nested(FSPConfigurationSchema, many=True, data_key="fsp")
    subarray_config = fields.Nested(SubarrayConfigurationSchema, data_key="subarray")
    common_config = fields.Nested(CommonConfigurationSchema, data_key="common")
    cbf_config = fields.Nested(CBFConfigurationSchema, data_key="cbf")

    @pre_dump
    def convert(
            self, csp_configuration: CSPConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process CSPConfiguration instance so that it is ready for conversion
        to JSON.

        :param csp_configuration: CSP configuration to process
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        copied = copy.deepcopy(csp_configuration)
        if hasattr(copied, 'frequency_band') and copied.frequency_band:
            copied.frequency_band = csp_configuration.frequency_band.value
        return copied

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON
        """
        interface = data.get("interface", None)
        csp_id = data.get("csp_id", None)
        frequency_band = data.get("frequency_band", None)
        if frequency_band is not None:
            frequency_band = ReceiverBand(frequency_band)
        fsp_configs = data.get("fsp_configs", None)
        subarray_config = data.get("subarray_config", None)
        common_config = data.get("common_config", None)
        cbf_config = data.get("cbf_config", None)

        return CSPConfiguration(
            interface=interface,
            csp_id=csp_id,
            frequency_band=frequency_band,
            fsp_configs=fsp_configs,
            subarray_config=subarray_config,
            common_config=common_config,
            cbf_config=cbf_config
        )

    @post_dump
    def validate_on_dump(self, data, **_):
        """
        Validating the structure of JSON against schemas and
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        # filter out null values from JSON
        data = {k: v for k, v in data.items() if v is not None}

        # convert tuples to lists
        data = json.loads(json.dumps(data))

        data = super().validate_on_dump(data)
        return data
