"""
The mccssubarray.configure module contains a Python object model for the
various structured bits of JSON given in an MCCSSubarray.Configure call.
"""
from pydantic.dataclasses import dataclass

__all__ = [
    "ConfigureRequest",
    "StationConfiguration",
    "SubarrayBeamConfiguration",
    "SubarrayBeamLogicalBands",
    "SubarrayBeamAperatures",
    "SubarrayBeamSkyCoordinates",
]

SCHEMA = "https://schema.skao.int/ska-low-mccs-configure/2.0"


@dataclass
class StationConfiguration:
    """A class to hold station configuration

    :param station_id: stations id
    """

    station_id: int


@dataclass
class SubarrayBeamSkyCoordinates:
    """
    A class to hold Subarray Beam sky coordinates configuration items
    :param timestamp: UTC time for begin of drift.
    :type timestamp: str
    :param reference_frame: Must be one of: ["topocentric", "ICRS", "galactic"]
    :type reference_frame: str
    :param c1: first coordinate, RA or azimuth, in degrees
    :type c1: float
    :param c1_rate: Drift rate for first coordinate
    :type c1_rate: float
    :param c2: second coordinate, RA or azimuth, in degrees
    :type c2: float
    :param c2_rate: Drift rate for second coordinate
    :type c2_rate: float
    """

    timestamp: str = None
    reference_frame: str = None
    c1: float = None
    c1_rate: float = None
    c2: float = None
    c2_rate: float = None


@dataclass
class SubarrayBeamLogicalBands:
    """
    A class to hold Subarray Beam logical bands configuration items
    :param start_channel: Start channel value.
    :type start_channel: str
    :param number_of_channels: No of channels
    :type number_of_channels: str
    """

    start_channel: int = None
    number_of_channels: int = None


@dataclass
class SubarrayBeamAperatures:
    """
    A class to hold Subarray Beam aperatures configuration
    items
    :param aperture_id: Aperture ID.
    :type aperture_id: str
    :param weighting_key_ref: Descriptive ID for the aperture
    weights in the aperture database.
    :type weighting_key_ref: str
    """

    aperture_id: str = None
    weighting_key_ref: str = None


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

    subarray_beam_id: int
    station_ids: list[int]
    update_rate: float
    channels: list[list[int]]
    sky_coordinates: list[float]
    antenna_weights: list[float]
    phase_centre: list[float]
    logical_bands: list[SubarrayBeamLogicalBands]
    apertures: list[SubarrayBeamAperatures]
    sky_coordinates: SubarrayBeamSkyCoordinates


@dataclass(kw_only=True)
class ConfigureRequest:
    """
    Class to hold all subarray configuration.

    :param stations: a list of station configurations
    :param subarray_beams: a list of subarray beam configurations
    """

    interface: str = SCHEMA
    stations: list[StationConfiguration]
    subarray_beams: list[SubarrayBeamConfiguration]
