"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.assign_resources import (
    AssignResourcesRequest,
    AssignResourcesResponse,
)
from ska_tmc_cdm.schemas.central_node.common import (
    DishAllocationResponseSchema,
    DishAllocationSchema,
)
from ska_tmc_cdm.schemas.central_node.csp import CSPConfigurationSchema
from ska_tmc_cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema

from ...schemas import CODEC
from ..shared import ValidatingSchema

__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
]


@CODEC.register_mapping(AssignResourcesRequest)
class AssignResourcesRequestSchema(
    ValidatingSchema
):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesRequest class.
    """

    interface = fields.String()
    transaction_id = fields.String(data_key="transaction_id")
    subarray_id = fields.Integer(data_key="subarray_id")
    dish = fields.Nested(DishAllocationSchema)
    sdp_config = fields.Nested(SDPConfigurationSchema, data_key="sdp")
    csp_config = fields.Nested(CSPConfigurationSchema, data_key="csp")
    mccs = fields.Nested(MCCSAllocateSchema)

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
        interface = data.get("interface", None)
        transaction_id = data.get("transaction_id", None)
        subarray_id = data.get("subarray_id", None)
        dish_allocation = data.get("dish", None)
        sdp_config = data.get("sdp_config", None)
        csp_config = data.get("csp_config", None)
        mccs = data.get("mccs", None)

        return AssignResourcesRequest(
            interface=interface,
            transaction_id=transaction_id,
            subarray_id=subarray_id,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            csp_config=csp_config,
            mccs=mccs,
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CBF configuration
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
