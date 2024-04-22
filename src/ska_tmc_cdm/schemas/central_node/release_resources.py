"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
import json

from marshmallow import fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.release_resources import (
    ReleaseResourcesRequest,
)
from ska_tmc_cdm.schemas.central_node.common import DishAllocationSchema

from ...schemas import CODEC
from ..shared import ValidatingSchema

__all__ = [
    "ReleaseResourcesRequestSchema",
]


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(ValidatingSchema):
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    interface = fields.String()
    transaction_id = fields.String()
    subarray_id = fields.Integer()
    release_all = fields.Boolean()
    dish = fields.Pluck(
        DishAllocationSchema, "receptor_ids", data_key="receptor_ids"
    )

    class Meta:
        """
        Marshmallow directives for ReleaseResourcesRequestSchema.
        """

        ordered = True

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

    @post_dump
    def validate_on_dump(self, data, **_):  # pylint: disable=arguments-differ
        """
        Validating the structure of JSON against schemas and
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """

        # filter out null values from JSON
        data = {k: v for k, v in data.items() if v is not None}
        # MID and LOW still have different schema for PI11. Eventually these
        # schemas will be unified into a single schema, but for now we need
        # to detect the difference and do some special handling.
        is_mid = "ska-tmc-low" not in data["interface"]

        if is_mid:
            # for MID, remove dish specifier when release all is True and vice
            # versa. We do not need to strip partial resources for LOW as only
            # full release is allowed.
            # TODO : - When the receptor Ids will be added into the telemodel library for
            #  MID release resource command when release_all = False  then we need to remove below if condition
            if not data["release_all"]:
                temp_receptor_id = data["receptor_ids"]
                del data["receptor_ids"]

        # convert tuples to lists
        data = json.loads(json.dumps(data))
        data = super().validate_on_dump(data)
        # TODO : - When the receptor Ids will be added into the telemodel library for
        #  MID release resource command when release_all = False  then we need to remove below if condition
        if is_mid and not data["release_all"]:
            data["receptor_ids"] = temp_receptor_id
        return data
