from __future__ import annotations

from enum import Enum
from typing import Literal, Optional, Union

from pydantic import Discriminator, Field
from typing_extensions import Annotated

from ska_tmc_cdm import CdmObject
from ska_tmc_cdm.messages.skydirection import SkyDirection


class TrajectoryType(str, Enum):
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


class MosaicTrajectory(CdmObject):
    name: Literal[TrajectoryType.MOSAIC] = TrajectoryType.MOSAIC
    attrs: MosaicTrajectory.Attrs

    class Attrs(CdmObject):
        x_offsets: list[float]
        y_offsets: list[float]


class TableTrajectory(CdmObject):
    name: Literal[TrajectoryType.TABLE] = TrajectoryType.TABLE
    attrs: TableTrajectory.Attrs

    class Attrs(CdmObject):
        x: list[float]
        y: list[float]
        t: list[float]


class FixedTrajectory(CdmObject):
    name: Literal[TrajectoryType.FIXED] = TrajectoryType.FIXED
    attrs: FixedTrajectory.Attrs

    class Attrs(CdmObject):
        x: float
        y: float


Trajectory = Annotated[
    Union[MosaicTrajectory, TableTrajectory, FixedTrajectory],
    Discriminator("name"),
]


class ProjectionType(str, Enum):
    """Projection Names"""

    SIN = "SIN"
    TAN = "TAN"
    ARC = "ARC"
    STG = "STG"
    CAR = "CAR"
    SSN = "SSN"


class ProjectionAlignment(str, Enum):
    """Projection Alignment"""

    ICRS = "ICRS"
    ALTAZ = "AltAz"


class Projection(CdmObject):
    """
    Projection Config
    """

    name: ProjectionType = ProjectionType.SIN
    alignment: ProjectionAlignment = ProjectionAlignment.ICRS


class ReceptorGroup(CdmObject):
    """
    Receptor Group defines a set of receptors plus the sky direction and
    tracking/mapping strategy for target tracking."""

    receptors: set[str] = Field(default_factory=set)
    field: SkyDirection
    trajectory: Optional[Trajectory] = None
    projection: Optional[Projection] = None
