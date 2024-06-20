"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
import math
from enum import Enum
from typing import ClassVar, Optional, Any, Callable
from typing_extensions import Self

from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic_core import SerializationCallable
from pydantic import (
    ConfigDict,
    Field,
    model_validator,
    model_serializer,
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
        arbitrary_types_allowed=True, validate_assignment=True, validate_default=True
    )
    ra: Optional[str | float] = None
    dec: Optional[str | float] = None
    reference_frame: str = "icrs"
    unit: UnitInput = Field(default=("hourangle", "deg"), exclude=True)
    target_name: str = ""
    ca_offset_arcsec: float = 0.0
    ie_offset_arcsec: float = 0.0
    coord: Optional[SkyCoord] = Field(default=None, exclude=True)

    @model_serializer(mode="wrap")
    def omit_defaults(self, handler: Callable):
        """
        (Custom serializer logic copied verbatim from
        removed Marshmallow schema.)

        Don't bother sending JSON fields with null/empty/default values.
        """
        data = handler(self)
        if data["ra"] is None and data["dec"] is None:
            del data["ra"]
            del data["dec"]
            del data["reference_frame"]
        else:
            # TODO: IMHO doing this conversion here is janky. If we only want to
            # work with ICRS coordinates, we should enforce that as part of
            # validation, not convert to it at the end when we dump()
            # Preseved directly from Marshmallow...
            #     Process Target co-ordinates by converting them to ICRS frame before
            #     the JSON marshalling process begins.
            icrs_coord = self.coord.transform_to("icrs")
            data["reference_frame"] = icrs_coord.frame.name
            data["ra"], data["dec"] = icrs_coord.to_string("hmsdms", sep=":").split(" ")

        # If offset values are zero, omit them:
        for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
            if data[field_name] == 0.0:
                del data[field_name]

        if data["target_name"] == "":
            del data["target_name"]

        return data

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
    def set_coord(cls, value: Any, info: ValidationInfo) -> Optional[SkyCoord]:
        # NB: This validator only fires with validate_default=True
        # because we want to *replace* the default None.
        if info.data["ra"] and info.data["dec"]:
            return SkyCoord(
                ra=info.data["ra"],
                dec=info.data["dec"],
                unit=info.data["unit"],
                frame=info.data["reference_frame"],
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
        if bool(self.coord) != bool(other.coord):
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
        if self.coord is None:
            return "Target(target_name={!r}, ca_offset_arcsect={!r}, ie_offset_arcsec={!r})".format(
                self.target_name, self.ca_offset_arcsec, self.ie_offset_arcsec
            )
        else:
            raw_ra = self.coord.ra.value
            raw_dec = self.coord.dec.value
            units = (self.coord.ra.unit.name, self.coord.dec.unit.name)
            reference_frame = self.coord.frame.name
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
        reference_frame = self.coord.frame.name
        target_name = self.target_name
        hmsdms = self.coord.to_string(style="hmsdms")
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
