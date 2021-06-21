"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load
import json
from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesRequest
from ska_tmc_cdm.messages.central_node.assign_resources import AssignResourcesResponse
from ska_tmc_cdm.schemas.central_node.common import (
    DishAllocationSchema,
    DishAllocationResponseSchema,
)
from ska_tmc_cdm.schemas.central_node.mccs import MCCSAllocateSchema
from ska_tmc_cdm.schemas.central_node.sdp import SDPConfigurationSchema
from ..shared import ValidatingSchema
from ...schemas import CODEC

__all__ = [
    "AssignResourcesRequestSchema",
    "AssignResourcesResponseSchema",
]


@CODEC.register_mapping(AssignResourcesRequest)
class AssignResourcesRequestSchema(ValidatingSchema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the AssignResourcesRequest class.
    """

    interface = fields.String()
    subarray_id = fields.Integer()
    subarray_id_mid = fields.Integer(data_key="subarrayID")
    dish = fields.Nested(DishAllocationSchema)
    sdp_config = fields.Nested(SDPConfigurationSchema, data_key="sdp")
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
        subarray_id = data.get("subarray_id", None)
        subarray_id_mid = data.get("subarray_id_mid", None)
        dish_allocation = data.get("dish", None)
        sdp_config = data.get("sdp_config", None)
        mccs = data.get("mccs", None)

        is_low = subarray_id is not None and interface is not None

        if not is_low:
            subarray_id = subarray_id_mid

        return AssignResourcesRequest(
            interface=interface,
            subarray_id=subarray_id,
            dish_allocation=dish_allocation,
            sdp_config=sdp_config,
            mccs=mccs
        )

    @post_dump
    def validate_on_dump(self, data, **_):
        """
        Validating the structure of JSON against schemas and
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        is_low = data.get('subarray_id', None) is not None and \
                 data.get('interface', None) is not None and \
                 'low' in data['interface']
        if not is_low:
            data['subarrayID'] = data['subarray_id']
            del data['subarray_id']

        # filter out nulls
        data = {k: v for k, v in data.items() if v is not None}

        # convert tuples to lists
        data = json.loads(json.dumps(data))

        data = super().validate_on_dump(data)
        return data


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
