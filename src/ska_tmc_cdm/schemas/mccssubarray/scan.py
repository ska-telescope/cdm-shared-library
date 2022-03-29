"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""

from marshmallow import fields, post_load

from ska_tmc_cdm.messages.mccssubarray.scan import ScanRequest
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.schemas.shared import ValidatingSchema

__all__ = ["ScanRequestSchema"]


@CODEC.register_mapping(ScanRequest)
class ScanRequestSchema(ValidatingSchema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanRequest
    """

    interface = fields.Str(require=True)
    scan_id = fields.Integer(required=True)
    start_time = fields.Float(required=True)

    @post_load
    def create_scanrequest(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """
        interface = data["interface"]
        scan_id = data["scan_id"]
        start_time = data["start_time"]

        return ScanRequest(interface=interface, scan_id=scan_id, start_time=start_time)
