from typing import List, Optional

from pydantic import Field

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

    equinox: Optional[float] = None
    ra: Optional[str] = None
    dec: Optional[str] = None


class PSTChannelizationStageConfiguration(CdmObject):
    """
    Class to hold Channelization Stage configuration items
    :param num_filter_taps: Number of filter taps
    :param filter_coefficients: Filter coefficients
    :param num_frequency_channels: Number of frequency channels
    :param oversampling_ratio: Oversampling ratio
    """

    num_filter_taps: Optional[int] = None
    filter_coefficients: List[float] = Field(default_factory=list)
    num_frequency_channels: Optional[int] = None
    oversampling_ratio: List[int] = Field(default_factory=list)


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

    activation_time: Optional[str] = None
    bits_per_sample: int = None
    num_of_polarizations: Optional[int] = None
    udp_nsamp: Optional[int] = None
    wt_nsamp: Optional[int] = None
    udp_nchan: Optional[int] = None
    num_frequency_channels: Optional[int] = None
    centre_frequency: Optional[float] = None
    total_bandwidth: Optional[float] = None
    observation_mode: Optional[str] = None
    observer_id: Optional[str] = None
    project_id: Optional[str] = None
    pointing_id: Optional[str] = None
    source: Optional[str] = None
    itrf: List[float] = Field(default_factory=list)
    receiver_id: Optional[str] = None
    feed_polarization: Optional[str] = None
    feed_handedness: Optional[int] = None
    feed_angle: Optional[float] = None
    feed_tracking_mode: Optional[str] = None
    feed_position_angle: Optional[float] = None
    oversampling_ratio: List[int] = Field(default_factory=list)
    coordinates: Optional[PSTScanCoordinates] = None
    max_scan_length: Optional[float] = None
    subint_duration: Optional[float] = None
    receptors: List[str] = Field(default_factory=list)
    receptor_weights: List[float] = Field(default_factory=list)
    num_channelization_stages: Optional[int] = None
    channelization_stages: List[PSTChannelizationStageConfiguration] = Field(
        default_factory=list
    )


class PSTBeamConfiguration(CdmObject):
    """
    Class to hold PST beam configuration items
    :param beam_id: Beam ID
    :param scan: Scan configuration
    """

    beam_id: Optional[int] = None
    scan: Optional[PSTScanConfiguration] = None


class PSTConfiguration(CdmObject):
    """
    Class to hold PST configuration items
    :param beams: List of beam configurations
    """

    beams: List[PSTBeamConfiguration] = Field(default_factory=list)
