"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode MCCS configuration to/from JSON.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
    SubarrayBeamTarget,
)
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "MCCSConfigurationSchema",
    "StnConfigurationSchema",
    "SubarrayBeamConfigurationSchema",
    "SubarrayBeamTargetSchema",
    "SubarrayBeamAperatures",
    "SubarrayBeamLogicalBands",
    "SubarrayBeamSkyCoordinates",
]

from ska_tmc_cdm.schemas.shared import ValidatingSchema


@CODEC.register_mapping(SubarrayBeamTarget)
class SubarrayBeamTargetSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Target class
    """

    az = fields.Float(data_key="az", required=True)
    el = fields.Float(data_key="el", required=True)
    target_name = fields.String(data_key="target_name", required=True)
    reference_frame = fields.String(data_key="reference_frame", required=True)

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        az = data["az"]
        el = data["el"]
        target_name = data["target_name"]
        reference_frame = data["reference_frame"]
        return SubarrayBeamTarget(
            az=az, el=el, target_name=target_name, reference_frame=reference_frame
        )


@CODEC.register_mapping(SubarrayBeamSkyCoordinates)
class SubarrayBeamSkyCoordinatesSchema(Schema):
    timestamp = fields.String(data_key="timestamp", required=True)
    reference_frame = fields.String(data_key="reference_frame", required=True)
    c1 = fields.Float(data_key="c1", required=True)
    c1_rate = fields.Float(data_key="c1_rate", required=True)
    c2 = fields.Float(data_key="c2", required=True)
    c2_rate = fields.Float(data_key="c2_rate", required=True)

    @post_load
    def create(self, data, **_):
        """
        Convert parsed JSON back into a SubarrayBeamSkyCoordinates object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamSkyCoordinates instance populated to match JSON
        :rtype: SubarrayBeamSkyCoordinates
        """
        timestamp = data["timestamp"]
        reference_frame = data["reference_frame"]
        c1 = data["c1"]
        c1_rate = data["c1_rate"]
        c2 = data["c2"]
        c2_rate = data["c2_rate"]
        return SubarrayBeamSkyCoordinates(
            timestamp=timestamp,
            reference_frame=reference_frame,
            c1=c1,
            c1_rate=c1_rate,
            c2=c2,
            c2_rate=c2_rate,
        )


@CODEC.register_mapping(SubarrayBeamLogicalBands)
class SubarrayBeamLogicalBandsSchema(Schema):
    start_channel = fields.Integer(data_key="start_channel", required=True)
    number_of_channels = fields.Integer(data_key="number_of_channels", required=True)

    @post_load
    def create(self, data, **_):
        """
        Convert parsed JSON back into a SubarrayBeamLogicalBands object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamLogicalBands instance populated to match JSON
        :rtype: SubarrayBeamLogicalBands
        """
        start_channel = data["start_channel"]
        number_of_channels = data["number_of_channels"]
        return SubarrayBeamLogicalBands(
            start_channel=start_channel, number_of_channels=number_of_channels
        )


@CODEC.register_mapping(SubarrayBeamAperatures)
class SubarrayBeamAperaturesSchema(Schema):
    aperture_id = fields.String(data_key="aperture_id", required=True)
    weighting_key_ref = fields.String(data_key="weighting_key_ref", required=True)

    @post_load
    def create(self, data, **_):
        """
        Convert parsed JSON back into a SubarrayBeamAperatures object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamAperatures instance populated to match JSON
        :rtype: SubarrayBeamAperatures
        """
        aperture_id = data["aperture_id"]
        weighting_key_ref = data["weighting_key_ref"]
        return SubarrayBeamAperatures(
            aperture_id=aperture_id, weighting_key_ref=weighting_key_ref
        )


@CODEC.register_mapping(StnConfiguration)
class StnConfigurationSchema(Schema):
    station_id = fields.Integer(data_key="station_id", required=True)

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StnConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnConfiguration instance populated to match JSON
        :rtype: StnConfiguration
        """
        station_id = data["station_id"]
        return StnConfiguration(station_id)


@CODEC.register_mapping(SubarrayBeamConfiguration)
class SubarrayBeamConfigurationSchema(Schema):
    subarray_beam_id = fields.Integer(data_key="subarray_beam_id", required=True)
    station_ids = fields.List(fields.Integer(data_key="station_ids"))
    channels = fields.List(fields.List(fields.Integer), data_key="channels")
    update_rate = fields.Float(data_key="update_rate")
    target = fields.Nested(SubarrayBeamTargetSchema, data_key="target")
    antenna_weights = fields.List(fields.Float(data_key="antenna_weights"))
    phase_centre = fields.List(fields.Float(data_key="phase_centre"))
    logical_bands = fields.List(
        fields.Nested(SubarrayBeamLogicalBandsSchema, data_key="logical_bands")
    )
    apertures = fields.List(
        fields.Nested(SubarrayBeamAperaturesSchema, data_key="apertures")
    )
    sky_coordinates = fields.Nested(
        SubarrayBeamSkyCoordinatesSchema, data_key="sky_coordinates"
    )

    @post_load
    def create(self, data, **_) -> SubarrayBeamConfiguration:
        """
         Convert parsed JSON back into a SubarrayBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamConfiguration instance populated to match JSON
        """
        subarray_beam_id = data.get("subarray_beam_id", None)
        station_ids = data.get("station_ids", None)
        channels = data.get("channels", None)
        update_rate = data.get("update_rate", None)
        target = data.get("target", None)
        antenna_weights = data.get("antenna_weights", None)
        phase_centre = data.get("phase_centre", None)
        logical_bands = data.get("logical_bands", None)
        apertures = data.get("apertures", None)
        sky_coordinates = data.get("sky_coordinates", None)

        return SubarrayBeamConfiguration(
            subarray_beam_id=subarray_beam_id,
            station_ids=station_ids,
            channels=channels,
            update_rate=update_rate,
            target=target,
            antenna_weights=antenna_weights,
            phase_centre=phase_centre,
            logical_bands=logical_bands,
            apertures=apertures,
            sky_coordinates=sky_coordinates,
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        return {k: v for k, v in data.items() if v is not None}


@CODEC.register_mapping(MCCSConfiguration)
class MCCSConfigurationSchema(ValidatingSchema):
    """
    Marshmallow schema for the subarray_node.MCCSConfiguration class
    """

    station_configs = fields.Nested(
        StnConfigurationSchema, many=True, data_key="stations"
    )
    subarray_beam_configs = fields.Nested(
        SubarrayBeamConfigurationSchema, many=True, data_key="subarray_beams"
    )

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a MCCSConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSConfiguration instance populated to match JSON
        :rtype: MCCSConfiguration
        """
        stn_configs = data["station_configs"]
        subarray_beam_configs = data["subarray_beam_configs"]
        return MCCSConfiguration(
            station_configs=stn_configs, subarray_beam_configs=subarray_beam_configs
        )
