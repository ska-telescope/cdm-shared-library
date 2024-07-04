from typing import List

from ska_tmc_cdm.messages.subarray_node.configure.pst import (
    PSTBeamConfiguration,
    PSTChannelizationStageConfiguration,
    PSTConfiguration,
    PSTScanConfiguration,
    PSTScanCoordinates,
)


class PSTScanCoordinatesBuilder:
    def __init__(self):
        self.equinox = None
        self.ra = None
        self.dec = None

    def set_equinox(self, equinox: float) -> "PSTScanCoordinatesBuilder":
        """
        Set equinox
        :param: equinox: equinox specification
        """
        self.equinox = equinox
        return self

    def set_ra(self, ra: str) -> "PSTScanCoordinatesBuilder":
        """
        Set ra
        :param: ra: ra specification
        """
        self.ra = ra
        return self

    def set_dec(self, dec: str) -> "PSTScanCoordinatesBuilder":
        """
        Set dec
        :param: dec: dec specification
        """
        self.dec = dec
        return self

    def build(self) -> PSTScanCoordinates:
        """
        Build ScanCoordinates object
        :return: ScanCoordinates object
        """
        return PSTScanCoordinates(
            equinox=self.equinox, ra=self.ra, dec=self.dec
        )


class PSTChannelizationStageConfigurationBuilder:
    def __init__(self):
        self.num_filter_taps = None
        self.filter_coefficients = None
        self.num_frequency_channels = None
        self.oversampling_ratio = None

    def set_num_filter_taps(
        self, num_filter_taps: int
    ) -> "PSTChannelizationStageConfigurationBuilder":
        """
        Set num_filter_taps
        :param: num_filter_taps: num_filter_taps specification
        """
        self.num_filter_taps = num_filter_taps
        return self

    def set_filter_coefficients(
        self, filter_coefficients: List[float]
    ) -> "PSTChannelizationStageConfigurationBuilder":
        """
        Set filter_coefficients
        :param: filter_coefficients: filter_coefficients specification
        """
        self.filter_coefficients = filter_coefficients
        return self

    def set_num_frequency_channels(
        self, num_frequency_channels: int
    ) -> "PSTChannelizationStageConfigurationBuilder":
        """
        Set num_frequency_channels
        :param: num_frequency_channels: num_frequency_channels specification
        """
        self.num_frequency_channels = num_frequency_channels
        return self

    def set_oversampling_ratio(
        self, oversampling_ratio: List[int]
    ) -> "PSTChannelizationStageConfigurationBuilder":
        """
        Set oversampling_ratio
        :param: oversampling_ratio: oversampling_ratio specification
        """
        self.oversampling_ratio = oversampling_ratio
        return self

    def build(self) -> PSTChannelizationStageConfiguration:
        """
        Build ChannelizationStageConfiguration object
        :return: ChannelizationStageConfiguration object
        """
        return PSTChannelizationStageConfiguration(
            num_filter_taps=self.num_filter_taps,
            filter_coefficients=self.filter_coefficients,
            num_frequency_channels=self.num_frequency_channels,
            oversampling_ratio=self.oversampling_ratio,
        )


class PSTScanConfigurationBuilder:
    def __init__(self):
        self.activation_time = None
        self.bits_per_sample = None
        self.num_of_polarizations = None
        self.udp_nsamp = None
        self.wt_nsamp = None
        self.udp_nchan = None
        self.num_frequency_channels = None
        self.centre_frequency = None
        self.total_bandwidth = None
        self.observation_mode = None
        self.observer_id = None
        self.project_id = None
        self.pointing_id = None
        self.source = None
        self.itrf = []
        self.receiver_id = None
        self.feed_polarization = None
        self.feed_handedness = None
        self.feed_angle = None
        self.feed_tracking_mode = None
        self.feed_position_angle = None
        self.oversampling_ratio = []
        self.coordinates = None
        self.max_scan_length = None
        self.subint_duration = None
        self.receptors = []
        self.receptor_weights = []
        self.num_channelization_stages = []
        self.channelization_stages = None

    def set_activation_time(
        self, activation_time: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set activation_time
        :param: activation_time: activation_time specification
        """
        self.activation_time = activation_time
        return self

    def set_bits_per_sample(
        self, bits_per_sample: int
    ) -> "PSTScanConfigurationBuilder":
        """
        Set bits_per_sample
        :param: bits_per_sample: bits_per_sample specification
        """
        self.bits_per_sample = bits_per_sample
        return self

    def set_num_of_polarizations(
        self, num_of_polarizations: int
    ) -> "PSTScanConfigurationBuilder":
        """
        Set num_of_polarizations
        :param: num_of_polarizations: num_of_polarizations specification
        """
        self.num_of_polarizations = num_of_polarizations
        return self

    def set_udp_nsamp(self, udp_nsamp: int) -> "PSTScanConfigurationBuilder":
        """
        Set udp_nsamp
        :param: udp_nsamp: udp_nsamp specification
        """
        self.udp_nsamp = udp_nsamp
        return self

    def set_wt_nsamp(self, wt_nsamp: int) -> "PSTScanConfigurationBuilder":
        """
        Set wt_nsamp
        :param: wt_nsamp: wt_nsamp specification
        """
        self.wt_nsamp = wt_nsamp
        return self

    def set_udp_nchan(self, udp_nchan: int) -> "PSTScanConfigurationBuilder":
        """
        Set udp_nchan
        :param: udp_nchan: udp_nchan specification
        """
        self.udp_nchan = udp_nchan
        return self

    def set_num_frequency_channels(
        self, num_frequency_channels: int
    ) -> "PSTScanConfigurationBuilder":
        """
        Set num_frequency_channels
        :param: num_frequency_channels: num_frequency_channels specification
        """
        self.num_frequency_channels = num_frequency_channels
        return self

    def set_centre_frequency(
        self, centre_frequency: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set centre_frequency
        :param: centre_frequency: centre_frequency specification
        """
        self.centre_frequency = centre_frequency
        return self

    def set_total_bandwidth(
        self, total_bandwidth: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set total_bandwidth
        :param: total_bandwidth: total_bandwidth specification
        """
        self.total_bandwidth = total_bandwidth
        return self

    def set_observation_mode(
        self, observation_mode: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set observation_mode
        :param: observation_mode: observation_mode specification
        """
        self.observation_mode = observation_mode
        return self

    def set_observer_id(
        self, observer_id: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set observer_id
        :param: observer_id: observer_id specification
        """
        self.observer_id = observer_id
        return self

    def set_project_id(self, project_id: str) -> "PSTScanConfigurationBuilder":
        """
        Set project_id
        :param: project_id: project_id specification
        """
        self.project_id = project_id
        return self

    def set_pointing_id(
        self, pointing_id: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set pointing_id
        :param: pointing_id: pointing_id specification
        """
        self.pointing_id = pointing_id
        return self

    def set_source(self, source: str) -> "PSTScanConfigurationBuilder":
        """
        Set source
        :param: source: source specification
        """
        self.source = source
        return self

    def set_itrf(self, itrf: List[float]) -> "PSTScanConfigurationBuilder":
        """
        Set itrf
        :param: itrf: itrf specification
        """
        self.itrf = itrf
        return self

    def set_receiver_id(
        self, receiver_id: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set receiver_id
        :param: receiver_id: receiver_id specification
        """
        self.receiver_id = receiver_id
        return self

    def set_feed_polarization(
        self, feed_polarization: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set feed_polarization
        :param: feed_polarization: feed_polarization specification
        """
        self.feed_polarization = feed_polarization
        return self

    def set_feed_handedness(
        self, feed_handedness: int
    ) -> "PSTScanConfigurationBuilder":
        """
        Set feed_handedness
        :param: feed_handedness: feed_handedness specification
        """
        self.feed_handedness = feed_handedness
        return self

    def set_feed_angle(
        self, feed_angle: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set feed_angle
        :param: feed_angle: feed_angle specification
        """
        self.feed_angle = feed_angle
        return self

    def set_feed_tracking_mode(
        self, feed_tracking_mode: str
    ) -> "PSTScanConfigurationBuilder":
        """
        Set feed_tracking_mode
        :param: feed_tracking_mode: feed_tracking_mode specification
        """
        self.feed_tracking_mode = feed_tracking_mode
        return self

    def set_feed_position_angle(
        self, feed_position_angle: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set feed_position_angle
        :param: feed_position_angle: feed_position_angle specification
        """
        self.feed_position_angle = feed_position_angle
        return self

    def set_oversampling_ratio(
        self, oversampling_ratio: List[int]
    ) -> "PSTScanConfigurationBuilder":
        """
        Set oversampling_ratio
        :param: oversampling_ratio: oversampling_ratio specification
        """
        self.oversampling_ratio = oversampling_ratio
        return self

    def set_coordinates(
        self, coordinates: PSTScanCoordinates
    ) -> "PSTScanConfigurationBuilder":
        """
        Set coordinates
        :param: coordinates: coordinates specification
        """
        self.coordinates = coordinates
        return self

    def set_max_scan_length(
        self, max_scan_length: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set max_scan_length
        :param: max_scan_length: max_scan_length specification
        """
        self.max_scan_length = max_scan_length
        return self

    def set_subint_duration(
        self, subint_duration: float
    ) -> "PSTScanConfigurationBuilder":
        """
        Set subint_duration
        :param: subint_duration: subint_duration specification
        """
        self.subint_duration = subint_duration
        return self

    def set_receptors(
        self, receptors: List[str]
    ) -> "PSTScanConfigurationBuilder":
        """
        Set receptors
        :param: receptors: receptors specification
        """
        self.receptors = receptors
        return self

    def set_receptor_weights(
        self, receptor_weights: List[float]
    ) -> "PSTScanConfigurationBuilder":
        """
        Set receptor_weights
        :param: receptor_weights: receptor_weights specification
        """
        self.receptor_weights = receptor_weights
        return self

    def set_num_channelization_stages(
        self, num_channelization_stages: int
    ) -> "PSTScanConfigurationBuilder":
        """
        Set num_channelization_stages
        :param: num_channelization_stages: num_channelization_stages specification
        """
        self.num_channelization_stages = num_channelization_stages
        return self

    def set_channelization_stages(
        self, channelization_stages: List[PSTChannelizationStageConfiguration]
    ) -> "PSTScanConfigurationBuilder":
        """
        Set channelization_stages
        :param: channelization_stages: channelization_stages specification
        """
        self.channelization_stages = channelization_stages
        return self

    def build(self) -> PSTScanConfiguration:
        """
        Build the ScanConfiguration object
        """
        return PSTScanConfiguration(
            activation_time=self.activation_time,
            bits_per_sample=self.bits_per_sample,
            num_of_polarizations=self.num_of_polarizations,
            udp_nsamp=self.udp_nsamp,
            wt_nsamp=self.wt_nsamp,
            udp_nchan=self.udp_nchan,
            num_frequency_channels=self.num_frequency_channels,
            centre_frequency=self.centre_frequency,
            total_bandwidth=self.total_bandwidth,
            observation_mode=self.observation_mode,
            observer_id=self.observer_id,
            project_id=self.project_id,
            pointing_id=self.pointing_id,
            source=self.source,
            itrf=self.itrf,
            receiver_id=self.receiver_id,
            feed_polarization=self.feed_polarization,
            feed_handedness=self.feed_handedness,
            feed_angle=self.feed_angle,
            feed_tracking_mode=self.feed_tracking_mode,
            feed_position_angle=self.feed_position_angle,
            oversampling_ratio=self.oversampling_ratio,
            coordinates=self.coordinates,
            max_scan_length=self.max_scan_length,
            subint_duration=self.subint_duration,
            receptors=self.receptors,
            receptor_weights=self.receptor_weights,
            num_channelization_stages=self.num_channelization_stages,
            channelization_stages=self.channelization_stages,
        )


class PSTBeamConfigurationBuilder:
    def __init__(self):
        self.beam_id = None
        self.scan = None

    def set_beam_id(self, beam_id: int) -> "PSTBeamConfigurationBuilder":
        self.beam_id = beam_id
        return self

    def set_scan(
        self, scan: PSTScanConfiguration
    ) -> "PSTBeamConfigurationBuilder":
        self.scan = scan
        return self

    def build(self) -> PSTBeamConfiguration:
        return PSTBeamConfiguration(
            beam_id=self.beam_id,
            scan=self.scan,
        )


class PSTConfigurationBuilder:
    def __init__(self):
        self.beams = []

    def set_beams(
        self, beam: PSTBeamConfiguration
    ) -> "PSTConfigurationBuilder":
        self.beams = beam
        return self

    def build(self) -> PSTConfiguration:
        return PSTConfiguration(
            beams=self.beams,
        )
