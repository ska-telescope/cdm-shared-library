"""
The configure module defines Marshmallow schemas that maps the
MCCSSubarray.Configure call arguments to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska.cdm.messages.mccssubarray.configure import (
    ConfigureRequest,
    StationConfiguration,
    SubarrayBeamConfiguration
)
from ska.cdm.schemas import CODEC

__all__ = [
    "ConfigureRequestSchema",
    "StationConfigurationSchema",
    "SubarrayBeamConfiguration"
]


class StationConfigurationSchema(Schema):
    station_id = fields.Integer(required=True)

    @post_load
    def create(self, data, **_) -> StationConfiguration:
        """
         Convert parsed JSON back into a StationConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnConfiguration instance populated to match JSON
        """
        station_id = data["station_id"]
        return StationConfiguration(
            station_id=station_id
        )


class SubarrayBeamConfigurationSchema(Schema):
    subarray_beam_id = fields.Integer(required=True)
    station_ids = fields.List(fields.Integer, required=True)
    update_rate = fields.Float(required=True)
    channels = fields.List(fields.List(fields.Integer), required=True)
    sky_coordinates = fields.List(fields.Float, required=True)
    antenna_weights = fields.List(fields.Float, required=True)
    phase_centre = fields.List(fields.Float, required=True)

    @post_load
    def create(self, data, **_) -> SubarrayBeamConfiguration:
        """
         Convert parsed JSON back into a SubarrayBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamConfiguration instance populated to match JSON
        """
        subarray_beam_id = data["subarray_beam_id"]
        station_ids = data["station_ids"]
        update_rate = data["update_rate"]
        channels = data["channels"]
        sky_coordinates = data["sky_coordinates"]
        antenna_weights = data["antenna_weights"]
        phase_centre = data["phase_centre"]

        return SubarrayBeamConfiguration(
            subarray_beam_id=subarray_beam_id,
            station_ids=station_ids,
            update_rate=update_rate,
            channels=channels,
            sky_coordinates=sky_coordinates,
            antenna_weights=antenna_weights,
            phase_centre=phase_centre
        )


@CODEC.register_mapping(ConfigureRequest)
class ConfigureRequestSchema(Schema):
    """
    Marshmallow schema for the mccssubarray.ConfigureRequest class
    """

    interface = fields.String(required=True)
    stations = fields.Nested(StationConfigurationSchema, many=True, required=True)
    subarray_beams = fields.Nested(
        SubarrayBeamConfigurationSchema, many=True, required=True
    )

    @post_load
    def create(self, data, **_) -> ConfigureRequest:
        """
         Convert parsed JSON back into a ConfigureRequest object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: ConfigureRequest instance populated to match JSON
        """
        interface = data["interface"]
        stations = data["stations"]
        subarray_beams = data["subarray_beams"]
        return ConfigureRequest(
            interface=interface,
            stations=stations,
            subarray_beams=subarray_beams
        )
