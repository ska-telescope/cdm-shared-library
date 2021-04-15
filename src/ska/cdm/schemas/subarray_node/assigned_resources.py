"""
This module defines Marshmallow schemas that map CDM classes
to/from JSON.
"""

from marshmallow import Schema, fields, post_load

from ska.cdm.messages.subarray_node.assigned_resources import MCCSAllocation
from ska.cdm.messages.subarray_node.assigned_resources import AssignedResources
from ska.cdm.schemas import CODEC

__all__ = [
    "MCCSAllocationSchema",
    "AssignedResourcesSchema"
]


@CODEC.register_mapping(MCCSAllocation)
class MCCSAllocationSchema(Schema):
    """
    Marshmallow schema for the MCCSAllocation class.
    """

    subarray_beam_ids = fields.List(
        fields.Integer, data_key="subarray_beam_ids", required=True
    )
    station_ids = fields.List(
                    fields.List(fields.Integer),
                    data_key="station_ids",
                    required=True
    )
    channel_blocks = fields.List(
                    fields.Integer,
                    data_key="channel_blocks",
                    required=True
    )

    @post_load
    def create_mccs_allocation(self, data, **_):
        """
        Convert parsed JSON back into a MCCSAllocation object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSAllocation object populated from data
        """
        subarray_beam_ids = data.get("subarray_beam_ids", None)
        station_ids = data.get("station_ids", None)
        channel_blocks = data.get("channel_blocks", None)
        return MCCSAllocation(subarray_beam_ids, station_ids, channel_blocks)


@CODEC.register_mapping(AssignedResources)
class AssignedResourcesSchema(Schema):
    """
    """
    mccs = fields.Nested(MCCSAllocationSchema)
    interface = fields.String(data_key="interface")

    @post_load
    def create_assigned_resources(self, data, **_):
        """
        Convert parsed JSON back into an AssignedResources object

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: AssignedResources object populated from data
        """
        mccs = data.get("mccs", None)
        interface = data.get("interface", None)
        return AssignedResources(mccs, interface)
