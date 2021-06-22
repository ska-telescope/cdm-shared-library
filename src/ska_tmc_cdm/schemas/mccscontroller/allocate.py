"""
The schemas.central_node module defines Marshmallow schemas that map
MCCSController AllocateRequest message classes to/from their JSON
representation.
"""
from marshmallow import (
    fields,
    post_load,
)

from ..shared import ValidatingSchema
from ...messages.mccscontroller.allocate import AllocateRequest
from ...schemas import CODEC

__all__ = ["AllocateRequestSchema"]


@CODEC.register_mapping(AllocateRequest)
class AllocateRequestSchema(ValidatingSchema):
    """
    Marshmallow schema for the MCCSController AllocateRequest class.
    """

    interface = fields.String(required=False)
    subarray_id = fields.Integer(required=True)
    subarray_beam_ids = fields.List(fields.Integer, required=True)
    station_ids = fields.List(fields.List(fields.Integer), required=True)
    channel_blocks = fields.List(fields.Integer, required=True)

    @post_load
    def create_allocaterequest(self, data, **_) -> AllocateRequest:
        """
        Convert parsed JSON back into an AllocateRequest object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: AllocateRequest object populated from data
        """
        interface = data["interface"]
        subarray_id = data["subarray_id"]
        subarray_beam_ids = data["subarray_beam_ids"]
        station_ids = data["station_ids"]
        channel_blocks = data["channel_blocks"]
        return AllocateRequest(
            interface=interface,
            subarray_id=subarray_id,
            subarray_beam_ids=subarray_beam_ids,
            station_ids=station_ids,
            channel_blocks=channel_blocks
        )
