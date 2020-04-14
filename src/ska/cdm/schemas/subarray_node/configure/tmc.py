"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
from datetime import timedelta

from marshmallow import Schema, fields, post_load, pre_dump

from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska.cdm.schemas import CODEC

__all__ = ["TMCConfigurationSchema"]


@CODEC.register_mapping(TMCConfiguration)
class TMCConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """
    scan_duration = fields.Float(data_key='scanDuration')

    @pre_dump
    def convert_scan_duration_timedelta_to_float(self, data, **_):  # pylint: disable=no-self-use
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
    def convert_scan_duration_number_to_timedelta(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a TMConfiguration

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: TMCConfiguration instance populated to match JSON
        """
        t_to_scan = timedelta(seconds=data.get("scan_duration"))
        tmc_config = TMCConfiguration(t_to_scan)
        return tmc_config
