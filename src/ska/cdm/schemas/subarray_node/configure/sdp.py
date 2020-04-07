"""
This module defines Marshmallow schemas that map CDM the message classes for
SDP configuration to and from a JSON representation.
"""

from marshmallow import Schema, fields, post_load

import ska.cdm.messages.subarray_node.configure as configure_msgs

__all__ = ['SDPConfigurationSchema']


class SDPConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow class for the SDPConfiguration class
    """
    scan_type = fields.String(data_key="scan_type")

    @post_load
    def create_sdp_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a set containing all the scans
        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration instance populated to match JSON
        """
        return configure_msgs.SDPConfiguration(**data)
