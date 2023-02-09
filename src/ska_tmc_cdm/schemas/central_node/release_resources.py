"""
The schemas.central_node module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""

from marshmallow import fields, post_dump, post_load, pre_load

from ska_tmc_cdm.jsonschema.json_schema import JsonSchema
from ska_tmc_cdm.messages.central_node.release_resources import ReleaseResourcesRequest
from ska_tmc_cdm.schemas.central_node.common import DishAllocationSchema

from ...schemas import CODEC
from ..shared import ValidatingSchema

__all__ = [
    "ReleaseResourcesRequestSchema",
]


@CODEC.register_mapping(ReleaseResourcesRequest)
class ReleaseResourcesRequestSchema(
    ValidatingSchema
):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the ReleaseResourcesRequest class.
    """

    interface = fields.String()
    transaction_id = fields.String()
    subarray_id = fields.Integer()
    release_all = fields.Boolean()
    dish = fields.Pluck(DishAllocationSchema, "receptor_ids", data_key="receptor_ids")

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

        # MID and LOW still have different schema for PI11. Eventually these
        # schemas will be unified into a single schema, but for now we need
        # to detect the difference and do some special handling.
        is_mid = "ska-tmc-low" not in data["interface"]
        if is_mid:
            # for MID, remove dish specifier when release all is True and vice
            # versa. We do not need to strip partial resources for LOW as only
            # full release is allowed.
            if data["release_all"]:
                del data["receptor_ids"]

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

    @pre_load
    def validate_schema(self, data, **_):  # pylint: disable=no-self-use
        """
        validating the structure of JSON against schemas

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CSP configuration
        """
        if data.get("release_all") and data["release_all"] == False:
            temp_receptor_id = data["receptor_ids"]
            del data["receptor_ids"]
            # ~ self.validate_json(data, lambda x: _convert_tuples_to_lists(x)) # Do we need this?
            self.validate_json(data)
            data["receptor_ids"] = temp_receptor_id
        else:
            self.validate_json(data)
        return data

    @post_dump
    def filter_nulls_and_validate_schema(
        self, data, **_
    ):  # pylint: disable=no-self-use
        """
        validating the structure of JSON against schemas and
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        data = {k: v for k, v in data.items() if v is not None}
        if data.get("release_all") and data["release_all"] == False:
            temp_receptor_id = data["receptor_ids"]
            del data["receptor_ids"]
            # ~ self.validate_json(data, lambda x: _convert_tuples_to_lists(x)) # Do we need this?
            self.validate_json(data)
            data["receptor_ids"] = temp_receptor_id
        else:
            self.validate_json(data)
        return data

    def validate_json(self, data, process_fn=lambda x: x):
        """
        validating the structure of JSON against schemas

        :param data: Marshmallow-provided dict containing parsed object values
        :param lambda function: use for converting list of tuples to list of list
        :return:
        """
        # return early unless custom_validate is defined and True
        if not self.context.get("custom_validate", False):
            return
        interface = data.get("interface", None)
        if interface:
            JsonSchema.validate_schema(interface, process_fn(data))
