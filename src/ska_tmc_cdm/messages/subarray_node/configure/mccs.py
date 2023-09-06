"""
The configure.mccs module contains Python classes that represent the various
aspects of MCCS configuration that may be specified in a SubArray.configure
command.
"""

from dataclasses import KW_ONLY
from typing import List

from pydantic.dataclasses import dataclass

__all__ = [
    "MCCSConfiguration",
    "StnConfiguration",
    "SubarrayBeamConfiguration",
    "SubarrayBeamTarget",
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


class StnConfiguration:
    """A class to hold station configuration configuration

    :param station_id: stations id
    :type station_id: int
    """

    station_id: int


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

    subarray_beam_id: int
    station_ids: List[int]
    channels: List[List[int]]
    update_rate: float
    target: SubarrayBeamTarget
    antenna_weights: List[float]
    phase_centre: List[float]


class MCCSConfiguration:
    """
    Class to hold all subarray configuration.

    :param station_configs: a list of station configurations
    :type station_configs: List[StnConfiguration]
    :param subarray_beam_configs: a list of subarray beam configurations
    :type subarray_beam_configs: List[SubarrayBeamConfiguration]
    """

    _: KW_ONLY
    station_configs: List[StnConfiguration]
    subarray_beam_configs: List[SubarrayBeamConfiguration]
