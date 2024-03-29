"""
The schemas module defines Marshmallow schemas that map shared CDM message
classes for SubArrayNode configuration to/from a JSON representation.
"""
import collections
import copy

from marshmallow import Schema, fields, post_dump, post_load, pre_dump
from marshmallow.validate import OneOf

import ska_tmc_cdm.messages.subarray_node.configure.core as configure_msgs
from ska_tmc_cdm.messages.subarray_node.configure import ConfigureRequest

from ... import CODEC, shared
from . import csp, mccs, sdp, tmc

__all__ = [
    "ConfigureRequestSchema",
    "DishConfigurationSchema",
    "PointingSchema",
    "TargetSchema",
]

JsonTarget = collections.namedtuple(
    "JsonTarget", "ra dec reference_frame target_name ca_offset_arcsec ie_offset_arcsec"
)


class TargetSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.Target class
    """

    ra = fields.String()
    dec = fields.String()
    reference_frame = shared.UpperCasedField(data_key="reference_frame")
    target_name = fields.String()
    ca_offset_arcsec = fields.Float()
    ie_offset_arcsec = fields.Float()

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
        if target.coord is None:
            hms, dms, reference_frame = None, None, None
        else:
            icrs_coord = target.coord.transform_to("icrs")
            reference_frame = icrs_coord.frame.name
            hms, dms = icrs_coord.to_string("hmsdms", sep=":").split(" ")
        sexagesimal = JsonTarget(
            ra=hms,
            dec=dms,
            reference_frame=reference_frame,
            target_name=target.target_name,
            ca_offset_arcsec=target.ca_offset_arcsec,
            ie_offset_arcsec=target.ie_offset_arcsec,
        )

        return sexagesimal

    @post_dump
    def omit_optional_fields_with_default_values(
        self, data, **_
    ):  # pylint: disable=no-self-use
        """
        Don't bother sending JSON fields with null/empty/default values.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for JSON serialization as a Target
        """
        if data["ra"] is None and data["dec"] is None:
            del data["ra"]
            del data["dec"]
            del data["reference_frame"]

        # If offset values are zero, omit them:
        for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
            if data[field_name] == 0.0:
                del data[field_name]

        if data["target_name"] == "":
            del data["target_name"]

        return data

    @post_load
    def create_target(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Target object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """

        target = configure_msgs.Target(
            data.get("ra"),
            data.get("dec"),
            reference_frame=data.get("reference_frame", ""),
            target_name=data.get("target_name", ""),
            unit=("hourangle", "deg"),
            ca_offset_arcsec=data.get("ca_offset_arcsec", 0.0),
            ie_offset_arcsec=data.get("ie_offset_arcsec", 0.0),
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
        data_key="receiver_band", required=True, validate=OneOf(["1", "2", "5a", "5b"])
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
class ConfigureRequestSchema(
    shared.ValidatingSchema
):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the subarray_node.ConfigureRequest class.
    """

    interface = fields.String(required=True)
    transaction_id = fields.String()

    pointing = fields.Nested(PointingSchema)
    dish = fields.Nested(DishConfigurationSchema)
    sdp = fields.Nested(sdp.SDPConfigurationSchema)
    csp = fields.Nested(csp.CSPConfigurationSchema)
    tmc = fields.Nested(tmc.TMCConfigurationSchema)
    mccs = fields.Nested(mccs.MCCSConfigurationSchema)

    @post_load
    def create_configuration(
        self, data, **_
    ):  # pylint: disable=no-self-use,redefined-outer-name
        """
        Converted parsed JSON backn into a subarray_node.ConfigureRequest
        object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ConfigurationRequest instance populated to match JSON
        """
        interface = data.get("interface")
        transaction_id = data.get("transaction_id", None)
        pointing = data.get("pointing", None)
        dish = data.get("dish", None)
        sdp = data.get("sdp", None)
        csp = data.get("csp", None)
        tmc = data.get("tmc", None)
        mccs = data.get("mccs", None)
        return ConfigureRequest(
            interface=interface,
            transaction_id=transaction_id,
            pointing=pointing,
            dish=dish,
            sdp=sdp,
            csp=csp,
            mccs=mccs,
            tmc=tmc,
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
