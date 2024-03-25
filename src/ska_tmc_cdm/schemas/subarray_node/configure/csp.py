"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode CSP configuration to/from JSON.
"""
import copy
import json

from marshmallow import Schema, fields, post_dump, post_load, pre_dump
from marshmallow.validate import OneOf

from ska_tmc_cdm.messages.subarray_node.configure.core import ReceiverBand
from ska_tmc_cdm.messages.subarray_node.configure.csp import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    VisConfiguration,
    VisFspConfiguration,
)
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.shared import ValidatingSchema

__all__ = [
    "CSPConfigurationSchema",
    "FSPConfigurationSchema",
    "SubarrayConfigurationSchema",
    "CommonConfigurationSchema",
    "CBFConfigurationSchema",
    "LowCBFConfigurationSchema",
]


@CODEC.register_mapping(SubarrayConfiguration)
class SubarrayConfigurationSchema(Schema):
    subarray_name = fields.String(data_key="subarray_name", required=True)

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
    config_id = fields.String(data_key="config_id", required=True)
    subarray_id = fields.Integer(data_key="subarray_id")
    frequency_band = fields.String(data_key="frequency_band")
    band_5_tuning = fields.List(fields.Float, data_key="band_5_tuning")

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
        if hasattr(copied, "frequency_band") and copied.frequency_band is not None:
            copied.frequency_band = common_configuration.frequency_band.value
        return copied

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
         Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration instance populated to match JSON
        """
        config_id = data.get("config_id")
        frequency_band = data.get("frequency_band")
        subarray_id = data.get("subarray_id")
        band_5_tuning = data.get("band_5_tuning", None)
        if frequency_band:
            frequency_band_enum = ReceiverBand(frequency_band)
            return CommonConfiguration(
                config_id, subarray_id, frequency_band_enum, band_5_tuning
            )
        return CommonConfiguration(config_id, subarray_id, band_5_tuning)


@CODEC.register_mapping(FSPConfiguration)
class FSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.FSPConfiguration class
    """

    fsp_id = fields.Integer(data_key="fsp_id", required=True)
    function_mode = fields.String(
        data_key="function_mode",
        validate=OneOf(["CORR", "PSS-BF", "PST-BF", "VLBI"]),
        required=True,
    )
    frequency_slice_id = fields.Integer(data_key="frequency_slice_id", required=True)
    zoom_factor = fields.Integer(data_key="zoom_factor", required=True)
    integration_factor = fields.Integer(data_key="integration_factor", required=True)
    channel_averaging_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="channel_averaging_map"
    )
    output_link_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="output_link_map"
    )
    channel_offset = fields.Integer(data_key="channel_offset")
    zoom_window_tuning = fields.Integer(data_key="zoom_window_tuning")

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
        copied = copy.deepcopy(fsp_configuration)
        copied.function_mode = fsp_configuration.function_mode.value
        return copied

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
        zoom_factor = data["zoom_factor"]
        integration_factor = data["integration_factor"]

        # optional arguments
        channel_averaging_map = data.get("channel_averaging_map", None)
        output_link_map = data.get("output_link_map", None)
        channel_offset = data.get("channel_offset", None)
        zoom_window_tuning = data.get("zoom_window_tuning", None)

        return FSPConfiguration(
            fsp_id,
            function_mode_enum,
            frequency_slice_id,
            integration_factor,
            zoom_factor,
            channel_averaging_map=channel_averaging_map,
            output_link_map=output_link_map,
            channel_offset=channel_offset,
            zoom_window_tuning=zoom_window_tuning,
        )


@CODEC.register_mapping(CBFConfiguration)
class CBFConfigurationSchema(Schema):
    fsp_configs = fields.Nested(FSPConfigurationSchema, many=True, data_key="fsp")
    vlbi_config = fields.Dict(data_key="vlbi")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a CBFConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: CBFConfiguration instance populated to match JSON
        :rtype: CBFConfiguration
        """
        fsp_configs = data.get("fsp_configs", None)
        # TODO: In future, when csp Interface 2.2 will be used than vlbi_config parameter type will be                  # pylint: disable=W0511
        #  replaced with the respective class schema (VLBIConfigurationSchema)
        vlbi_config = data.get("vlbi_config", None)
        return CBFConfiguration(fsp_configs=fsp_configs, vlbi_config=vlbi_config)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


@CODEC.register_mapping(StnBeamConfiguration)
class StnBeamConfigurationSchema(Schema):
    stn_beam_id = fields.Integer(data_key="stn_beam_id")
    freq_ids = fields.List(fields.Integer, data_key="freq_ids")
    host = fields.List(fields.Tuple((fields.Integer, fields.String)), data_key="host")
    port = fields.List(
        fields.Tuple((fields.Integer, fields.Integer, fields.Integer)), data_key="port"
    )
    mac = fields.List(fields.Tuple((fields.Integer, fields.String)), data_key="mac")
    integration_ms = fields.Integer(data_key="integration_ms")
    beam_id = fields.Integer(data_key="beam_id")
    delay_poly = fields.String(data_key="delay_poly")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StnBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnBeamConfiguration instance populated to match JSON
        :rtype: StnBeamConfiguration
        """
        stn_beam_id = data.get("stn_beam_id", None)
        freq_ids = data.get("freq_ids", None)
        host = data.get("host", None)
        port = data.get("port", None)
        mac = data.get("mac", None)
        integration_ms = data.get("integration_ms", None)
        beam_id = data.get("beam_id", None)
        delay_poly = data.get("delay_poly", None)

        return StnBeamConfiguration(
            stn_beam_id=stn_beam_id,
            freq_ids=freq_ids,
            host=host,
            port=port,
            mac=mac,
            integration_ms=integration_ms,
            beam_id=beam_id,
            delay_poly=delay_poly,
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


@CODEC.register_mapping(VisFspConfiguration)
class VisFspConfigurationSchema(Schema):
    function_mode = fields.String(data_key="function_mode")
    fsp_ids = fields.List(fields.Integer, data_key="fsp_ids")
    firmware = fields.String(data_key="firmware")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a VisFspConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: VisFspConfiguration instance populated to match JSON
        :rtype: VisFspConfiguration
        """
        function_mode = data.get("function_mode", None)
        fsp_ids = data.get("fsp_ids", None)
        firmware = data.get("firmware", None)
        return VisFspConfiguration(
            function_mode=function_mode, fsp_ids=fsp_ids, firmware=firmware
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


@CODEC.register_mapping(VisConfiguration)
class VisConfigurationSchema(Schema):
    fsp = fields.Nested(VisFspConfigurationSchema)
    stn_beams = fields.List(fields.Nested(StnBeamConfigurationSchema))

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a VisConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: VisConfiguration instance populated to match JSON
        :rtype: VisConfiguration
        """
        fsp = data.get("fsp", None)
        stn_beams = data.get("stn_beams", None)
        return VisConfiguration(fsp=fsp, stn_beams=stn_beams)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


@CODEC.register_mapping(StationConfiguration)
class StationConfigurationSchema(Schema):
    stns = fields.List(fields.List(fields.Integer))
    stn_beams = fields.List(fields.Nested(StnBeamConfigurationSchema))

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StationConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StationConfiguration instance populated to match JSON
        :rtype: StationConfiguration
        """
        stns = data.get("stns", None)
        stn_beams = data.get("stn_beams", None)
        return StationConfiguration(stns=stns, stn_beams=stn_beams)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


@CODEC.register_mapping(LowCBFConfiguration)
class LowCBFConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.LowCBFConfiguration class
    """

    stations = fields.Nested(StationConfigurationSchema, data_key="stations")
    vis = fields.Nested(VisConfigurationSchema, data_key="vis")

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a LowCBFConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: LowCBFConfiguration instance populated to match JSON
        """
        stations = data.get("stations", None)
        vis = data.get("vis", None)

        return LowCBFConfiguration(
            stations=stations,
            vis=vis,
        )


@CODEC.register_mapping(CSPConfiguration)
class CSPConfigurationSchema(ValidatingSchema):
    """
    Marshmallow schema for the subarray_node.CSPConfiguration class
    """

    interface = fields.String()
    subarray = fields.Nested(SubarrayConfigurationSchema, data_key="subarray")
    common = fields.Nested(CommonConfigurationSchema, data_key="common")
    cbf_config = fields.Nested(CBFConfigurationSchema, data_key="cbf")
    lowcbf = fields.Nested(LowCBFConfigurationSchema, data_key="lowcbf")

    # TODO: In future when csp Interface 2.2 will be used than these 2 parameter type will be                           # pylint: disable=W0511
    #  replaced with the respective class schema (PSSConfigurationSchema,PSTConfigurationSchema)
    pss_config = fields.Dict(data_key="pss")
    pst_config = fields.Dict(data_key="pst")

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON
        """
        interface = data.get("interface", None)
        subarray = data.get("subarray", None)
        common = data.get("common", None)
        cbf_config = data.get("cbf_config", None)
        pss = data.get("pss_config", None)
        pst = data.get("pst_config", None)
        lowcbf = data.get("lowcbf", None)

        return CSPConfiguration(
            interface=interface,
            subarray=subarray,
            common=common,
            cbf_config=cbf_config,
            pss_config=pss,
            pst_config=pst,
            lowcbf=lowcbf,
        )

    @post_dump
    def validate_on_dump(self, data, **_):  # pylint: disable=arguments-differ
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
