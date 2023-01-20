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
    BeamsConfiguration,
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    LowCBFConfiguration,
    StationsConfiguration,
    StnBeamConfiguration,
    SubarrayConfiguration,
    TimingBeamsConfiguration,
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
    config_id = fields.String(data_key="config_id", required=False)
    frequency_band = fields.String(data_key="frequency_band", required=False)
    subarray_id = fields.Integer(data_key="subarray_id", required=True)
    band_5_tuning = fields.List(fields.Float, data_key="band_5_tuning")

    @pre_dump
    def convert(
        self, commonuration: CommonConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process CommonConfiguration instance so that it is ready for conversion
        to JSON.

        :param CommonConfiguration: Common configuration to process
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        copied = copy.deepcopy(commonuration)
        if hasattr(copied, "frequency_band") and copied.frequency_band is not None:
            copied.frequency_band = commonuration.frequency_band.value
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
        frequency_band_enum = (
            ReceiverBand(frequency_band) if frequency_band else frequency_band
        )
        subarray_id = data.get("subarray_id")
        band_5_tuning = data.get("band_5_tuning", None)

        return CommonConfiguration(
            config_id, frequency_band_enum, subarray_id, band_5_tuning
        )


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
    beam_id = fields.Integer(data_key="beam_id")
    freq_ids = fields.List(fields.Integer, data_key="stns")
    boresight_dly_poly = fields.String(data_key="boresight_dly_poly")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StnBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnBeamConfiguration instance populated to match JSON
        :rtype: StnBeamConfiguration
        """
        beam_id = data.get("beam_id", None)
        freq_ids = data.get("freq_ids", None)
        boresight_dly_poly = data.get("boresight_dly_poly", None)
        return StnBeamConfiguration(
            beam_id=beam_id, freq_ids=freq_ids, boresight_dly_poly=boresight_dly_poly
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


@CODEC.register_mapping(BeamsConfiguration)
class BeamsConfigurationSchema(Schema):
    pst_beam_id = fields.Integer(data_key="pst_beam_id")
    stn_beam_id = fields.Integer(data_key="stn_beam_id")
    offset_dly_poly = fields.String(data_key="config_id")
    stn_weights = fields.List(fields.Float, data_key="stn_weights")
    jones = fields.String(data_key="jones")
    dest_ip = fields.List(fields.String(), data_key="dest_ip")
    dest_chans = fields.List(fields.Integer, data_key="dest_chans")
    rfi_enable = fields.List(fields.Boolean, data_key="rfi_enable")
    rfi_static_chans = fields.List(fields.Integer, data_key="rfi_static_chans")
    rfi_dynamic_chans = fields.List(fields.Integer, data_key="rfi_dynamic_chans")
    rfi_weighted = fields.Integer(data_key="rfi_weighted")

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a BeamsConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: BeamsConfiguration instance populated to match JSON
        :rtype: BeamsConfiguration
        """
        pst_beam_id = data.get("pst_beam_id", None)
        stn_beam_id = data.get("stn_beam_id", None)
        offset_dly_poly = data.get("offset_dly_poly", None)
        stn_weights = data.get("stn_weights", None)
        jones = data.get("jones", None)
        dest_ip = data.get("dest_ip", None)
        dest_chans = data.get("dest_chans", None)
        rfi_enable = data.get("rfi_enable", None)
        rfi_static_chans = data.get("rfi_static_chans", None)
        rfi_dynamic_chans = data.get("rfi_dynamic_chans", None)
        rfi_weighted = data.get("rfi_weighted", None)
        return BeamsConfiguration(
            pst_beam_id=pst_beam_id,
            stn_beam_id=stn_beam_id,
            offset_dly_poly=offset_dly_poly,
            stn_weights=stn_weights,
            jones=jones,
            dest_ip=dest_ip,
            dest_chans=dest_chans,
            rfi_enable=rfi_enable,
            rfi_static_chans=rfi_static_chans,
            rfi_dynamic_chans=rfi_dynamic_chans,
            rfi_weighted=rfi_weighted,
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


@CODEC.register_mapping(TimingBeamsConfiguration)
class TimingBeamsConfigurationSchema(Schema):
    beams = fields.List(fields.Nested(BeamsConfigurationSchema))

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a TimingBeamsConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: TimingBeamsConfiguration instance populated to match JSON
        :rtype: TimingBeamsConfiguration
        """
        beams = data.get("beams", None)
        return TimingBeamsConfiguration(beams=beams)

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


@CODEC.register_mapping(StationsConfiguration)
class StationsConfigurationSchema(Schema):
    stns = fields.List(fields.List(fields.Integer))
    stn_beams = fields.List(fields.Nested(StnBeamConfigurationSchema))

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StationsConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StationsConfiguration instance populated to match JSON
        :rtype: StationsConfiguration
        """
        stns = data.get("stns", None)
        stn_beams = data.get("stn_beams", None)
        return StationsConfiguration(stns=stns, stn_beams=stn_beams)

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

    stations = fields.Dict(data_key="stations")
    timing_beams = fields.Dict(data_key="timing_beams")
    search_beams = fields.String(data_key="search_beams")
    zooms = fields.String()
    scan_id = fields.Integer()
    unix_epoch_seconds = fields.Integer()
    timestamp_ns = fields.Integer()
    packet_offset = fields.Integer()
    scan_seconds = fields.Integer()

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a LowCBFConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: LowCBFConfiguration instance populated to match JSON
        """
        stations = data.get("stations", None)
        timing_beams = data.get("timing_beams", None)
        search_beams = data.get("search_beams", None)
        zooms = data.get("zooms", None)
        scan_id = data.get("scan_id", None)
        unix_epoch_seconds = data.get("unix_epoch_seconds", None)
        timestamp_ns = data.get("timestamp_ns", None)
        packet_offset = data.get("packet_offset", None)
        scan_seconds = data.get("scan_seconds", None)

        return LowCBFConfiguration(
            stations=stations,
            timing_beams=timing_beams,
            search_beams=search_beams,
            zooms=zooms,
            scan_id=scan_id,
            unix_epoch_seconds=unix_epoch_seconds,
            timestamp_ns=timestamp_ns,
            packet_offset=packet_offset,
            scan_seconds=scan_seconds,
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

        # data = super().validate_on_dump(data)
        return data


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
