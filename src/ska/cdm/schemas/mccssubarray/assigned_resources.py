"""
The assigned_resources module defines Marshmallow schemas that maps the
MCCSSubarray.assigned_resources attribute to/from a JSON representation.
"""

from marshmallow import fields, post_load

from ska.cdm.messages.mccssubarray.assigned_resources import AssignedResources
from ska.cdm.schemas import CODEC
from ska.cdm.schemas.shared import ValidatingSchema

__all__ = ["AssignedResourcesSchema"]


@CODEC.register_mapping(AssignedResources)
class AssignedResourcesSchema(ValidatingSchema):
    """
    Marshmallow schema for the MCCSSubarray AssignedResources class.
    """

    interface = fields.String(required=False)
    subarray_beam_ids = fields.List(fields.Integer, required=True)
    station_ids = fields.List(fields.List(fields.Integer), required=True)
    channel_blocks = fields.List(fields.Integer, required=True)

    @post_load
    def create_allocaterequest(self, data, **_) -> AssignedResources:
        """
        Convert parsed JSON back into an AssignedResources object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: AssignedResources object populated from data
        """
        interface = data["interface"]
        subarray_beam_ids = data["subarray_beam_ids"]
        station_ids = data["station_ids"]
        channel_blocks = data["channel_blocks"]
        return AssignedResources(
            interface=interface,
            subarray_beam_ids=subarray_beam_ids,
            station_ids=station_ids,
            channel_blocks=channel_blocks
        )
