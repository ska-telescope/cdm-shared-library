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
    ResourceConfiguration,
)
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "CSPConfigurationSchema",
    "CommonConfigurationSchema",
    "ResourceConfigurationSchema",
    "LowCbfConfigurationSchema",
]


@CODEC.register_mapping(CommonConfiguration)
class CommonConfigurationSchema(Schema):
    """
    Marsmallow class for the common subarray id field
    of CommonConfigurationSchema
    """

    subarray_id = fields.Integer(metadata={"require": True})

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for Common configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_common_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a CSPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration object populated from data
        """
        return CommonConfiguration(**data)


@CODEC.register_mapping(ResourceConfiguration)
class ResourceConfigurationSchema(Schema):
    """
    Marsmallow class for the resources field
    of ResourceConfigurationSchema
    """

    device = fields.String(metadata={"require": True})
    shared = fields.Boolean(metadata={"require": True})
    fw_image = fields.String(metadata={"require": True})
    fw_mode = fields.String(metadata={"require": True})

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for Resource configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_resource_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ResourceConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ResourceConfiguration object populated from data
        """
        return ResourceConfiguration(**data)


@CODEC.register_mapping(LowCbfConfiguration)
class LowCbfConfigurationSchema(Schema):
    """
    Marsmallow class of LowCbfConfigurationSchema
    """

    resources = fields.List(
        fields.Nested(ResourceConfigurationSchema), metadata={"require": True}
    )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for LowCbf configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_lowcbf_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a LowCbfConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: LowCbfConfiguration object populated from data
        """
        return LowCbfConfiguration(**data)


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
        :return: dict suitable for CSP configuration
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
