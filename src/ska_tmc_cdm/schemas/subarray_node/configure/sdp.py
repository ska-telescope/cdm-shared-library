"""
This module defines Marshmallow schemas that map the SDPConfiguration message
classes to/from JSON.
"""

from marshmallow import Schema, fields, post_load

from ska_tmc_cdm.messages.subarray_node.configure.sdp import SDPConfiguration
from ska_tmc_cdm.schemas import CODEC
from ska_tmc_cdm.jsonschema.json_schema import JsonSchema

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

