from typing import List, Optional

from ska_tmc_cdm.messages.base import CdmObject

__all__ = [
    "PSTScanCoordinates",
    "PSTChannelizationStageConfiguration",
    "PSTScanConfiguration",
    "PSTBeamConfiguration",
    "PSTConfiguration",
]


class PSTScanCoordinates(CdmObject):
    """
    Class to hold Scan coordinates
    :param equinox: equinox value
    :param ra: Right Ascension
    :param dec: Declination
    """

    equinox: float = None
    ra: str = None
    dec: str = None


class PSTChannelizationStageConfiguration(CdmObject):
    """
    Class to hold Channelization Stage configuration items
    :param num_filter_taps: Number of filter taps
    :param filter_coefficients: Filter coefficients
    :param num_frequency_channels: Number of frequency channels
    :param oversampling_ratio: Oversampling ratio
    """

    num_filter_taps: int = None
    filter_coefficients: List[float] = None
    num_frequency_channels: int = None
    oversampling_ratio: List[int] = None


class PSTScanConfiguration(CdmObject):
    """
    Class to hold Scan configuration items
    :param activation_time: Activation time
    :param bits_per_sample: Bits per sample
    :param num_of_polarizations: Number of polarizations
    :param udp_nsamp: UDP nsamp
    :param wt_nsamp: WT nsamp
    :param udp_nchan: UDP nchan
    :param num_frequency_channels: Number of frequency channels
    :param centre_frequency: Centre frequency
    :param total_bandwidth: Total bandwidth
    :param observation_mode: Observation mode
    :param observer_id: Observer ID
    :param project_id: Project ID
    :param pointing_id: Pointing ID
    :param source: Source
    :param itrf: ITRF coordinates
    :param receiver_id: Receiver ID
    :param feed_polarization: Feed polarization
    :param feed_handedness: Feed handedness
    :param feed_angle: Feed angle
    :param feed_tracking_mode: Feed tracking mode
    """

    activation_time: str = None
    bits_per_sample: int = None
    num_of_polarizations: int = None
    udp_nsamp: int = None
    wt_nsamp: int = None
    udp_nchan: int = None
    num_frequency_channels: int = None
    centre_frequency: float = None
    total_bandwidth: float = None
    observation_mode: str = None
    observer_id: str = None
    project_id: str = None
    pointing_id: str = None
    source: str = None
    itrf: List[float] = None
    receiver_id: str = None
    feed_polarization: str = None
    feed_handedness: int = None
    feed_angle: float = None
    feed_tracking_mode: str = None
    feed_position_angle: float = None
    oversampling_ratio: List[int] = None
    coordinates: Optional[PSTScanCoordinates] = None
    max_scan_length: float = None
    subint_duration: float = None
    receptors: List[str] = None
    receptor_weights: List[float] = None
    num_channelization_stages: int = None
    channelization_stages: Optional[
        List[PSTChannelizationStageConfiguration]
    ] = None


class PSTBeamConfiguration(CdmObject):
    """
    Class to hold PST beam configuration items
    :param beam_id: Beam ID
    :param scan: Scan configuration
    """

    beam_id: int = None
    scan: Optional[PSTScanConfiguration] = None


class PSTConfiguration(CdmObject):
    """
    Class to hold PST configuration items
    :param beams: List of beam configurations
    """

    beams: Optional[List[PSTBeamConfiguration]] = None
