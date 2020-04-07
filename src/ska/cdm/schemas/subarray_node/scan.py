"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""

from marshmallow import Schema, fields, post_load

import ska.cdm.messages.subarray_node.scan as scan_msgs
from ska.cdm.schemas import CODEC

__all__ = ["ScanRequestSchema"]


@CODEC.register_mapping(scan_msgs.ScanRequest)
class ScanRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """

    scan_id = fields.Integer(data_key="id")

    @post_load
    def create_scan_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """
        scan_id = data["scan_id"]
        return scan_msgs.ScanRequest(scan_id)
