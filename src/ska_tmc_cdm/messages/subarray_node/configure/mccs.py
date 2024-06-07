"""
The configure.mccs module contains Python classes that represent the various
aspects of MCCS configuration that may be specified in a SubArray.configure
command.
"""

from typing import List, Optional

from pydantic.dataclasses import dataclass

__all__ = [
    "MCCSConfiguration",
    "SubarrayBeamConfiguration",
    "SubarrayBeamSkyCoordinates",
    "SubarrayBeamLogicalBands",
    "SubarrayBeamAperatures",
]


from ska_tmc_cdm.messages.base import CdmObject


class SubarrayBeamSkyCoordinates(CdmObject):
    """
    A class to hold Subarray Beam sky coordinates configuration items
    :param reference_frame: Must be one of: ["topocentric", "ICRS", "galactic"]
    :type reference_frame: str
    :param c1: first coordinate, RA or azimuth, in degrees
    :type c1: float
    :param c2: second coordinate, RA or azimuth, in degrees
    :type c2: float
    """

    reference_frame: str = None
    c1: float = None
    c2: float = None


from ska_tmc_cdm.messages.base import CdmObject


class SubarrayBeamLogicalBands(CdmObject):
    """
    A class to hold Subarray Beam logical bands configuration items
    :param start_channel: Start channel value.
    :type start_channel: str
    :param number_of_channels: No of channels
    :type number_of_channels: str
    """

    start_channel: int = None
    number_of_channels: int = None


from ska_tmc_cdm.messages.base import CdmObject


class SubarrayBeamAperatures(CdmObject):
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


from ska_tmc_cdm.messages.base import CdmObject


class SubarrayBeamConfiguration(CdmObject):
    """A class to hold subarray_beam configuration attributes

    :param subarray_beam_id: stationbeam's id
    :type subarray_beam_id: int
    :param update_rate: frequency of new Az/El during scan
    :type update_rate: float
    """

    update_rate: float
    logical_bands: List[SubarrayBeamLogicalBands]
    apertures: List[SubarrayBeamAperatures]
    sky_coordinates: SubarrayBeamSkyCoordinates
    subarray_beam_id: Optional[int] = None


from ska_tmc_cdm.messages.base import CdmObject


class MCCSConfiguration(CdmObject):
    """
    Class to hold all subarray configuration.
    :param subarray_beam_configs: a list of subarray beam configurations
    :type subarray_beam_configs: List[SubarrayBeamConfiguration]
    """

    subarray_beam_configs: List[SubarrayBeamConfiguration]
