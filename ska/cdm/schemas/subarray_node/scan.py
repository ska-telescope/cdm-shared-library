"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
from datetime import timedelta

from marshmallow import Schema, fields, post_load, pre_dump

import ska.cdm.messages.subarray_node.scan as scan_msgs
from ska.cdm.schemas import CODEC

__all__ = ['ScanRequestSchema']


@CODEC.register_mapping(scan_msgs.ScanRequest)
class ScanRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """
    scan_duration = fields.Float(data_key='scanDuration')

    @pre_dump
    def convert_to_scan(self, data, **_):  # pylint: disable=no-self-use
        """
        Process scan_duration and converted it to a float

        :param data: the scan_duration timedelta
        :param _: kwargs passed by Marshallow
        :return: float converted
        """
        duration = data.scan_duration
        in_secs = duration.total_seconds()
        data.scan_duration = in_secs
        return data

    @post_load
    def create_scan_request(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanRequest instance populated to match JSON
        """
        t_to_scan = timedelta(seconds=data['scan_duration'])
        scan_request = scan_msgs.ScanRequest(t_to_scan)
        return scan_request
