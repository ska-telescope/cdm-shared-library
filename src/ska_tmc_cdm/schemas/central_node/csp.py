"""
The module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation
for the TMC CentralNode.AssignResources command.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_tmc_cdm.messages.central_node.csp import (
    CommonConfiguration,
    CSPConfiguration,
    LowCbfConfiguration,
    ResourcesConfiguration,
)
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "CSPConfigurationSchema",
    "CommonConfigurationSchema",
    "ResourcesConfigurationSchema",
    "LowCbfConfigurationSchema",
]


@CODEC.register_mapping(CommonConfiguration)
class CommonConfigurationSchema(Schema):
    """
    Marsmallow class for the common subarray id field
    of CommonConfigurationSchema
    """

    subarray_id = fields.Integer(metadata={"require": True})


@CODEC.register_mapping(ResourcesConfiguration)
class ResourcesConfigurationSchema(Schema):
    """
    Marsmallow class for the resources field
    of ResourcesConfigurationSchema
    """

    device = fields.String(metadata={"require": True})
    shared = fields.Boolean(metadata={"require": True})
    fw_image = fields.String(metadata={"require": True})
    fw_mode = fields.String(metadata={"require": True})


@CODEC.register_mapping(LowCbfConfiguration)
class LowCbfConfigurationSchema(Schema):
    """
    Marsmallow class of LowCbfConfigurationSchema
    """

    resources = fields.List(
        fields.Nested(ResourcesConfigurationSchema), metadata={"require": True}
    )


@CODEC.register_mapping(CSPConfiguration)
class CSPConfigurationSchema(Schema):
    """
    Marsmallow class for the CSPConfiguration class
    """

    interface = fields.String(metadata={"require": True})
    common = fields.Nested(
        CommonConfigurationSchema, data_key="common", metadata={"require": True}
    )
    lowcbf = fields.Nested(
        LowCbfConfigurationSchema, data_key="lowcbf", metadata={"require": True}
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
