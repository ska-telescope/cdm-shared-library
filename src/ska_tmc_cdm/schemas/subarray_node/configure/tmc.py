"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
import copy
from datetime import timedelta

from marshmallow import Schema, fields, post_dump, post_load, pre_dump, pre_load

from ska_tmc_cdm.jsonschema.json_schema import JsonSchema
from ska_tmc_cdm.messages.subarray_node.configure.tmc import TMCConfiguration
from ska_tmc_cdm.schemas import CODEC

__all__ = ["TMCConfigurationSchema"]


@CODEC.register_mapping(TMCConfiguration)
class TMCConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Create the Schema for ScanDuration using timedelta
    """

    scan_duration = fields.Float()

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
        scan_duration = timedelta(seconds=data.get("scan_duration"))

        tmc_config = TMCConfiguration(scan_duration=scan_duration)
        return tmc_config

    @pre_load
    def validate_schema(self, data, **_):  # pylint: disable=no-self-use
        """
        validating the structure of JSON against schemas

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for CSP configuration
        """
        self.validate_json(data)
        return data

    @post_dump
    def filter_nulls_and_validate_schema(
        self, data, **_
    ):  # pylint: disable=no-self-use
        """
        validating the structure of JSON against schemas and
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        data = {k: v for k, v in data.items() if v is not None}

        # ~ self.validate_json(data, lambda x: _convert_tuples_to_lists(x)) # Do we need this?
        self.validate_json(data)
        return data

    def validate_json(self, data, process_fn=lambda x: x):
        """
        validating the structure of JSON against schemas

        :param data: Marshmallow-provided dict containing parsed object values
        :param lambda function: use for converting list of tuples to list of list
        :return:
        """
        # return early unless custom_validate is defined and True
        if not self.context.get("custom_validate", False):
            return

        interface = data.get("interface", None)
        if interface:
            JsonSchema.validate_schema(interface, process_fn(data))
