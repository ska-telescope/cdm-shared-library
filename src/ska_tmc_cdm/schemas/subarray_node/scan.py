"""
The ska_tmc_cdm.schemas.subarray_node.scan module contains Marshmallow schema
that map ska_tmc_cdm.schemas.subarray_node.scan message classes to/from JSON.
"""

from marshmallow import fields, post_dump, post_load

from ska_tmc_cdm.messages.subarray_node.scan import ScanRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.shared import ValidatingSchema

__all__ = ["ScanRequestSchema"]


@CODEC.register_mapping(ScanRequest)
class ScanRequestSchema(ValidatingSchema):  # pylint: disable=too-few-public-methods
    """
    ScanRequestSchema is the Marshmallow schema that marshals a ScanRequest
    to/from JSON.
    """

    # Message metadata and tracing fields ------------------------------------

    # schema ID, e.g., https://schema.skao.int/ska-tmc-scan/1.0
    interface = fields.String()
    # optional transaction ID, used to trace commands through the system
    transaction_id = fields.String(required=False)

    # Message content fields -------------------------------------------------

    # holds numeric scan ID
    scan_id = fields.Integer()

    @post_load
    def create_scanrequest(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """
        interface = data["interface"]
        transaction_id = data.get("transaction_id", None)
        scan_id = data["scan_id"]

        return ScanRequest(
            interface=interface, transaction_id=transaction_id, scan_id=scan_id
        )

    @post_dump
    def filter_nulls(self, data, **_):
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        # filter out nulls
        data = {k: v for k, v in data.items() if v is not None}

        return data
