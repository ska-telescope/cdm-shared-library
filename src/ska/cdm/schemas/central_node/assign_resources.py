"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.assign_resources import AssignResourcesResponse
from ska.cdm.schemas import CODEC
from ska.cdm.schemas.central_node.common import (
    DishAllocationSchema,
    DishAllocationResponseSchema,
)
from ska.cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska.cdm.schemas.central_node.sdp import SDPConfigurationSchema

__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
]


@CODEC.register_mapping(AssignResourcesRequest)
class AssignResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesRequest class.
    """

    subarray_id_mid = fields.Integer(data_key="subarrayID")
    dish = fields.Nested(DishAllocationSchema, data_key="dish")
    sdp_config = fields.Nested(SDPConfigurationSchema, data_key="sdp")
    mccs = fields.Nested(MCCSAllocateSchema, data_key="mccs")
    interface_url = fields.String(data_key="interface")
    subarray_id_low = fields.Integer(data_key="subarray_id")

    class Meta:  # pylint: disable=too-few-public-methods
        """
        marshmallow directives for AssignResourcesRequestSchema.
        """

        ordered = True

    @post_load
    def create_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into an AssignResources request object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: AssignResources object populated from data
        """
        subarray_id_mid = data.get("subarray_id_mid", None)
        dish_allocation = data.get("dish", None)
        sdp_config = data.get("sdp_config", None)
        mccs = data.get("mccs", None)
        interface = data.get("interface_url", None)
        subarray_id_low = data.get("subarray_id_low", None)

        return AssignResourcesRequest(
            subarray_id_mid,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            mccs_allocate=mccs,
            interface_url=interface,
            subarray_id_low=subarray_id_low
        )

    @post_dump
    def filter_nulls(self, data, **_):
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        return {k: v for k, v in data.items() if v is not None}


@CODEC.register_mapping(AssignResourcesResponse)
class AssignResourcesResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesResponse class.
    """

    dish = fields.Nested(DishAllocationResponseSchema, data_key="dish", required=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Marshmallow directives for AssignResourcesResponseSchema.
        """

        ordered = True

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON from an AssignResources response back into an
        AssignResourcesResponse object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: AssignResourcesResponse object populated from data
        """
        dish_allocation = data["dish"]
        return AssignResourcesResponse(dish_allocation=dish_allocation)
