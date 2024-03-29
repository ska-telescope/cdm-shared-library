"""
This module defines Marshmallow schemas that map the CDM classes for
SubArrayNode MCCS configuration to/from JSON.
"""
from marshmallow import Schema, fields, post_load

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget,
)
from ska_tmc_cdm.schemas import CODEC

__all__ = [
    "MCCSConfigurationSchema",
    "StnConfigurationSchema",
    "SubarrayBeamConfigurationSchema",
    "SubarrayBeamTargetSchema",
]

from ska_tmc_cdm.schemas.shared import ValidatingSchema


@CODEC.register_mapping(SubarrayBeamTarget)
class SubarrayBeamTargetSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Target class
    """

    az = fields.Float(data_key="az", required=True)
    el = fields.Float(data_key="el", required=True)
    target_name = fields.String(data_key="target_name", required=True)
    reference_frame = fields.String(data_key="reference_frame", required=True)

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        az = data["az"]
        el = data["el"]
        target_name = data["target_name"]
        reference_frame = data["reference_frame"]
        return SubarrayBeamTarget(
            az=az, el=el, target_name=target_name, reference_frame=reference_frame
        )


@CODEC.register_mapping(StnConfiguration)
class StnConfigurationSchema(Schema):
    station_id = fields.Integer(data_key="station_id", required=True)

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a StnConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: StnConfiguration instance populated to match JSON
        :rtype: StnConfiguration
        """
        station_id = data["station_id"]
        return StnConfiguration(station_id)


@CODEC.register_mapping(SubarrayBeamConfiguration)
class SubarrayBeamConfigurationSchema(Schema):
    subarray_beam_id = fields.Integer(data_key="subarray_beam_id", required=True)
    station_ids = fields.List(fields.Integer(data_key="station_ids", required=True))
    channels = fields.List(fields.List(fields.Integer), data_key="channels")
    update_rate = fields.Float(data_key="update_rate")
    target = fields.Nested(SubarrayBeamTargetSchema, data_key="target")
    antenna_weights = fields.List(fields.Float(data_key="antenna_weights"))
    phase_centre = fields.List(fields.Float(data_key="phase_centre"))

    @post_load
    def create(self, data, **_) -> SubarrayBeamConfiguration:
        """
         Convert parsed JSON back into a SubarrayBeamConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayBeamConfiguration instance populated to match JSON
        """
        subarray_beam_id = data["subarray_beam_id"]
        station_ids = data["station_ids"]
        channels = data["channels"]
        update_rate = data["update_rate"]
        target = data["target"]
        antenna_weights = data["antenna_weights"]
        phase_centre = data["phase_centre"]

        return SubarrayBeamConfiguration(
            subarray_beam_id=subarray_beam_id,
            station_ids=station_ids,
            channels=channels,
            update_rate=update_rate,
            target=target,
            antenna_weights=antenna_weights,
            phase_centre=phase_centre,
        )


@CODEC.register_mapping(MCCSConfiguration)
class MCCSConfigurationSchema(ValidatingSchema):
    """
    Marshmallow schema for the subarray_node.MCCSConfiguration class
    """

    station_configs = fields.Nested(
        StnConfigurationSchema, many=True, data_key="stations"
    )
    subarray_beam_configs = fields.Nested(
        SubarrayBeamConfigurationSchema, many=True, data_key="subarray_beams"
    )

    @post_load
    def create(self, data, **_):
        """
         Convert parsed JSON back into a MCCSConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSConfiguration instance populated to match JSON
        :rtype: MCCSConfiguration
        """
        stn_configs = data["station_configs"]
        subarray_beam_configs = data["subarray_beam_configs"]
        return MCCSConfiguration(
            station_configs=stn_configs, subarray_beam_configs=subarray_beam_configs
        )
