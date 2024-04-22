"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
import copy
from datetime import timedelta

from marshmallow import Schema, fields, post_dump, post_load, pre_dump

from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska_tmc_cdm.schemas import CODEC

__all__ = ["TMCConfigurationSchema"]


@CODEC.register_mapping(TMCConfiguration)
class TMCConfigurationSchema(Schema):
    """
    Create the Schema for ScanDuration using timedelta
    """

    scan_duration = fields.Float()
    partial_configuration = fields.Boolean()

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
        if data.scan_duration:
            in_secs = data.scan_duration.total_seconds()
            copied.scan_duration = in_secs
        return copied

    @post_dump
    def omit_default_values_from_configuration(self, data, **_):
        """
        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict output for JSON serialization
        """
        # For compatibility, if partial_configuration=False (the default value)
        # then we omit it from the output. ~2023-10-6
        # Revisit this choice in future?
        if data["partial_configuration"] is False:
            del data["partial_configuration"]
        if data["scan_duration"] is None:
            del data["scan_duration"]

        return data

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
        scan_duration = data.get("scan_duration")
        if scan_duration:
            scan_duration_td = timedelta(seconds=scan_duration)
        else:
            scan_duration_td = None

        tmc_config = TMCConfiguration(
            scan_duration=scan_duration_td,
            partial_configuration=data.get("partial_configuration", False),
        )
        return tmc_config
