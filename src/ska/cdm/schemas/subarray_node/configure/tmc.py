"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
import copy
from datetime import timedelta

from marshmallow import Schema, fields, post_load, pre_dump, post_dump

from ska.cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska.cdm.schemas import CODEC

__all__ = ["TMCConfigurationSchema"]


@CODEC.register_mapping(TMCConfiguration)
class TMCConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """

    scan_duration = fields.Float()
    scanDuration = fields.Float()

    @pre_dump
    def convert_scan_duration_timedelta_to_float(
        self, data: TMCConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process scan_duration and convert it to a float

        :param data: the scan_duration timedelta
        :param _: kwargs passed by Marshallow
        :return: float converted
        """
        copied = copy.deepcopy(data)
        in_secs = data.scan_duration.total_seconds()
        copied.scan_duration = in_secs
        return copied

    @pre_dump
    def do_it(self, o: TMCConfiguration, **_):
        o = copy.deepcopy(o)
        if o.is_ska_mid:
            o.scanDuration = o.scan_duration
            delattr(o, 'scan_duration')
        return o

    @post_load
    def convert_scan_duration_number_to_timedelta(
        self, data, **_
    ):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a TMConfiguration

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: TMCConfiguration instance populated to match JSON
        """
        is_low = 'scan_duration' in data
        is_mid = 'scanDuration' in data

        if is_low:
            scan_duration = timedelta(seconds=data.get('scan_duration'))
        if is_mid:
            scan_duration = timedelta(seconds=data.get('scanDuration'))

        tmc_config = TMCConfiguration(
            scan_duration=scan_duration, is_ska_mid=is_mid
        )
        return tmc_config
