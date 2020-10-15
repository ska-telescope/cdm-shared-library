"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska.cdm.messages.central_node.mccs import MCCSAllocate
from ska.cdm.schemas import CODEC

__all__ = ["MCCSAllocateSchema"]


@CODEC.register_mapping(MCCSAllocate)
class MCCSAllocateSchema(Schema):
    """
    Marshmallow schema for the MCCSAllocate class.
    """

    subarray_id = fields.Integer(data_key="subarray_id", required=True)
    station_ids = fields.List(fields.Integer, data_key="station_ids")
    station_beam_ids = fields.List(fields.Integer, data_key="station_beam_ids")

    @post_load
    def create_mccs_allocate(self, data, **_):
        """
        Convert parsed JSON back into a MCCSAllocate object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSAllocate object populated from data
        """
        subarray_id = data["subarray_id"]
        station_ids = data["station_ids"]
        station_beam_ids = data["station_beam_ids"]
        return MCCSAllocate(subarray_id, station_ids, station_beam_ids)
