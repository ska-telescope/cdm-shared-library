"""
The configure.mccs module contains Python classes that represent the various
aspects of MCCS configuration that may be specified in a SubArray.configure
command.
"""

from typing import List

__all__ = ["MCCSConfiguration", "StnConfiguration", "StnBeamConfiguration"]


class StnConfiguration:
    """A class to hold station configuration configuration"""

    def __init__(self, station_id: int):
        """
        Initialise the station configuration.

        :param station_id: stations id
        :type station_id: int
        """
        self.station_id = station_id

    def __eq__(self, other):
        """
        Check for equality between two station configuration objects

        :param other: the object to check against this object
        :type other: station configuration object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, StnConfiguration):
            return False
        return self.station_id == other.station_id


class StnBeamConfiguration:
    """A class to hold station_beam configuration attributes"""

    def __init__(
        self,
        station_beam_id: int,
        station_ids: List[int],
        channels: List[int],
        update_rate: float,
        sky_coordinates: List[float],
    ):
        """
        Initialise the station beam configuration.

        :param station_beam_id: stationbeam's id
        :type station_beam_id: int
        :param station_ids: station id's
        :type station_ids: List[int]
        :param channels: channels to form station beam
        :type channels: List[int]
        :param update_rate: frequency of new Az/El during scan
        :type update_rate: float
        :param sky_coordinates: Az/El specification with rates
        :type sky_coordinates: List[float]
        """
        self.station_beam_id = station_beam_id
        self.station_ids = station_ids
        self.channels = channels
        self.update_rate = update_rate
        self.sky_coordinates = sky_coordinates

    def __eq__(self, other):
        """
        Check for equality between two station beam configuration objects

        :param other: the object to check against this object
        :type other: station beam configuration object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, StnBeamConfiguration):
            return False
        return (
            self.station_beam_id == other.station_beam_id
            and self.station_ids == other.station_ids
            and self.channels == other.channels
            and self.update_rate == other.update_rate
            and self.sky_coordinates == other.sky_coordinates
        )


class MCCSConfiguration:
    """
    Class to hold all subarray configuration.
    """

    def __init__(
        self,
        station_configs: List[StnConfiguration],
        station_beam_configs: List[StnBeamConfiguration],
    ):
        """
        Create a new MCCSConfiguration.

        :param station_configs: a list of station configurations
        :type station_configs: List[StnConfiguration]
        :param station_beam_configs: a list of station beam configurations
        :type station_beam_configs: List[StnBeamConfiguration]
        """
        self.station_configs = station_configs
        self.station_beam_configs = station_beam_configs

    def __eq__(self, other):
        """
        Check for equality between two mccs configuration objects

        :param other: the object to check against this object
        :type other: mccs configuration object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, MCCSConfiguration):
            return False
        return (
            self.station_configs == other.station_configs
            and self.station_beam_configs == other.station_beam_configs
        )
