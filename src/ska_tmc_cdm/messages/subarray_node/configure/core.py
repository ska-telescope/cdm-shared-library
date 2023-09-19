"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
from dataclasses import InitVar, field
from enum import Enum
from typing import ClassVar, Optional, Union

from astropy import units as u
from astropy.coordinates import SkyCoord
from pydantic import ConfigDict, model_validator
from pydantic.dataclasses import dataclass

__all__ = ["PointingConfiguration", "Target", "ReceiverBand", "DishConfiguration"]


@dataclass(
    config=ConfigDict(arbitrary_types_allowed=True)
)  # Required because AstroPy types aren't Pydantic models
class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    ra: InitVar[str | int | float | u.Quantity]
    dec: InitVar[str | int | float | u.Quantity]
    target_name: str = ""
    reference_frame: InitVar[str] = "icrs"
    unit: InitVar[str | u.Unit | tuple[str | u.Unit, str | u.Unit]] = (
        u.hourangle,
        u.deg,
    )
    coord: SkyCoord = field(init=False)

    OFFSET_MARGIN_IN_RAD: ClassVar[float] = 6e-17  # Arbitrary small number

    def __post_init__(
        self,
        ra: str | u.Quantity,
        dec: str | u.Quantity,
        reference_frame: str,
        unit: u.Unit,
    ):
        self.coord = SkyCoord(ra=ra, dec=dec, unit=unit, frame=reference_frame)

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False

        # Please replace this with a  more elegant way of dealing with differences
        # due to floating point arithmetic when comparing targets
        # defined in different ways.
        sep = self.coord.separation(other.coord)

        return (
            self.target_name == other.target_name
            and self.coord.frame.name == other.coord.frame.name
            and sep.radian < self.OFFSET_MARGIN_IN_RAD
        )

    def __repr__(self):
        raw_ra = self.coord.ra.value
        raw_dec = self.coord.dec.value
        units = (self.coord.ra.unit.name, self.coord.dec.unit.name)
        reference_frame = self.coord.frame.name
        target_name = self.target_name
        return "<Target(ra={!r}, dec={!r}, target_name={!r}, reference_frame={!r}, unit={!r})>".format(
            raw_ra, raw_dec, target_name, reference_frame, units
        )

    def __str__(self):
        reference_frame = self.coord.frame.name
        target_name = self.target_name
        hmsdms = self.coord.to_string(style="hmsdms")
        return "<Target: {!r} ({} {})>".format(target_name, hmsdms, reference_frame)


@dataclass
class PointingConfiguration:  # pylint: disable=too-few-public-methods
    """
    PointingConfiguration specifies where the subarray receptors are going to
    point.
    """

    target: Target


class ReceiverBand(Enum):
    """
    ReceiverBand is an enumeration of SKA MID receiver bands.
    """

    BAND_1 = "1"
    BAND_2 = "2"
    BAND_5A = "5a"
    BAND_5B = "5b"


@dataclass
class DishConfiguration:
    """
    DishConfiguration specifies how SKA MID dishes in a sub-array should be
    configured. At the moment, this is limited to setting the receiver band.
    """

    receiver_band: ReceiverBand
