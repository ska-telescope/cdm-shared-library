import json

from marshmallow import fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescope

from ...schemas import CODEC
from ..shared import ValidatingSchema

__all__ = ["StartTelescopeSchema"]
@CODEC.register_mapping(StartTelescope)
class StartTelescopeSchema(ValidatingSchema):
    transaction_id = fields.String(data_key="transaction_id")
    subarray_id = fields.Integer(data_key="subarray_id")

    class Meta:
        """
        marshmallow directives for StartTelescopeSchema.
        """

        ordered = True

    @post_load
    def create_request(self, data, **_):
        transaction_id = data.get("transaction_id", None)
        subarray_id = data.get("subarray_id", None)

        return StartTelescope(subarray_id=subarray_id, transaction_id=transaction_id)

    @post_dump
    def validate_on_dump(self, data, **_):  # pylint: disable=arguments-differ
        """
        Validating the structure of JSON against schemas and
        Filter out null values from JSON
        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """

        # filter out nulls
        data = {k: v for k, v in data.items() if v is not None}

        # convert tuples to lists
        data = json.loads(json.dumps(data))

        data = super().validate_on_dump(data)
        return data
