"""
The schemas module defines Marshmallow schemas that map CDM message classes
and data model classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska.cdm.messages import subarray_node as sn
from ska.cdm.schemas.codec import CODEC
from ska.cdm.schemas.subarray_node.configure.core import *
from ska.cdm.schemas.subarray_node.configure.csp import *
from ska.cdm.schemas.subarray_node.configure.sdp import *


@CODEC.register_mapping(sn.ConfigureRequest)
class ConfigureRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.ConfigureRequest class.
    """

    scan_id = fields.Integer(required=True, data_key='scanID')
    pointing = fields.Nested(PointingSchema)
    dish = fields.Nested(DishConfigurationSchema)
    sdp = fields.Nested(SDPConfigurationSchema)
    csp = fields.Nested(CSPConfigurationSchema)

    @post_load
    def create_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Converted parsed JSON backn into a subarray_node.ConfigureRequest
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ConfigurationRequest instance populated to match JSON
        """
        return sn.ConfigureRequest(**data)
