"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
import math
from enum import Enum
from typing import (
    Any,
    Callable,
    ClassVar,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
)

from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic import (
    ConfigDict,
    Discriminator,
    Field,
    Tag,
    field_serializer,
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
    "GenericPattern",
    "HolographyReceptorGroupConfig",
    "TrajectoryConfig",
]

UnitStr = str | u.Unit
UnitInput = UnitStr | tuple[UnitStr, UnitStr]

# If we upgrade to Py 3.11 use StrEnum
class TargetType(str, Enum):
    SPECIAL = "special"
    DEFAULT = "default"

    @classmethod
    def determine(cls, val: Any) -> "TargetType":
        if isinstance(val, dict):
            reference_frame = val.get("reference_frame", "")
        else:
            reference_frame = getattr(val, "reference_frame", "")

        match reference_frame.lower():
            case cls.SPECIAL:
                return cls.SPECIAL
            case _:
                return cls.DEFAULT


# If we upgrade to Py 3.11 use StrEnum
class SolarSystemObject(str, Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"


T = TypeVar("T")


class TargetBase:
    @field_validator("reference_frame", mode="before")
    @classmethod
    def _to_lowercase(cls, value: T) -> T:
        """
        Load to lowercase for compatibility with removed Marshmallow schema
        """
        if isinstance(value, str):
            return value.lower()
        # Not a str, downstream validators will catch:
        return value

    @field_serializer("reference_frame")
    def _to_uppercase(self, value: str) -> str:
        """
        Dump to uppercase for compatibility with removed Marshmallow schema
        """
        return value.upper()


class SpecialTarget(TargetBase, CdmObject):
    reference_frame: Literal[TargetType.SPECIAL] = TargetType.SPECIAL
    target_name: SolarSystemObject


# TODO: Target() is doing too much fancy logic IMHO.
# Could we annotate astropy.SkyCoord and use that directly
# instead?
class Target(TargetBase, CdmObject):
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
    # TODO: Can this be Literal["ICRS"] instead?
    reference_frame: str = "icrs"
    unit: UnitInput = Field(default=("hourangle", "deg"), exclude=True)
    target_name: str = ""
    ca_offset_arcsec: float = 0.0
    ie_offset_arcsec: float = 0.0

    @property
    def coord(self) -> Optional[SkyCoord]:
        if self.ra and self.dec:
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
            data["reference_frame"] = icrs_coord.frame.name.upper()
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
            return "Target(ra={!r}, dec={!r}, target_name={!r}, reference_frame={!r}, unit={!r}, ca_offset_arcsec={!r}, ie_offset_arcsec={!r})".format(
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


TargetUnion = Annotated[
    Union[
        Annotated[Target, Tag(TargetType.DEFAULT)],
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


class GenericPattern(Enum):
    """
    Holography Scan Pattern
    """

    FIXED = "fixed"
    MOSAIC = "mosaic"
    SPIRAL = "spiral"
    RASTER = "raster"
    CONSTANT_VELOCITY = "constant-velocity"
    TABLE = "table"
    HYPOTROCHOID = "hypotrochoid"


class TableAttrsConfig(CdmObject):
    """Attrs for table pattern"""

    x: int | list[int]
    y: int | list[int]
    t: Optional[int | list[int]]


class MosaicAttrsConfig(CdmObject):
    """Attrs for mosiac pattern"""

    x_offsets: list[int]
    y_offsets: list[int]


class MosaicTrajectoryConfig(CdmObject):
    name: Literal[GenericPattern.MOSAIC] = GenericPattern.MOSAIC
    attrs: MosaicAttrsConfig


class TableTrajectoryConfig(CdmObject):
    name: Literal[GenericPattern.TABLE] = GenericPattern.TABLE
    attrs: TableAttrsConfig


class FixedTrajectoryConfig(CdmObject):
    name: Literal[GenericPattern.FIXED] = GenericPattern.FIXED
    attrs: TableAttrsConfig


TrajectoryConfig = Annotated[
    Union[
        Annotated[MosaicTrajectoryConfig, Tag(GenericPattern.MOSAIC)],
        Annotated[TableTrajectoryConfig, Tag(GenericPattern.TABLE)],
        Annotated[FixedTrajectoryConfig, Tag(GenericPattern.FIXED)],
    ],
    Field(discriminator="name"),
]


class ProjectionName(Enum):
    """Projection Names"""

    SIN = "SIN"
    TAN = "TAN"
    ARC = "ARC"
    STG = "STG"
    CAR = "CAR"
    SSN = "SSN"


class ProjectionAlignment(Enum):
    """Projection Alignment"""

    ICRS = "ICRS"
    ALTAZ = "AltAz"


class ProjectionConfig(CdmObject):
    """Projection Config"""

    name: ProjectionName = ProjectionName.SIN
    alignment: ProjectionAlignment = ProjectionAlignment.ICRS


class HolographyReceptorGroupConfig(CdmObject):
    """Holography Receptor Group to apply"""

    receptors: list[str] = Field(default_factory=list)
    field: dict = Field(default_factory=dict)
    trajectory: Optional[TrajectoryConfig] = None
    projection: Optional[ProjectionConfig] = None


class PointingConfiguration(CdmObject):
    """
    PointingConfiguration specifies where the subarray receptors are going to
    point.
    """

    target: Optional[TargetUnion] = None
    correction: Optional[PointingCorrection] = None
    groups: list[HolographyReceptorGroupConfig] = Field(default_factory=list)


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
