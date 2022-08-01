from marshmallow import fields, post_load

from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescope

from ...schemas import CODEC
from ..shared import ValidatingSchema


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
