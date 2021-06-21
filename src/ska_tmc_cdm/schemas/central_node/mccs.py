"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""

from marshmallow import (
    fields,
    post_load,
    Schema
)

from ska_tmc_cdm.messages.central_node.mccs import MCCSAllocate

__all__ = ["MCCSAllocateSchema"]


class MCCSAllocateSchema(Schema):
    """
    Marshmallow schema for the MCCSAllocate class.
    """

    station_ids = fields.List(fields.List(fields.Integer()), required=True)
    channel_blocks = fields.List(fields.Integer(), required=True)
    subarray_beam_ids = fields.List(fields.Integer(), required=True)

    @post_load
    def create_mccs_allocate(self, data, **_):
        """
        Convert parsed JSON back into a MCCSAllocate object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSAllocate object populated from data
        """
        station_ids = data["station_ids"]
        channel_blocks = data["channel_blocks"]
        subarray_beam_ids = data["subarray_beam_ids"]
        return MCCSAllocate(station_ids, channel_blocks, subarray_beam_ids)
