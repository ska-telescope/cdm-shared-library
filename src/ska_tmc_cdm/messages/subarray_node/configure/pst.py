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
    """

    equinox: float = None
    ra: str = None
    dec: str = None


class PSTChannelizationStageConfiguration(CdmObject):
    """
    Class to hold Channelization Stage configuration items
    """

    num_filter_taps: int = None
    filter_coefficients: List[float] = None
    num_frequency_channels: int = None
    oversampling_ratio: List[int] = None


class PSTScanConfiguration(CdmObject):
    """
    Class to hold Scan configuration items
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
    coordinates: PSTScanCoordinates = None
    max_scan_length: float = None
    subint_duration: float = None
    receptors: List[str] = None
    receptor_weights: List[float] = None
    num_channelization_stages: int = None
    channelization_stages: List[PSTChannelizationStageConfiguration] = None


class PSTBeamConfiguration(CdmObject):
    """
    Class to hold PST beam configuration items
    """

    beam_id: int = None
    scan: Optional[PSTScanConfiguration] = None


class PSTConfiguration(CdmObject):
    """
    Class to hold PST configuration items
    """

    beams: List[PSTBeamConfiguration] = None
