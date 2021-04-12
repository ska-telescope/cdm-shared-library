"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode MCCS configuration to/from JSON.
"""

from marshmallow import Schema, fields, post_load

from ska.cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import StnConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import StnBeamConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import MCCSAllocate
from ska.cdm.schemas import CODEC

__all__ = [
    "MCCSConfigurationSchema",
    "StnConfigurationSchema",
    "StnBeamConfigurationSchema",
    "MCCSAllocateSchema",
]


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


class StnBeamConfigurationSchema(Schema):

    station_beam_id = fields.Integer(data_key="station_beam_id", required=True)
    station_ids = fields.List(fields.Integer(data_key="station_ids", required=True))
    channels = fields.List(fields.Integer(data_key="channels"))
    update_rate = fields.Float(data_key="update_rate")
    sky_coordinates = fields.List(fields.Float(data_key="sky_coordinates"))

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StnBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnBeamConfiguration instance populated to match JSON
        :rtype: StnBeamConfiguration
        """
        station_beam_id = data["station_beam_id"]
        station_ids = data["station_ids"]
        channels = data["channels"]
        update_rate = data["update_rate"]
        sky_coords = data["sky_coordinates"]
        return StnBeamConfiguration(
            station_beam_id, station_ids, channels, update_rate, sky_coords
        )


@CODEC.register_mapping(MCCSConfiguration)
class MCCSConfigurationSchema(Schema):
    """
    Marshmallow schema for the subarray_node.MCCSConfiguration class
    """

    station_configs = fields.Nested(
        StnConfigurationSchema, many=True, data_key="stations"
    )
    station_beam_configs = fields.Nested(
        StnBeamConfigurationSchema, many=True, data_key="station_beams"
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
        stn_beam_configs = data["station_beam_configs"]
        return MCCSConfiguration(stn_configs, stn_beam_configs)


@CODEC.register_mapping(MCCSAllocate)
class MCCSAllocateSchema(Schema):
    """
    Marshmallow schema for the MCCSAllocate class.
    """

    subarray_beam_ids = fields.List(
        fields.Integer, data_key="subarray_beam_ids", required=True
    )
    station_ids = fields.List(fields.List(fields.Integer), data_key="station_ids", required=True)
    channel_blocks = fields.List(fields.Integer, data_key="channel_blocks", required=True)
    

    @post_load
    def create_mccs_allocate(self, data, **_):
        """
        Convert parsed JSON back into a MCCSAllocate object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSAllocate object populated from data
        """
        subarray_beam_ids = data["subarray_beam_ids"]
        station_ids = data["station_ids"]
        channel_blocks = data["channel_blocks"]
        return MCCSAllocate(subarray_beam_ids, station_ids, channel_blocks)

