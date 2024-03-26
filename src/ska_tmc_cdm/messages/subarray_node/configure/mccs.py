"""
The configure.mccs module contains Python classes that represent the various
aspects of MCCS configuration that may be specified in a SubArray.configure
command.
"""

from typing import List, Optional

from pydantic.dataclasses import dataclass

__all__ = [
    "MCCSConfiguration",
    "StnConfiguration",
    "SubarrayBeamConfiguration",
    "SubarrayBeamTarget",
    "SubarrayBeamSkyCoordinates",
    "SubarrayBeamLogicalBands",
    "SubarrayBeamAperatures",
]


@dataclass
class SubarrayBeamTarget:
    """
    Target encapsulates source coordinates and source metadata.

    The SubArrayNode ICD specifies that az and el must be provided


    :param az: Az specification with rates
    :param el: El specification with rates
    :param target_name: target name
    :param reference_frame: Target coordinate reference frame
    """

    az: float
    el: float
    target_name: str
    reference_frame: str


@dataclass
class StnConfiguration:
    """A class to hold station configuration configuration

    :param station_id: stations id
    :type station_id: int
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
    """A class to hold subarray_beam configuration attributes

    :param subarray_beam_id: stationbeam's id
    :type subarray_beam_id: int
    :param station_ids: station id's
    :type station_ids: List[int]
    :param channels: channels to form station beam
    :type channels: List[Tuple]
    :param update_rate: frequency of new Az/El during scan
    :type update_rate: float
    :param target: Az/El specification with target source
    :type target: SubarrayBeamTarget
    :param antenna_weights: antenna_weights
    :type antenna_weights: List[float]
    :param phase_centre: phase_centre
    :type phase_centre: List[float]
    """

    update_rate: float
    logical_bands: List[SubarrayBeamLogicalBands]
    apertures: List[SubarrayBeamAperatures]
    sky_coordinates: SubarrayBeamSkyCoordinates
    subarray_beam_id: Optional[int] = None
    station_ids: Optional[List[int]] = None
    channels: Optional[List[List[int]]] = None
    target: Optional[SubarrayBeamTarget] = None
    antenna_weights: Optional[List[float]] = None
    phase_centre: Optional[List[float]] = None


@dataclass(kw_only=True)
class MCCSConfiguration:
    """
    Class to hold all subarray configuration.

    :param station_configs: a list of station configurations
    :type station_configs: List[StnConfiguration]
    :param subarray_beam_configs: a list of subarray beam configurations
    :type subarray_beam_configs: List[SubarrayBeamConfiguration]
    """

    subarray_beam_configs: List[SubarrayBeamConfiguration]
    station_configs: Optional[List[StnConfiguration]] = None

