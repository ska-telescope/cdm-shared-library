"""
The configure.common module contains simple Python representations of the
structured request and response for the TMC SubArrayNode.Configure command.

As configurations become more complex, they may be rehomed in a submodule of
this package.
"""
from enum import Enum

from astropy.coordinates import SkyCoord

__all__ = ["PointingConfiguration", "Target", "ReceiverBand", "DishConfiguration"]


class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    OFFSET_MARGIN_IN_RAD = 6e-17  # Arbitrary small number

    #  pylint: disable=too-many-arguments
    def __init__(self, ra, dec, target_name="", reference_frame="icrs", unit=("hourangle", "deg")):
        self.coord = SkyCoord(ra, dec, unit=unit, frame=reference_frame)
        self.target_name = target_name

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
        return "<Target(ra={!r}, dec={!r}, name={!r}, reference_frame={!r}, unit={!r})>".format(
            raw_ra, raw_dec, target_name, reference_frame, units
        )

    def __str__(self):
        reference_frame = self.coord.frame.name
        target_name = self.target_name
        hmsdms = self.coord.to_string(style="hmsdms")
        return "<Target: {!r} ({} {})>".format(target_name, hmsdms, reference_frame)


class PointingConfiguration:  # pylint: disable=too-few-public-methods
    """
    PointingConfiguration specifies where the subarray receptors are going to
    point.
    """

    def __init__(self, target: Target):
        self.target = target

    def __eq__(self, other):
        if not isinstance(other, PointingConfiguration):
            return False
        return self.target == other.target


class ReceiverBand(Enum):
    """
    ReceiverBand is an enumeration of SKA MID receiver bands.
    """

    BAND_1 = "1"
    BAND_2 = "2"
    BAND_5A = "5a"
    BAND_5B = "5b"


class DishConfiguration:  # pylint: disable=too-few-public-methods
    """
    DishConfiguration specifies how SKA MID dishes in a sub-array should be
    configured. At the moment, this is limited to setting the receiver band.
    """

    def __init__(self, receiver_band: ReceiverBand):
        self.receiver_band = receiver_band

    def __eq__(self, other):
        if not isinstance(other, DishConfiguration):
            return False
        return self.receiver_band == other.receiver_band
