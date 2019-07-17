"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from enum import Enum

from astropy.coordinates import SkyCoord

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'Target',
           'ReceiverBand']


class Target:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that RA and Dec must be provided, hence
    non-ra/dec frames such as galactic are not supported.
    """

    def __init__(self, ra, dec, name='', frame='icrs', unit='rad'):
        self.coord = SkyCoord(ra, dec, unit=unit, frame=frame)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False
        # As the target frame is ra/dec, we can rely on .ra and .dec
        # properties to be present
        return all([self.name == other.name,
                    self.coord.ra == other.coord.ra,
                    self.coord.dec == other.coord.dec,
                    self.coord.frame.name == other.coord.frame.name])

    def __str__(self):
        units = self.coord.ra.unit.name
        frame = self.coord.frame.name
        name = self.name
        # named ra_val rather than ra to satisfy static analysis
        ra_val = self.coord.ra.value
        dec_val = self.coord.dec.value
        return '<Target(ra={}, dec={}, name={!r}, frame={!r}, unit={!r})>'.format(
            ra_val, dec_val, name, frame, units
        )


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

    BAND_1 = '1'
    BAND_2 = '2'
    BAND_5A = '5a'
    BAND_5B = '5b'


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


class ConfigureRequest:  # pylint: disable=too-few-public-methods
    """
    ConfigureRequest encapsulates the arguments required for the TMC
    SubArrayNode.Configure() command.
    """

    def __init__(self, pointing: PointingConfiguration, dish: DishConfiguration):
        self.pointing = pointing
        self.dish = dish

    def __eq__(self, other):
        if not isinstance(other, ConfigureRequest):
            return False
        return self.pointing == other.pointing and self.dish == other.dish
