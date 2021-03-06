"""
The schemas module defines Marshmallow schemas that map shared CDM message
classes for SubArrayNode configuration to/from a JSON representation.
"""
import collections
import copy

from marshmallow import Schema, fields, post_dump, post_load, pre_dump
from marshmallow.validate import OneOf

from ska.cdm.messages.subarray_node.configure import ConfigureRequest
import ska.cdm.messages.subarray_node.configure.core as configure_msgs
from . import csp, sdp, tmc, mccs
from ... import CODEC, shared

__all__ = [
    "ConfigureRequestSchema",
    "DishConfigurationSchema",
    "PointingSchema",
    "TargetSchema",
]

JsonTarget = collections.namedtuple("JsonTarget", "ra dec frame name")


class TargetSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Target class
    """

    ra = fields.String(data_key="RA")
    dec = fields.String()
    frame = shared.UpperCasedField(data_key="system")
    name = fields.String()

    @pre_dump
    def convert_to_icrs(
        self, target: configure_msgs.Target, **_
    ):  # pylint: disable=no-self-use
        """
        Process Target co-ordinates by converting them to ICRS frame before
        the JSON marshalling process begins.

        :param target: Target instance to process
        :param _: kwargs passed by Marshallow
        :return: SexagesimalTarget with ICRS ra/dec expressed in hms/dms
        """
        # All pointing coordinates are in ICRS
        icrs_coord = target.coord.transform_to("icrs")
        hms, dms = icrs_coord.to_string("hmsdms", sep=":").split(" ")
        sexagesimal = JsonTarget(
            ra=hms, dec=dms, frame=icrs_coord.frame.name, name=target.name
        )

        return sexagesimal

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        name = data["name"]
        hms = data["ra"]
        dms = data["dec"]
        frame = data["frame"]
        target = configure_msgs.Target(
            hms, dms, frame=frame, name=name, unit=("hourangle", "deg")
        )
        return target


class PointingSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Pointing class.
    """

    target = fields.Nested(TargetSchema)

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a subarray_node.Pointing object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Pointing instance populated to match JSON
        """
        target = data["target"]
        return configure_msgs.PointingConfiguration(target)


class DishConfigurationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.DishConfiguration class.
    """

    receiver_band = fields.String(
        data_key="receiverBand", required=True, validate=OneOf(["1", "2", "5a", "5b"])
    )

    @pre_dump
    def convert(
        self, dish_configuration: configure_msgs.DishConfiguration, **_
    ):  # pylint: disable=no-self-use
        """
        Process DishConfiguration instance so that it is ready for conversion
        to JSON.

        :param dish_configuration: the dish configuration
        :param _: kwargs passed by Marshmallow
        :return: DishConfiguration instance populated to match JSON
        """
        # Convert Python Enum to its string value
        copied = copy.deepcopy(dish_configuration)
        copied.receiver_band = dish_configuration.receiver_band.value
        return copied

    @post_load
    def create_dish_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Converted parsed JSON back into a subarray_node.DishConfiguration
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishConfiguration instance populated to match JSON
        """
        receiver_band = data["receiver_band"]
        enum_obj = configure_msgs.ReceiverBand(receiver_band)
        return configure_msgs.DishConfiguration(enum_obj)


@CODEC.register_mapping(ConfigureRequest)
class ConfigureRequestSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.ConfigureRequest class.
    """

    pointing = fields.Nested(PointingSchema)
    dish = fields.Nested(DishConfigurationSchema)
    sdp = fields.Nested(sdp.SDPConfigurationSchema)
    csp = fields.Nested(csp.CSPConfigurationSchema)
    tmc = fields.Nested(tmc.TMCConfigurationSchema)
    mccs = fields.Nested(mccs.MCCSConfigurationSchema)

    @post_load
    def create_configuration(self, data, **_):  # pylint: disable=no-self-use
        """
        Converted parsed JSON backn into a subarray_node.ConfigureRequest
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ConfigurationRequest instance populated to match JSON
        """
        pointing = data.get("pointing", None)
        dish = data.get("dish", None)
        sdp = data.get("sdp", None)
        csp = data.get("csp", None)
        tmc = data.get("tmc", None)
        mccs = data.get("mccs", None)
        return ConfigureRequest(
            pointing=pointing, dish=dish, sdp=sdp, csp=csp, mccs=mccs, tmc=tmc,
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        return {k: v for k, v in data.items() if v is not None}
