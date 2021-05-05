"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""

from marshmallow import fields, post_dump, post_load

from ska.cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska.cdm.schemas.central_node.common import (
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
    subarray_id_low = fields.Integer(data_key="subarray_id")
    subarray_id_mid = fields.Integer(data_key="subarrayID")
    release_all_mid = fields.Boolean(data_key="releaseALL")
    release_all_low = fields.Boolean(data_key="release_all")
    dish = fields.Nested(DishAllocationSchema)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Marshmallow directives for ReleaseResourcesRequestSchema.
        """

        ordered = True

    @post_dump
    def filter_args(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter Marshmallow's JSON based on the value of release_all_mid.

        If release_all_mid is True, other resource definitions should be stripped
        from the request.
        If release_all_mid for MID set to False, the 'release_all_mid' key
        itself should be stripped.
        If release_all_low for LOW set to False, the 'release_all_low' key
        itself should be stripped.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for request submission
        """
        # If release_all_mid is True, other resources should be stripped - and
        # vice versa

        # Filter out  null values from JSON.
        data = {k: v for k, v in data.items() if v is not None}

        is_low = "low" in data.get("interface", "")
        if is_low:
            to_remove = ["releaseALL", "subarrayID", "dish"]
        else:
            to_remove = ["release_all", "subarray_id"]

            # for MID, also need to remove dish specifier when release all is
            # True. We do not need to strip partial resources for LOW as only full
            # release is allowed.
            release_all_mid = data.get("releaseALL", None)
            if release_all_mid is True:
                to_remove.append("dish")
            else:
                to_remove.append("releaseALL")

        for key in to_remove:
            if key in data:
                del data[key]

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
        subarray_id_mid = data.get("subarray_id_mid", None)
        release_all_mid = data.get("release_all_mid", False)
        dish_allocation = data.get("dish", None)
        interface = data.get("interface", None)
        subarray_id_low = data.get("subarray_id_low", None)
        release_all_low = data.get("release_all_low", False)

        return ReleaseResourcesRequest(
            interface=interface,
            subarray_id_low=subarray_id_low,
            subarray_id_mid=subarray_id_mid,
            dish_allocation=dish_allocation,
            release_all_low=release_all_low,
            release_all_mid = release_all_mid
        )
