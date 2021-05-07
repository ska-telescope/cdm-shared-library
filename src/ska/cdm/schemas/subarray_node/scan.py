"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""

from marshmallow import fields, post_load, post_dump

import ska.cdm.messages.subarray_node.scan as scan_msgs
from ska.cdm.schemas import CODEC
from ska.cdm.schemas.shared import ValidatingSchema

__all__ = ["ScanRequestSchema"]


@CODEC.register_mapping(scan_msgs.ScanRequest)
class ScanRequestSchema(ValidatingSchema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """

    interface = fields.String()
    # holds scan ID for MID
    id = fields.Integer()
    # holds scan ID for LOW
    scan_id = fields.Integer()

    @post_load
    def create_scan_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """

        is_low = 'low' in data.get("interface", '')
        if is_low:
            scan_id = data["scan_id"]
            interface = data["interface"]
        else:
            scan_id = data["id"]
            interface = None

        return scan_msgs.ScanRequest(
            scan_id=scan_id,
            interface=interface
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

        # set scan ID key name appropriately for telescope
        is_low = 'low' in data.get('interface', '')
        if not is_low:
            data['id'] = data['scan_id']
            del data['scan_id']

        return data
