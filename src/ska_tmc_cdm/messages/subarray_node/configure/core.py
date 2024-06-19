"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
import math
from enum import Enum
from typing import ClassVar, Optional, Any
from typing_extensions import Self

from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic import (
    ConfigDict,
    Field,
    model_validator,
    field_serializer,
    field_validator,
    ValidationInfo,
)

from ska_tmc_cdm.messages.base import CdmObject

__all__ = [
    "PointingConfiguration",
    "Target",
    "PointingCorrection",
    "ReceiverBand",
    "DishConfiguration",
]

UnitStr = str | u.Unit
UnitInput = UnitStr | tuple[UnitStr, UnitStr]


# class TargetSchema(Schema):
#     """
#     Marshmallow schema for the subarray_node.Target class
#     """

#     ra = fields.String()
#     dec = fields.String()
#     reference_frame = shared.UpperCasedField(data_key="reference_frame")
#     target_name = fields.String()
#     ca_offset_arcsec = fields.Float()
#     ie_offset_arcsec = fields.Float()

#     @pre_dump
#     def convert_to_icrs(
#         self, target: configure_msgs.Target, **_
#     ):  # pylint: disable=no-self-use
#         """
#         Process Target co-ordinates by converting them to ICRS frame before
#         the JSON marshalling process begins.

#         :param target: Target instance to process
#         :param _: kwargs passed by Marshallow
#         :return: SexagesimalTarget with ICRS ra/dec expressed in hms/dms
#         """
#         # All pointing coordinates are in ICRS
#         if target.coord is None:
#             hms, dms, reference_frame = None, None, None
#         else:
#             icrs_coord = target.coord.transform_to("icrs")
#             reference_frame = icrs_coord.frame.name
#             hms, dms = icrs_coord.to_string("hmsdms", sep=":").split(" ")
#         sexagesimal = JsonTarget(
#             ra=hms,
#             dec=dms,
#             reference_frame=reference_frame,
#             target_name=target.target_name,
#             ca_offset_arcsec=target.ca_offset_arcsec,
#             ie_offset_arcsec=target.ie_offset_arcsec,
#         )

#         return sexagesimal

#     @post_dump
#     def omit_optional_fields_with_default_values(
#         self, data, **_
#     ):  # pylint: disable=no-self-use
#         """
#         Don't bother sending JSON fields with null/empty/default values.

#         :param data: Marshmallow-provided dict containing parsed object values
#         :param _: kwargs passed by Marshmallow
#         :return: dict suitable for JSON serialization as a Target
#         """
#         if data["ra"] is None and data["dec"] is None:
#             del data["ra"]
#             del data["dec"]
#             del data["reference_frame"]

#         # If offset values are zero, omit them:
#         for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
#             if data[field_name] == 0.0:
#                 del data[field_name]

#         if data["target_name"] == "":
#             del data["target_name"]

#         return data

#     @post_load
#     def create_target(self, data, **_):  # pylint: disable=no-self-use
#         """
#         Convert parsed JSON back into a Target object.

#         :param data: dict containing parsed JSON values
#         :param _: kwargs passed by Marshmallow
#         :return: Target instance populated to match JSON
#         """

#         target = configure_msgs.Target(
#             data.get("ra"),
#             data.get("dec"),
#             reference_frame=data.get("reference_frame", ""),
#             target_name=data.get("target_name", ""),
#             unit=("hourangle", "deg"),
#             ca_offset_arcsec=data.get("ca_offset_arcsec", 0.0),
#             ie_offset_arcsec=data.get("ie_offset_arcsec", 0.0),
#         )
#         return target

#         # If offset values are zero, omit them:
#         for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
#             if data[field_name] == 0.0:
#                 del data[field_name]

#         if data["target_name"] == "":
#             del data["target_name"]

#         return data

#     @post_load
#     def create_target(self, data, **_):  # pylint: disable=no-self-use
#         """
#         Convert parsed JSON back into a Target object.

#         :param data: dict containing parsed JSON values
#         :param _: kwargs passed by Marshmallow
#         :return: Target instance populated to match JSON
#         """

#         target = configure_msgs.Target(
#             data.get("ra"),
#             data.get("dec"),
#             reference_frame=data.get("reference_frame", ""),
#             target_name=data.get("target_name", ""),
#             unit=("hourangle", "deg"),
#             ca_offset_arcsec=data.get("ca_offset_arcsec", 0.0),
#             ie_offset_arcsec=data.get("ie_offset_arcsec", 0.0),
#         )
#         return target


# TODO: Target() is doing too much fancy logic IMHO.
# Could we annotate astropy.SkyCoord and use that directly
# instead?
class Target(CdmObject):
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    OFFSET_MARGIN_IN_RAD: ClassVar[float] = 6e-17  # Arbitrary small number

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=False, validate_default=False
    )
    ra: Optional[str] = None
    dec: Optional[str] = None
    reference_frame: str = "icrs"
    unit: UnitInput = Field(default=("hourangle", "deg"), exclude=True)
    target_name: str = ""
    ca_offset_arcsec: float = 0.0
    ie_offset_arcsec: float = 0.0
    coord: Optional[SkyCoord] = Field(default=None, exclude=True)

    @field_serializer("reference_frame")
    def uppercase(self, value: str) -> str:
        """
        Dump to uppercase for compatibility with removed Marshmallow schema
        """
        return value.upper()

    @field_validator("reference_frame")
    @classmethod
    def lowercase(cls, value: str) -> str:
        """
        Load to lowercase for compatibility with removed Marshmallow schema
        """
        return value.lower()

    @field_validator("coord")
    @classmethod
    def set_coord(cls, value: Any, other_fields: ValidationInfo) -> Optional[SkyCoord]:
        if other_fields.data["ra"] and other_fields["dec"]:
            return SkyCoord(
                ra=other_fields.data["ra"],
                dec=other_fields.data["dec"],
                unit=other_fields.data["unit"],
                frame=other_fields.data["reference_frame"],
            )

    @model_validator(mode="after")
    def ra_dec_or_offsets_required(self) -> Self:
        offsets = self.ca_offset_arcsec or self.ie_offset_arcsec
        if not self.coord and not offsets:
            raise ValueError(
                "A Target() must specify either ra/dec or one nonzero ca_offset_arcsec or ie_offset_arcsec"
            )
        return self

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False
        # Either both are None or both defined...
        if bool(self.cord) != bool(other.coord):
            return False

        # Common checks:
        name_and_offsets_matching = (
            self.target_name == other.target_name
            and math.isclose(
                self.ca_offset_arcsec,
                other.ca_offset_arcsec,
                abs_tol=self.OFFSET_MARGIN_IN_RAD,
            )
            and math.isclose(
                self.ie_offset_arcsec,
                other.ie_offset_arcsec,
                abs_tol=self.OFFSET_MARGIN_IN_RAD,
            )
        )
        if not name_and_offsets_matching:
            return False

        # Please replace this with a more elegant way of dealing with differences
        # comparing targets with different properties...
        if self.coord is not None:
            sep = self.coord.separation(other.coord)
            return (
                self.coord.frame.name == other.coord.frame.name
                and sep.radian < self.OFFSET_MARGIN_IN_RAD
            )
        return True

    def __repr__(self):
        if self.cord is None:
            return "Target(target_name={!r}, ca_offset_arcsect={!r}, ie_offset_arcsec={!r})".format(
                self.target_name, self.ca_offset_arcsec, self.ie_offset_arcsec
            )
        else:
            raw_ra = self.cord.ra.value
            raw_dec = self.cord.dec.value
            units = (self.cord.ra.unit.name, self.coord.dec.unit.name)
            reference_frame = self.cord.frame.name
            target_name = self.target_name
            return "Target(ra={!r}, dec={!r}, target_name={!r}, reference_frame={!r}, unit={!r}, ca_offset_arcsec={!r}, ie_offset_arcsec={!r})".format(
                raw_ra,
                raw_dec,
                target_name,
                reference_frame,
                units,
                self.ca_offset_arcsec,
                self.ie_offset_arcsec,
            )

    def __str__(self):
        reference_frame = self.cord.frame.name
        target_name = self.target_name
        hmsdms = self.cord.to_string(style="hmsdms")
        return "<Target: {!r} ({} {})>".format(target_name, hmsdms, reference_frame)


class PointingCorrection(Enum):
    """
    Operation to apply to the pointing correction model.
    MAINTAIN: continue applying the current pointing correction model
    UPDATE: wait for (if necessary) and apply new pointing calibration solution
    RESET: reset the applied pointing correction to the pointing model defaults
    """

    MAINTAIN = "MAINTAIN"
    UPDATE = "UPDATE"
    RESET = "RESET"


class PointingConfiguration(CdmObject):
    """
    PointingConfiguration specifies where the subarray receptors are going to
    point.
    """

    target: Optional[Target] = None
    correction: Optional[PointingCorrection] = None


class ReceiverBand(Enum):
    """
    ReceiverBand is an enumeration of SKA MID receiver bands.
    """

    BAND_1 = "1"
    BAND_2 = "2"
    BAND_5A = "5a"
    BAND_5B = "5b"


class DishConfiguration(CdmObject):
    """
    DishConfiguration specifies how SKA MID dishes in a sub-array should be
    configured. At the moment, this is limited to setting the receiver band.
    """

    receiver_band: ReceiverBand
