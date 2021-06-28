"""
The mccssubarray.configure module contains a Python object model for the
various structured bits of JSON given in an MCCSSubarray.Configure call.
"""

from typing import List, Optional

__all__ = [
    "ConfigureRequest",
    "StationConfiguration",
    "SubarrayBeamConfiguration"
]

SCHEMA = "https://schema.skao.int/ska-low-mccs-configure/2.0"


class StationConfiguration:
    """A class to hold station configuration"""

    def __init__(self, station_id: int):
        """
        Initialise the station configuration.

        :param station_id: stations id
        """
        self.station_id = station_id

    def __eq__(self, other):
        """
        Check for equality between two station configuration objects

        :param other: the object to check against this object
        :type other: station configuration object

        :return: returns True if the objects are the same, else False
        """
        if not isinstance(other, StationConfiguration):
            return False
        return self.station_id == other.station_id


class SubarrayBeamConfiguration:
    """A class to hold subarray beam configuration attributes"""

    def __init__(
            self,
            *,  # force kwonly args
            subarray_beam_id: int,
            station_ids: List[int],
            update_rate: float,
            channels: List[List[int]],
            sky_coordinates: List[float],
            antenna_weights: List[float],
            phase_centre: List[float]
    ):
        """
        Initialise the subarray beam configuration.

        :param subarray_beam_id: subarray beam ID
        :param station_ids: station IDs
        :param channels: channels to form subarray beam
        :param update_rate: frequency of new Az/El during scan
        :param sky_coordinates: Az/El specification with rates
        :param antenna_weights: antenna weights, 1 per station
        :param phase_centre: phase centre of subarray beam
        """
        self.subarray_beam_id = subarray_beam_id
        self.station_ids = station_ids
        self.channels = channels
        self.update_rate = update_rate
        self.sky_coordinates = sky_coordinates
        self.antenna_weights = antenna_weights
        self.phase_centre = phase_centre

    def __eq__(self, other):
        """
        Check for equality between two SubarrayBeamConfiguration objects

        :param other: the object to check against this object

        :return: returns True if the objects are the same, else False
        """
        if not isinstance(other, SubarrayBeamConfiguration):
            return False
        return (
                self.subarray_beam_id == other.subarray_beam_id
                and self.station_ids == other.station_ids
                and self.channels == other.channels
                and self.update_rate == other.update_rate
                and self.sky_coordinates == other.sky_coordinates
                and self.antenna_weights == other.antenna_weights
                and self.phase_centre == other.phase_centre
        )


class ConfigureRequest:
    """
    Class to hold all subarray configuration.
    """

    def __init__(
            self,
            *,  # force kwonly args
            interface: Optional[str] = SCHEMA,
            stations: List[StationConfiguration],
            subarray_beams: List[SubarrayBeamConfiguration]
    ):
        """
        Create a new MCCSConfiguration.

        :param stations: a list of station configurations
        :param subarray_beams: a list of subarray beam configurations
        """
        self.interface = interface
        self.stations = stations
        self.subarray_beams = subarray_beams

    def __eq__(self, other):
        """
        Check for equality between two ConfigureRequest objects

        :param other: the object to check against this object

        :return: returns True if the objects are the same, else False
        """
        if not isinstance(other, ConfigureRequest):
            return False
        return (
                self.interface == other.interface
                and self.stations == other.stations
                and self.subarray_beams == other.subarray_beams
        )
