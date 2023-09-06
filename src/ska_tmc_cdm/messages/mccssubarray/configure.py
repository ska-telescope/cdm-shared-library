"""
The mccssubarray.configure module contains a Python object model for the
various structured bits of JSON given in an MCCSSubarray.Configure call.
"""
from dataclasses import KW_ONLY

from pydantic.dataclasses import dataclass

__all__ = ["ConfigureRequest", "StationConfiguration", "SubarrayBeamConfiguration"]

SCHEMA = "https://schema.skao.int/ska-low-mccs-configure/2.0"


@dataclass
class StationConfiguration:
    """A class to hold station configuration

    :param station_id: stations id
    """

    station_id: int


@dataclass
class SubarrayBeamConfiguration:
    """A class to hold subarray beam configuration attributes

    :param subarray_beam_id: subarray beam ID
    :param station_ids: station IDs
    :param channels: channels to form subarray beam
    :param update_rate: frequency of new Az/El during scan
    :param sky_coordinates: Az/El specification with rates
    :param antenna_weights: antenna weights, 1 per station
    :param phase_centre: phase centre of subarray beam
    """

    _: KW_ONLY
    subarray_beam_id: int
    station_ids: list[int]
    update_rate: float
    channels: list[list[int]]
    sky_coordinates: list[float]
    antenna_weights: list[float]
    phase_centre: list[float]


@dataclass
class ConfigureRequest:
    """
    Class to hold all subarray configuration.

    :param stations: a list of station configurations
    :param subarray_beams: a list of subarray beam configurations
    """

    _: KW_ONLY
    interface: str = SCHEMA
    stations: list[StationConfiguration]
    subarray_beams: list[SubarrayBeamConfiguration]
