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


class MCCSAllocateBuilder:
    """
    MCCSAllocateBuilder is a test data builder for CDM MCCSAllocate objects.

    By default, MCCSAllocateBuilder will build an MCCSAllocate

    for low observation command.
    """

    def __init__(self) -> "MCCSAllocateBuilder":
        self.subarray_beam_ids = None
        self.channel_blocks = None
        self.station_ids = None
        self.interface = None
        self.subarray_beams: SubArrayBeamsConfiguration = []

    def set_subarray_beam_ids(
        self, subarray_beam_ids: list
    ) -> "MCCSAllocateBuilder":
        """
        Set subarray_beam_ids
        :param subarray_beam_ids: subarray_beam_ids
        """
        self.subarray_beam_ids = subarray_beam_ids
        return self

    def set_station_ids(self, station_ids: list) -> "MCCSAllocateBuilder":
        """
        Set station_ids
        :param station_ids: station_ids
        """
        self.station_ids = station_ids
        return self

    def set_channel_blocks(
        self, channel_blocks: list
    ) -> "MCCSAllocateBuilder":
        """
        Set channel_blocks
        :param channel_blocks: channel_blocks
        """
        self.channel_blocks = channel_blocks
        return self

    def set_interface(self, interface: str) -> "MCCSAllocateBuilder":
        """
        Set interface
        :param interface: interface
        """
        self.interface = interface
        return self

    def set_subarray_beams(
        self, subarray_beams: SubArrayBeamsConfiguration
    ) -> "MCCSAllocateBuilder":
        """
        Set subarray_beams
        :param subarray_beams: subarray_beams
        """
        self.subarray_beams = subarray_beams
        return self

    def build(self) -> MCCSAllocate:
        """
        Build or create CDM MCCSAllocate object
        :return: CDM MCCSAllocate object
        """
        return MCCSAllocate(
            subarray_beam_ids=self.subarray_beam_ids,
            station_ids=self.station_ids,
            channel_blocks=self.channel_blocks,
            interface=self.interface,
            subarray_beams=self.subarray_beams,
        )
