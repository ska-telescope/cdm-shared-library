from marshmallow import fields, post_load

from ska_tmc_cdm.messages.central_node.telescope_start import StartTelescopeRequest

from ...schemas import CODEC
from ..shared import ValidatingSchema

__all__ = ["StartTelescopeRequestSchema"]


@CODEC.register_mapping(StartTelescopeRequest)
class StartTelescopeRequestSchema(ValidatingSchema):
    subarray_id = fields.Integer(data_key="subarray_id")
    interface = fields.String(data_key="interface")
    transaction_id = fields.String(data_key="transaction_id")

    class Meta:
        """
        marshmallow directives for StartTelescopeSchema.
        """

        ordered = True

    @post_load
    def create_request(self, data, **_):
        subarray_id = data.get("subarray_id", None)
        interface = data.get("interface", None)
        transaction_id = data.get("transaction_id", None)
        return StartTelescopeRequest(
            subarray_id=subarray_id, interface=interface, transaction_id=transaction_id
        )
