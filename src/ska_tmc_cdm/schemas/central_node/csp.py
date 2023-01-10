"""
The module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation
for the TMC CentralNode.AssignResources command.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.csp import CSPConfiguration
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "CSPConfigurationSchema",
]


class Resources(Schema):
    """
    Marsmallow class for the resources field
    of CSPConfigurationSchema
    """

    device = fields.String(metadata={"require": True})
    shared = fields.Boolean(metadata={"require": True})
    fw_image = fields.String(metadata={"require": True})
    fw_mode = fields.String(metadata={"require": True})


@CODEC.register_mapping(CSPConfiguration)
class CSPConfigurationSchema(Schema):
    """
    Marsmallow class for the CSPConfiguration class
    """

    interface = fields.String(metadata={"require": True})
    common = fields.Dict(
        keys=fields.String(), values=fields.Int(), metadata={"require": True}
    )
    lowcbf = fields.Dict(
        keys=fields.String(),
        values=fields.List(fields.Dict),
        metadata={"require": True},
    )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_csp_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a CSPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration object populated from data
        """
        return CSPConfiguration(**data)
