"""
The configure.mccs module contains Python classes that represent the various
aspects of MCCS configuration that may be specified in a SubArray.configure
command.
"""

from typing import List, Optional

from pydantic import AliasChoices, Field

from ska_tmc_cdm.messages.base import CdmObject

__all__ = [
    "MCCSConfiguration",
    "SubarrayBeamConfiguration",
    "SubarrayBeamSkyCoordinates",
    "SubarrayBeamLogicalBands",
    "SubarrayBeamAperatures",
]


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

    reference_frame: Optional[str] = None
    c1: Optional[float] = None
    c2: Optional[float] = None


class SubarrayBeamLogicalBands(CdmObject):
    """
    A class to hold Subarray Beam logical bands configuration items
    :param start_channel: Start channel value.
    :type start_channel: str
    :param number_of_channels: No of channels
    :type number_of_channels: str
    """

    start_channel: Optional[int] = None
    number_of_channels: Optional[int] = None


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

    aperture_id: Optional[str] = None
    weighting_key_ref: Optional[str] = None


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


class MCCSConfiguration(CdmObject):
    """
    Class to hold all subarray configuration.
    :param subarray_beam_configs: a list of subarray beam configurations
    :type subarray_beam_configs: List[SubarrayBeamConfiguration]
    """

    subarray_beam_configs: List[SubarrayBeamConfiguration] = Field(
        serialization_alias="subarray_beams",
        validation_alias=AliasChoices(
            "subarray_beams", "subarray_beam_configs"
        ),
    )
