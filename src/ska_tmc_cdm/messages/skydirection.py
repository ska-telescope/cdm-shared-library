from __future__ import annotations

from enum import Enum
from typing import Annotated, Callable, Literal, Optional, Union

from pydantic import BeforeValidator, Field

from ska_tmc_cdm import CdmObject


class CaseInsensitiveEnum(str, Enum):
    """
    Case-insensitive enumeration.

    The implementation requires that all enumeration names be upper-case.
    """

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return None
        return cls.__members__.get(value.upper(), None)


# If we upgrade to Py 3.11 use StrEnum
class SolarSystemObject(CaseInsensitiveEnum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"


class ReferenceFrame(CaseInsensitiveEnum):
    """
    A sky direction reference frame as defined in ADR-63.

    ADR-63 recommends that reference frames be lower-case.

    See https://confluence.skatelescope.org/x/75A_Cw
    """

    ICRS = "icrs"
    ALTAZ = "altaz"
    GALACTIC = "galactic"
    TLE = "tle"
    SPECIAL = "special"


def _normalise_enum_case(
    cls: type[CaseInsensitiveEnum],
) -> Callable[[str], str]:
    """
    Creates a function to return an Enum value corrected for case so that it
    exactly matches that of the Enum.
    """

    def f(v: str) -> str:
        # delegates to CaseInsensitiveEnum for the actual case processing
        return cls(v)

    return f


# While the CaseInsensitiveEnum is sufficient for deserialisation when used as
# a non-literal, validation as a literal requires that the input case be an
# exact match of the literal value. These annotations create a literal that
# pre-processes the input to normalise the case of the enum value to match
# that of the literal.
_ICRS = Annotated[
    Literal[ReferenceFrame.ICRS],
    BeforeValidator(_normalise_enum_case(ReferenceFrame)),
]
_ALTAZ = Annotated[
    Literal[ReferenceFrame.ALTAZ],
    BeforeValidator(_normalise_enum_case(ReferenceFrame)),
]
_GALACTIC = Annotated[
    Literal[ReferenceFrame.GALACTIC],
    BeforeValidator(_normalise_enum_case(ReferenceFrame)),
]
_SPECIAL = Annotated[
    Literal[ReferenceFrame.SPECIAL],
    BeforeValidator(_normalise_enum_case(ReferenceFrame)),
]
_TLE = Annotated[
    Literal[ReferenceFrame.TLE],
    BeforeValidator(_normalise_enum_case(ReferenceFrame)),
]


class ICRSField(CdmObject):
    """
    An ADR-63 field defined in the ICRS reference frame.
    """

    reference_frame: _ICRS = ReferenceFrame.ICRS
    target_name: str
    attrs: ICRSField.Attrs

    class Attrs(CdmObject):
        c1: float = Field(ge=0.0, lt=360.0)
        c2: float = Field(ge=-90.0, le=90.0)
        pm_c1: Optional[float] = None
        pm_c2: Optional[float] = None
        epoch: Optional[float] = None
        parallax: Optional[float] = None
        radial_velocity: Optional[float] = None


class AltAzField(CdmObject):
    """
    An ADR-63 field defined in the AltAz (az/el) reference frame.
    """

    reference_frame: _ALTAZ = ReferenceFrame.ALTAZ
    target_name: str
    attrs: AltAzField.Attrs

    class Attrs(CdmObject):
        c1: float = Field(ge=0.0, lt=360.0)
        c2: float = Field(ge=0.0, le=90.0)


class GalacticField(CdmObject):
    """
    An ADR-63 field defined in the Galactic reference frame.
    """

    reference_frame: _GALACTIC = ReferenceFrame.GALACTIC
    target_name: str
    attrs: GalacticField.Attrs

    class Attrs(CdmObject):
        c1: float = Field(ge=0.0, lt=360.0)
        c2: float = Field(ge=-90.0, le=90.0)
        pm_c1: Optional[float] = None
        pm_c2: Optional[float] = None
        epoch: Optional[float] = None
        parallax: Optional[float] = None
        radial_velocity: Optional[float] = None


class SpecialField(CdmObject):
    """
    An ADR-63 field whose coordinates will be looked up in runtime using
    Katpoint.
    """

    reference_frame: _SPECIAL = ReferenceFrame.SPECIAL
    target_name: SolarSystemObject


class TLEField(CdmObject):
    """
    A Two-Line element (TLE) ADR-63 field.
    """

    reference_frame: _TLE = ReferenceFrame.TLE
    target_name: str
    attrs: TLEField.Attrs

    class Attrs(CdmObject):
        line1: list[float] = Field(default_factory=list)
        line2: list[float] = Field(default_factory=list)


# Pydantic does not allow validators for discriminator fields. This is a
# problem for reference_frame, which we want to be case-insensitive AND be
# used as a discriminator. The Pydantic documentation says 'This can be
# worked around by using a standard Union, dropping the discriminator', which
# gives us the form below.
SkyDirection = Union[
    ICRSField, AltAzField, GalacticField, TLEField, SpecialField
]
