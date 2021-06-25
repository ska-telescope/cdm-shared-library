"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""

from marshmallow import fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas.central_node.common import (
    DishAllocationSchema,
)
from ..shared import ValidatingSchema
from ...schemas import CODEC

__all__ = [
    "ReleaseResourcesRequestSchema",
]


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(ValidatingSchema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    interface = fields.String()
    transaction_id = fields.String()
    subarray_id = fields.Integer()
    release_all = fields.Boolean()
    dish = fields.Nested(DishAllocationSchema)

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
        from the request.
        If release_all for MID set to False, the 'release_all' key
        itself should be stripped.
        If release_all_low for LOW set to False, the 'release_all_low' key
        itself should be stripped.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for request submission
        """
        # If release_all_mid is True, other resources should be stripped - and
        # vice versa

        is_low = data.get('subarray_id', None) is not None and \
                 data.get('interface', None) is not None and \
                 'low' in data['interface']
        if not is_low:

            # for MID, remove dish specifier when release all is True and vice
            # versa. We do not need to strip partial resources for LOW as only
            # full release is allowed.
            if data["release_all"]:
                del data["dish"]
            else:
                del data["release_all"]

        # Filter out  null values from JSON.
        data = {k: v for k, v in data.items() if v is not None}

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
        interface = data.get("interface", None)
        transaction_id = data.get("transaction_id", None)
        subarray_id = data.get("subarray_id", None)
        release_all = data.get("release_all", False)
        dish_allocation = data.get("dish", None)

        return ReleaseResourcesRequest(
            interface=interface,
            transaction_id=transaction_id,
            subarray_id=subarray_id,
            release_all=release_all,
            dish_allocation=dish_allocation,
        )
