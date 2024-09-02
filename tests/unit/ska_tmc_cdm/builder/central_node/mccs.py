import functools

from ska_tmc_cdm.messages.central_node.mccs import (
    ApertureConfiguration,
    MCCSAllocate,
    SubArrayBeamsConfiguration,
)


class ApertureConfigurationBuilder:
    """
    ApertureConfigurationBuilder is a test data builder for CDM
    ApertureConfiguration objects.
    """

    def __init__(self) -> "ApertureConfigurationBuilder":
        self.station_id = None
        self.aperture_id = None

    def set_station_id(
        self, station_id: int
    ) -> "ApertureConfigurationBuilder":
        """
        Set station_id
        :param station_id: station_id
        """
        self.station_id = station_id
        return self

    def set_aperture_id(
        self, aperture_id: int
    ) -> "ApertureConfigurationBuilder":
        """
        Set aperture_id
        :param aperture_id: aperture_id
        """
        self.aperture_id = aperture_id
        return self

    def build(self) -> ApertureConfiguration:
        """
        Build or create CDM ApertureConfiguration object
        :return: CDM ApertureConfiguration object
        """
        return ApertureConfiguration(
            station_id=self.station_id,
            aperture_id=self.aperture_id,
        )


class SubArrayBeamsConfigurationBuilder:
    """
    SubArrayBeamsConfigurationBuilder is a test data builder for CDM
    SubArrayBeamsConfiguration objects.
    """

    def __init__(self) -> "SubArrayBeamsConfigurationBuilder":
        self.subarray_beam_id = None
        self.apertures: ApertureConfiguration = []
        self.number_of_channels = None

    def set_subarray_beam_id(
        self, subarray_beam_id: list
    ) -> "SubArrayBeamsConfigurationBuilder":
        """
        Set subarray_beam_ids
        :param subarray_beam_ids: subarray_beam_ids
        """
        self.subarray_beam_id = subarray_beam_id
        return self

    def set_apertures(
        self, apertures: ApertureConfiguration
    ) -> "SubArrayBeamsConfigurationBuilder":
        """
        Set apertures
        :param apertures: apertures
        """
        self.apertures = apertures
        return self

    def set_number_of_channels(
        self, number_of_channels: int
    ) -> "SubArrayBeamsConfigurationBuilder":
        """
        Set number_of_channels
        :param number_of_channels: number_of_channels
        """
        self.number_of_channels = number_of_channels
        return self

    def build(self) -> SubArrayBeamsConfiguration:
        """
        Build or create CDM SubArrayBeamsConfiguration object
        :return: CDM SubArrayBeamsConfiguration object
        """
        return SubArrayBeamsConfiguration(
            subarray_beam_id=self.subarray_beam_id,
            apertures=self.apertures,
            number_of_channels=self.number_of_channels,
        )


MCCSAllocateBuilder = functools.partial(
    MCCSAllocate,
    subarray_beam_ids=(1,),
    station_ids=((1, 2),),
    channel_blocks=(3,),
)
