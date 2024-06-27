"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
import math
from enum import Enum
from typing import Any, Callable, ClassVar, Literal, Optional, Union

from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic import (
    ConfigDict,
    Discriminator,
    Field,
    Tag,
    field_validator,
    model_serializer,
    model_validator,
)
from typing_extensions import Annotated, Self

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


class TargetType(str, Enum):
    SPECIAL = "special"
    ICRS = "icrs"
    PARTIAL = "partial"

    @classmethod
    def determine(cls, val: Any) -> Self:
        if isinstance(val, dict):
            if val.get("reference_frame") == cls.SPECIAL:
                return cls.SPECIAL
            elif val.get("reference_frame") == cls.ICRS:
                return cls.ICRS
            elif val.get("ra") is val.get("dec") is None:
                return cls.PARTIAL
        raise ValueError("Unable to determine TargetType")


class SolarSystemObject(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"


class SpecialTarget(CdmObject):
    reference_frame: Literal[TargetType.SPECIAL] = TargetType.SPECIAL
    name: SolarSystemObject


class PartialTarget(CdmObject):
    OFFSET_MARGIN_IN_RAD: ClassVar[float] = 6e-17  # Arbitrary small number
    target_name: str = ""
    ca_offset_arcsec: float = 0.0
    ie_offset_arcsec: float = 0.0


    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Target):
            return False

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
        return name_and_offsets_matching



# TODO: Target() is doing too much fancy logic IMHO.
# Could we annotate astropy.SkyCoord and use that directly
# instead?
class ICRSTarget(PartialTarget):
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)


    reference_frame: Literal[TargetType.ICRS] = TargetType.ICRS

    ra: str | float
    dec: str | float
    unit: UnitInput = Field(default=("hourangle", "deg"), exclude=True)

    @property
    def coord(self) -> SkyCoord:
        return SkyCoord(
            ra=self.ra,
            dec=self.dec,
            unit=self.unit,
            frame=self.reference_frame,
        )

    @model_serializer(mode="wrap")
    def omit_defaults(self, handler: Callable):
        """
        (Custom serializer logic copied verbatim from
        removed Marshmallow schema.)

        Don't bother sending JSON fields with null/empty/default values.
        """
        data = handler(self)
        # TODO: IMHO doing this conversion here is janky. If we only want to
        # work with ICRS coordinates, we should enforce that as part of
        # validation, not convert to it at the end when we dump()
        # Preseved directly from Marshmallow...
        #     Process Target co-ordinates by converting them to ICRS frame before
        #     the JSON marshalling process begins.
        icrs_coord = self.coord.transform_to("icrs")
        data["reference_frame"] = icrs_coord.frame.name.upper()
        data["ra"], data["dec"] = icrs_coord.to_string(
            "hmsdms", sep=":"
        ).split(" ")

        # If offset values are zero, omit them:
        for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
            if data[field_name] == 0.0:
                del data[field_name]

        if data["target_name"] == "":
            del data["target_name"]

        return data

    @field_validator("reference_frame")
    @classmethod
    def lowercase(cls, value: str) -> str:
        """
        Load to lowercase for compatibility with removed Marshmallow schema
        """
        return value.lower()

    @model_validator(mode="after")
    def ra_dec_or_offsets_required(self) -> Self:
        offsets = self.ca_offset_arcsec or self.ie_offset_arcsec
        if not self.coord and not offsets:
            raise ValueError(
                "A Target() must specify either ra/dec or one nonzero ca_offset_arcsec or ie_offset_arcsec"
            )
        return self

    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other) is False:
            return False

        other_coord = getattr(other, 'coord', None)
        if not other_coord:
            return False

        sep = self.coord.separation(other_coord)
        return (
            self.coord.frame.name == other_coord.frame.name
            and sep.radian < self.OFFSET_MARGIN_IN_RAD
        )

    def __repr__(self):
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
        return "<Target: {!r} ({} {})>".format(
            target_name, hmsdms, reference_frame
        )


Target = Annotated[
    Union[
        Annotated[ICRSTarget, Tag(TargetType.ICRS)],
        Annotated[PartialTarget, Tag(TargetType.PARTIAL)],
        Annotated[SpecialTarget, Tag(TargetType.SPECIAL)],
    ],
    Discriminator(TargetType.determine),
]


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
