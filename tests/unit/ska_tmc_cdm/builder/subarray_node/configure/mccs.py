from typing import List

from ska_tmc_cdm.messages.subarray_node.configure.mccs import (
    MCCSConfiguration,
    StnConfiguration,
    SubarrayBeamConfiguration,
    SubarrayBeamTarget,
)


class SubarrayBeamTargetBuilder:
    def __init__(self):
        self.az = None
        self.el = None
        self.target_name = None
        self.reference_frame = None

    def set_az(self, az: float) -> "SubarrayBeamTargetBuilder":
        """
        Set Az
        :param: az: Az specification with rates
        """
        self.az = az
        return self

    def set_el(self, el: float) -> "SubarrayBeamTargetBuilder":
        """
        Set El
        :param: el: El specification with rates
        """
        self.el = el
        return self

    def set_target_name(self, target_name: str) -> "SubarrayBeamTargetBuilder":
        """
        Set target name
        :param: target_name: target name
        """
        self.target_name = target_name
        return self

    def set_reference_frame(self, reference_frame: str) -> "SubarrayBeamTargetBuilder":
        """
        Set reference frame
        :param: reference_frame: Target coordinate reference frame
        """
        self.reference_frame = reference_frame
        return self

    def build(self) -> SubarrayBeamTarget:
        """
        Build or create subarray beam target
        :return: CDM subarray beam target instance
        """
        return SubarrayBeamTarget(
            az=self.az,
            el=self.el,
            target_name=self.target_name,
            reference_frame=self.reference_frame,
        )


class StnConfigurationBuilder:
    def __init__(self):
        self.station_id = None

    def set_station_id(self, station_id: int) -> "StnConfigurationBuilder":
        """
        Set station id
        :param: station_id: station id
        """
        self.station_id = station_id
        return self

    def build(self) -> StnConfiguration:
        """
        Build or create station configuration
        :return: CDM station configuration instance
        """
        return StnConfiguration(station_id=self.station_id)


class SubarrayBeamConfigurationBuilder:
    def __init__(self):
        self.subarray_beam_id = None
        self.station_ids = None
        self.channels = None
        self.update_rate = None
        self.target = None
        self.antenna_weights = None
        self.phase_centre = None

    def set_subarray_beam_id(
        self, subarray_beam_id: int
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set subarray beam id
        :param: subarray_beam_id: subarray beam id
        """
        self.subarray_beam_id = subarray_beam_id
        return self

    def set_station_ids(
        self, station_ids: List[int]
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set station ids
        :param: station_ids: list of station ids
        """
        self.station_ids = station_ids
        return self

    def set_channels(
        self, channels: List[List[int]]
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set channels
        :param: channels: list of channel list
        """
        self.channels = channels
        return self

    def set_update_rate(self, update_rate: float) -> "SubarrayBeamConfigurationBuilder":
        """
        Set update rate
        :param: update_rate: update rate
        """
        self.update_rate = update_rate
        return self

    def set_target(
        self, target: SubarrayBeamTarget
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set target
        :param: target: SubarrayBeamTarget Instance
        """
        self.target = target
        return self

    def set_antenna_weights(
        self, antenna_weights: List[float]
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set antenna weights
        :param: antenna_weights: list of antenna weights
        """
        self.antenna_weights = antenna_weights
        return self

    def set_phase_centre(
        self, phase_centre: List[float]
    ) -> "SubarrayBeamConfigurationBuilder":
        """
        Set phase centre
        :param: phase_centre: list of phase centre
        """
        self.phase_centre = phase_centre
        return self

    def build(self) -> SubarrayBeamConfiguration:
        """
        Build or create subarray beam configuration
        :return: CDM subarray beam configuration instance
        """
        return SubarrayBeamConfiguration(
            subarray_beam_id=self.subarray_beam_id,
            station_ids=self.station_ids,
            channels=self.channels,
            update_rate=self.update_rate,
            target=self.target,
            antenna_weights=self.antenna_weights,
            phase_centre=self.phase_centre,
        )


class MCCSConfigurationBuilder:
    def __init__(self):
        self.station_configs = None
        self.subarray_beam_configs = None

    def set_station_configs(
        self, station_configs: List[StnConfiguration]
    ) -> "MCCSConfigurationBuilder":
        """
        Set station configuration
        :param station_configs: list of station configuration instance
        """
        self.station_configs = station_configs
        return self

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
            station_configs=self.station_configs,
            subarray_beam_configs=self.subarray_beam_configs,
        )
