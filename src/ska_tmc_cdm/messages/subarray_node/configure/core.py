"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
import math
from enum import Enum
from typing import Callable, ClassVar, Literal, Optional, Union, cast

import typing_extensions
from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic import (
    BeforeValidator,
    ConfigDict,
    Field,
    model_serializer,
    model_validator,
)
from typing_extensions import Annotated, Self

from ska_tmc_cdm.messages.base import CdmObject
from ska_tmc_cdm.messages.skydirection import (
    CaseInsensitiveEnum,
    SolarSystemObject,
    _normalise_enum_case,
)
from ska_tmc_cdm.messages.subarray_node.configure.receptorgroup import (
    ReceptorGroup,
)

__all__ = [
    "PointingConfiguration",
    "Target",
    "ICRSTarget",
    "FK5Target",
    "SpecialTarget",
    "PointingCorrection",
    "ReceiverBand",
    "DishConfiguration",
]


UnitStr = str | u.Unit
UnitInput = UnitStr | tuple[UnitStr, UnitStr]


class LegacyTargetReferenceFrame(CaseInsensitiveEnum):
    """
    ** DEPRECATED **

    This class supports the legacy Target class and will be removed in a
    future release.

    Enumeration of supported coordinate reference frames, one for each legacy
    Target coordinate class.

    """

    # these enum values becomes case-insensitive on reading, case-sensitive on writing.
    ICRS = "ICRS"
    FK5 = "fk5"
    SPECIAL = "special"


# normalise case on deserialisation. see comments in skydirection.py for info
# on how this works
_ICRS = Annotated[
    Literal[LegacyTargetReferenceFrame.ICRS],
    BeforeValidator(_normalise_enum_case(LegacyTargetReferenceFrame)),
]
_FK5 = Annotated[
    Literal[LegacyTargetReferenceFrame.FK5],
    BeforeValidator(_normalise_enum_case(LegacyTargetReferenceFrame)),
]
_SPECIAL = Annotated[
    Literal[LegacyTargetReferenceFrame.SPECIAL],
    BeforeValidator(_normalise_enum_case(LegacyTargetReferenceFrame)),
]


# TODO: Target() is doing too much fancy logic IMHO.
# Could we annotate astropy.SkyCoord and use that directly
# instead?
class _TargetBase(CdmObject):
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    OFFSET_MARGIN_IN_RAD: ClassVar[float] = 6e-17  # Arbitrary small number

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        validate_default=True,
    )
    ra: Optional[str | float] = None
    dec: Optional[str | float] = None
    unit: UnitInput = Field(default=("hourangle", "deg"), exclude=True)
    target_name: str = ""
    ca_offset_arcsec: float = 0.0
    ie_offset_arcsec: float = 0.0

    # just here to indicate what the coord functions expects. The scope will
    # be reduced to a single StrEnum enumerated frame by the subclass. Note,
    # we can't say _FK5 | _ICRS as pyright objects to the subclass redefining
    # the type class
    reference_frame: str

    @property
    def coord(self) -> Optional[SkyCoord]:
        if self.ra is not None and self.dec is not None:
            return SkyCoord(
                ra=self.ra,
                dec=self.dec,
                unit=self.unit,
                # astropy ref frames are all lower case
                frame=self.reference_frame.lower(),
            )

    @model_serializer(mode="wrap")
    def omit_defaults(self, handler: Callable):
        """
        (Custom serializer logic copied verbatim from
        removed Marshmallow schema.)

        Don't bother sending JSON fields with null/empty/default values.
        """
        data = handler(self)
        if self.ra is None and self.dec is None:
            # These should already be filtered out
            # by exclude_none=True
            data.pop("ra", None)
            data.pop("dec", None)
            del data["reference_frame"]
        else:
            # For the type checker. We know coord is not-none here.
            assert self.coord is not None
            # TODO: IMHO doing this conversion here is janky. If we only want to
            # work with ICRS coordinates, we should enforce that as part of
            # validation, not convert to it at the end when we dump()
            # Preseved directly from Marshmallow...
            #     Process Target co-ordinates by converting them to ICRS frame before
            #     the JSON marshalling process begins.
            icrs_coord = self.coord.transform_to("icrs")
            data["reference_frame"] = LegacyTargetReferenceFrame(
                icrs_coord.frame.name
            )
            coord_str = cast(str, icrs_coord.to_string("hmsdms", sep=":"))
            data["ra"], data["dec"] = coord_str.split(" ")

        # If offset values are zero, omit them:
        for field_name in ("ca_offset_arcsec", "ie_offset_arcsec"):
            if data[field_name] == 0.0:
                del data[field_name]

        if data["target_name"] == "":
            del data["target_name"]

        return data

    @model_validator(mode="after")
    def ra_dec_or_offsets_required(self) -> Self:
        offsets = self.ca_offset_arcsec or self.ie_offset_arcsec
        if self.coord is None and not offsets:
            raise ValueError(
                "A Target() must specify either ra/dec or one nonzero ca_offset_arcsec or ie_offset_arcsec"
            )
        return self

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
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
        self_coord, other_coord = self.coord, other.coord
        if self_coord is not None and other_coord is not None:
            sep = self_coord.separation(other_coord)
            return bool(
                self_coord.frame.name == other_coord.frame.name
                and cast(float, sep.radian) < self.OFFSET_MARGIN_IN_RAD
            )
        return True

    def __repr__(self):
        self_coord = self.coord
        if self_coord is not None:
            # For the type checker. We know these are not-None:
            assert self_coord.ra is not None
            assert self_coord.dec is not None
            raw_ra = self_coord.ra.value
            raw_dec = self_coord.dec.value
            assert self_coord.ra.unit is not None
            assert self_coord.dec.unit is not None
            units = (self_coord.ra.unit.name, self_coord.dec.unit.name)
            reference_frame = self_coord.frame.name
            target_name = self.target_name
            cls = self.__class__.__name__
            return "{!s}(ra={!r}, dec={!r}, target_name={!r}, reference_frame={!r}, unit={!r}, ca_offset_arcsec={!r}, ie_offset_arcsec={!r})".format(
                cls,
                raw_ra,
                raw_dec,
                target_name,
                reference_frame,
                units,
                self.ca_offset_arcsec,
                self.ie_offset_arcsec,
            )
        else:
            return "Target(target_name={!r}, ca_offset_arcsect={!r}, ie_offset_arcsec={!r})".format(
                self.target_name, self.ca_offset_arcsec, self.ie_offset_arcsec
            )

    def __str__(self):
        if self.coord is not None:
            reference_frame = self.coord.frame.name
            hmsdms = self.coord.to_string(style="hmsdms")
        else:
            hmsdms = ""
            reference_frame = ""
        target_name = self.target_name
        return "<Target: {!r} ({} {})>".format(
            target_name, hmsdms, reference_frame
        )


class ICRSTarget(_TargetBase):
    reference_frame: _ICRS = LegacyTargetReferenceFrame.ICRS


class FK5Target(_TargetBase):
    reference_frame: _FK5 = LegacyTargetReferenceFrame.FK5


class SpecialTarget(CdmObject):
    reference_frame: _SPECIAL = LegacyTargetReferenceFrame.SPECIAL
    target_name: SolarSystemObject


TargetUnion = Union[ICRSTarget, FK5Target, SpecialTarget]


# alias for backwards compatibility for anyone create Targets in notebooks.
# This should be sufficient because in practise the FK5 reference frame was
# never used apart from the unit tests for this project.
Target = ICRSTarget


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

    target: Optional[TargetUnion] = Field(
        None,
        deprecated=typing_extensions.deprecated(
            "PointingConfiguration.target is deprecated and will be removed "
            "in a future version. Use PointingConfiguration.groups instead.",
            stacklevel=2,
        ),
    )
    correction: Optional[PointingCorrection] = None
    groups: Optional[list[ReceptorGroup]] = None
    wrap_sector: Optional[int] = Field(
        None,
        ge=-1,
        le=0,
        description="Indicates which sector the dishes should rotate to before starting the scan, while omission or None is interpreted as 'no change'.",
    )


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
