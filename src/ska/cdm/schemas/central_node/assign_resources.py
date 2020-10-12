"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska.cdm.messages.central_node.assign_resources import AssignResourcesResponse
from ska.cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska.cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ska.cdm.schemas.central_node.csp import (
    DishAllocationSchema,
    DishAllocationResponseSchema,
)
from ska.cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska.cdm.schemas import CODEC

__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
    "ReleaseResourcesRequestSchema",
]


@CODEC.register_mapping(AssignResourcesRequest)
class AssignResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesRequest class.
    """

    subarray_id = fields.Integer(data_key="subarrayID", required=True)
    dish = fields.Nested(DishAllocationSchema, data_key="dish")
    sdp_config = fields.Nested(SDPConfigurationSchema, data_key="sdp")
    mccs = fields.Nested(MCCSAllocateSchema, data_key="mccs")

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
        subarray_id = data["subarray_id"]
        # Optional: not required in every case
        dish_allocation = data.get("dish", None)
        sdp_config = data.get("sdp_config", None)
        mccs = data.get("mccs", None)
        return AssignResourcesRequest(
            subarray_id,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            mccs_allocate=mccs,
        )


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


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    subarray_id = fields.Integer(data_key="subarrayID", required=True)
    dish = fields.Nested(DishAllocationSchema, data_key="dish")
    release_all = fields.Boolean(data_key="releaseALL")

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Marshmallow directives for ReleaseResourcesRequestSchema.
        """

        ordered = True

    @post_dump
    def filter_args(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter Marshmallow's JSON based on the value of release_all.

        If release_all is True, other resource definitions should be stripped
        from the request. If release_all if False, the 'release_all' key
        itself should be stripped.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for request submission
        """
        # If release_all is True, other resources should be stripped - and
        # vice versa
        release_all = data["releaseALL"]
        if release_all:
            del data["dish"]
        else:
            del data["releaseALL"]
        return data

    @post_load
    def create_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON from an ReleaseResources request back into an
        ReleaseResourcesRequest object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ReleaseResourcesRequest object populated from data
        """
        subarray_id = data["subarray_id"]
        release_all = data.get("release_all", False)
        dish_allocation = data.get("dish", None)
        return ReleaseResourcesRequest(
            subarray_id, release_all=release_all, dish_allocation=dish_allocation
        )
