"""
The messages module provides simple Python representations of the structured
request and response for the TMC SubArrayNode.Configure command.
"""
from typing import Optional, List
from astropy.coordinates import SkyCoord
from astropy.table import Column

__all__ = ['ConfigureRequest', 'DishConfiguration', 'PointingConfiguration', 'SubarrayConfiguration']


class Target:
    def __init__(self, ra, dec, name, frame="icrs", unit="rad" ):
        self.coord = SkyCoord(ra=ra, dec=dec, unit=unit, frame=frame )
        c = Column(name=name)
        self.coord.info = c.info


class PointingConfiguration:
    def __init__(self, target: SkyCoord):
        self.target = target


class DishConfiguration:
    def __init__(self, receiver_band: str):
        self.receiver_band = receiver_band


class SubarrayConfiguration:
    def __init__(self, pointing: PointingConfiguration, dish: DishConfiguration):
        self.pointing = pointing
        self.dish = dish


class ConfigureRequest:
    def __init__(self, pointing: PointingConfiguration, dish: DishConfiguration):
        self.pointing = pointing
        self.dish = dish