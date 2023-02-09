"""
This module defines Marshmallow schemas that map the SDPConfiguration message
classes to/from JSON.
"""

from marshmallow import Schema, fields, post_dump, post_load, pre_load

from ska_tmc_cdm.jsonschema.json_schema import JsonSchema
from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.schemas import CODEC

__all__ = ["SDPConfigurationSchema"]


@CODEC.register_mapping(SDPConfiguration)
class SDPConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow class for the SDPConfiguration class
    """

    interface = fields.String()
    scan_type = fields.String()

    @post_load
    def create_sdp_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set containing all the scans
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration instance populated to match JSON
        """
        return SDPConfiguration(**data)

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
