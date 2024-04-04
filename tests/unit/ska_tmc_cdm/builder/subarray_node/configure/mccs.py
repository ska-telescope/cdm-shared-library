from typing import List

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    SubarrayBeamAperatures,
    SubarrayBeamConfiguration,
    SubarrayBeamLogicalBands,
    SubarrayBeamSkyCoordinates,
)


class SubarrayBeamSkyCoordinatesBuilder:
    def __init__(self):
        self.reference_frame = None
        self.c1 = None
        self.c2 = None

    def set_reference_frame(
        self, reference_frame: str
    ) -> "SubarrayBeamSkyCoordinatesBuilder":
        """
        Set reference frame
        :param: reference_frame: Target coordinate reference frame
        """
        self.reference_frame = reference_frame
        return self

    def set_c1(self, c1: float) -> "SubarrayBeamSkyCoordinatesBuilder":
        """
        Set c1
        :param: c1: c1 specification
        """
        self.c1 = c1
        return self

    def set_c2(self, c2: float) -> "SubarrayBeamSkyCoordinatesBuilder":
        """
        Set c2
        :param: c2: c2 specification
        """
        self.c2 = c2
        return self

    def build(self) -> SubarrayBeamSkyCoordinates:
        """
        Build or create subarray beam target
        :return: CDM subarray beam target instance
        """
        return SubarrayBeamSkyCoordinates(
            reference_frame=self.reference_frame,
            c1=self.c1,
            c2=self.c2,
        )


class SubarrayBeamLogicalbandsBuilder:
    def __init__(self):
        self.start_channel = None
        self.number_of_channels = None

    def set_number_of_channels(
        self, number_of_channels: int
    ) -> "SubarrayBeamLogicalbandsBuilder":
        """
        Set number_of_channels
        :param: number_of_channels: number_of_channels specification
        """
        self.number_of_channels = number_of_channels
        return self

    def set_start_channel(
        self, start_channel: int
    ) -> "SubarrayBeamLogicalbandsBuilder":
        """
        Set start_channel
        :param: start_channel: start_channel specification
        """
        self.start_channel = start_channel
        return self


class SubarrayBeamApertureBuilder:
    def __init__(self):
        self.aperture_id = None
        self.weighting_key_ref = None

    def set_aperture_id(self, aperture_id: int) -> "SubarrayBeamApertureBuilder":
        """
        Set aperture_id
        :param: aperture_id: aperture_id specification
        """
        self.aperture_id = aperture_id
        return self

    def set_weighting_key_ref(
        self, weighting_key_ref: int
    ) -> "SubarrayBeamApertureBuilder":
        """
        Set weighting_key_ref
        :param: weighting_key_ref: weighting_key_ref specification
        """
        self.weighting_key_ref = weighting_key_ref
        return self


class SubarrayBeamConfigurationBuilder:
    def __init__(self):
        self.subarray_beam_id = None
        self.update_rate = None
        self.logical_bands = None
        self.apertures = None
        self.sky_coordinates = None

    def set_subarray_beam_id(
        self, subarray_beam_id: int
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set subarray beam id
        :param: subarray_beam_id: subarray beam id
        """
        self.subarray_beam_id = subarray_beam_id
        return self

    def set_update_rate(self, update_rate: float) -> "SubarrayBeamConfigurationBuilder":
        """
        Set update rate
        :param: update_rate: update rate
        """
        self.update_rate = update_rate
        return self

    def set_logical_bands(
        self, logical_bands: SubarrayBeamLogicalBands
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set logical_bands
        :param: logical_bands: SubarrayBeamLogicalBands Instance
        """
        self.logical_bands = logical_bands
        return self

    def set_apertures(
        self, apertures: SubarrayBeamAperatures
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set apertures
        :param: apertures: SubarrayBeamAperatures Instance
        """
        self.apertures = apertures
        return self

    def set_sky_coordinates(
        self, sky_coordinates: SubarrayBeamSkyCoordinates
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set sky_coordinates
        :param: sky_coordinates: SubarrayBeamSkyCoordinates Instance
        """
        self.sky_coordinates = sky_coordinates
        return self

    def build(self) -> SubarrayBeamConfiguration:
        """
        Build or create subarray beam configuration
        :return: CDM subarray beam configuration instance
        """
        return SubarrayBeamConfiguration(
            update_rate=self.update_rate,
            logical_bands=[
                SubarrayBeamLogicalBands(start_channel=80, number_of_channels=16)
            ],
            apertures=[
                SubarrayBeamAperatures(
                    aperture_id="AP001.01", weighting_key_ref="aperture2"
                )
            ],
            sky_coordinates=SubarrayBeamSkyCoordinates(
                reference_frame="ICRS",
                c1=180.0,
                c2=90.0,
            ),
            subarray_beam_id=self.subarray_beam_id,
        )


class MCCSConfigurationBuilder:
    def __init__(self):
        self.subarray_beam_configs = None

    def set_subarray_beam_config(
        self, subarray_beam_configs: List[SubarrayBeamConfiguration]
    ) -> "MCCSConfigurationBuilder":
        """
        Set subarray beam configuration
        :param subarray_beam_configs: list of subarray beam configuration instance
        """
        self.subarray_beam_configs = subarray_beam_configs
        return self

    def build(self) -> MCCSConfiguration:
        """
        Build or create mccs configuration
        :return: CDM MCCS configuration instance
        """
        return MCCSConfiguration(
            subarray_beam_configs=self.subarray_beam_configs,
        )
