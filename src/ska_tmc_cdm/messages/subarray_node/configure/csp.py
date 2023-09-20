"""
The configure.csp module contains Python classes that represent the various
aspects of CSP configuration that may be specified in a SubArrayNode.configure
command.
"""
from enum import Enum
from typing import List, Optional, Tuple

from pydantic import Field
from pydantic.dataclasses import dataclass

from . import core

__all__ = [
    "CSPConfiguration",
    "FSPConfiguration",
    "FSPFunctionMode",
    "CBFConfiguration",
    "SubarrayConfiguration",
    "CommonConfiguration",
    "LowCBFConfiguration",
    "TimingBeamConfiguration",
    "BeamConfiguration",
    "StationConfiguration",
    "StnBeamConfiguration",
]


class FSPFunctionMode(Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """

    CORR = "CORR"
    PSS_BF = "PSS-BF"
    PST_BF = "PST-BF"
    VLBI = "VLBI"


@dataclass
class FSPConfiguration:
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.

    Channel averaging map is an optional list of 20 x (int,int) tuples.

    :param fsp_id: FSP configuration ID [1..27]
    :param function_mode: FSP function mode
    :param frequency_slice_id: frequency slicer ID [1..26]
    :param zoom_factor: zoom factor [0..6]
    :param integration_factor: integration factor [1..10]
    :param channel_averaging_map: Optional channel averaging map
    :param output_link_map: Optional output link map
    :param channel_offset: Optional FSP channel offset
    :param zoom_window_tuning: Optional zoom window tuning

    :raises ValueError: Invalid parameter values entered
    """

    fsp_id: int = Field(ge=1, le=27)  # 1 <= id <= 27
    function_mode: FSPFunctionMode = Field()
    frequency_slice_id: int = Field(ge=1, le=26)
    integration_factor: int = Field(ge=1, le=10)
    zoom_factor: int = Field(ge=0, le=6)
    # FIXME: should be Field(default_factory=list, max_length=20)?
    channel_averaging_map: Optional[List[Tuple]] = Field(None, max_length=20)
    # could we add enforcements for output_link_map? What are the limits?
    output_link_map: Optional[List[Tuple]] = None  # FIXME: Field(default_factory=list)?
    channel_offset: Optional[int] = None
    zoom_window_tuning: Optional[int] = None


@dataclass
class SubarrayConfiguration:
    """
    Class to hold the parameters relevant only for the current sub-array device.

    :param sub-array_name: Name of the sub-array
    """

    subarray_name: str


@dataclass
class CommonConfiguration:
    """
    Class to hold the CSP sub-elements.

    :param config_id: CSP configuration ID
    :param frequency_band: the frequency band to set
    :param subarray_id: an ID of sub-array device
    :param band_5_tuning: band 5 receiver to set (optional)
    """

    config_id: str
    frequency_band: Optional[core.ReceiverBand] = None
    subarray_id: Optional[int] = None
    band_5_tuning: Optional[List[float]] = None


@dataclass
class StnBeamConfiguration:
    """
    Class to hold Stations Beam Configuration.

    :param beam_id: beam_id
    :param freq_ids: freq_ids
    :param boresight_dly_poly: boresight_dly_poly
    """

    beam_id: Optional[int] = None
    freq_ids: Optional[List[int]] = None
    boresight_dly_poly: Optional[str] = None


@dataclass
class StationConfiguration:
    """
    Class to hold Stations Configuration.

    :param stns: stns
    :param stn_beams: stn_beams
    """

    stns: Optional[List[List[int]]] = None
    stn_beams: Optional[List[StnBeamConfiguration]] = None


@dataclass
class BeamConfiguration:
    """
    Class to hold Beams Configuration.

    :param pst_beam_id: pst_beam_id
    :param stn_beam_id: stn_beam_id
    :param offset_dly_poly: offset_dly_poly
    :param stn_weights: stn_weights
    :param jones: jones
    :param dest_chans: dest_chans
    :param rfi_enable: rfi_enable
    :param rfi_static_chans: rfi_static_chans
    :param rfi_dynamic_chans: rfi_dynamic_chans
    :param rfi_weighted: rfi_weighted
    """

    pst_beam_id: Optional[int] = None
    stn_beam_id: Optional[int] = None
    offset_dly_poly: Optional[str] = None
    stn_weights: Optional[List[float]] = None
    jones: Optional[str] = None
    dest_chans: Optional[List[int]] = None
    rfi_enable: Optional[List[bool]] = None
    rfi_static_chans: Optional[List[int]] = None
    rfi_dynamic_chans: Optional[List[int]] = None
    rfi_weighted: Optional[float] = None


@dataclass
class TimingBeamConfiguration:
    """
    Class to hold Timing Beams Configuration.

    :param beams: beams
    """

    beams: Optional[List[BeamConfiguration]] = None


@dataclass
class LowCBFConfiguration:
    """
    Class to hold Low CBF Configuration.

    :param stations: stations
    :param timing_beams: PST beams subarray list
    """

    stations: Optional[StationConfiguration] = None
    timing_beams: Optional[TimingBeamConfiguration] = None


@dataclass
class VLBIConfiguration:
    pass


@dataclass
class CBFConfiguration:
    """
    Class to hold all FSP and VLBI configurations.

    :param fsp_configs: the FSP configurations to set
    :param vlbi_config: the VLBI configurations to set, it is optional
    """

    fsp_configs: List[FSPConfiguration]
    # TODO: In future when csp Interface 2.2 will be used than type of vlbi_config parameter # pylint: disable=W0511
    #  will be replaced with the respective class(VLBIConfiguration)
    vlbi_config: Optional[dict] = None


@dataclass
class PSTConfiguration:
    pass


@dataclass
class PSSConfiguration:
    pass


@dataclass
class CSPConfiguration:
    """
    Class to hold all CSP configuration. In order to support backward
    compatibility, We have kept old attributes as it is and added
    support of new attributes as per ADR-18

    :param interface: url string to determine JsonSchema version
    :param subarray: Sub-array configuration to set
    :param common: the common CSP elemenets to set
    :param cbf_config: the CBF configurations to set
    :param pst_config: the PST configurations to set
    :param pss_config: the PSS configurations to set
    """

    interface: Optional[str] = None
    subarray: Optional[SubarrayConfiguration] = None
    common: Optional[CommonConfiguration] = None
    cbf_config: Optional[CBFConfiguration] = None
    # TODO: In the future when csp Interface 2.2 is adopted, pst_config and pss_config # pylint: disable=W0511
    # should not accept dict types as inputs.
    pst_config: Optional[PSTConfiguration | dict] = None
    pss_config: Optional[PSSConfiguration | dict] = None
    lowcbf: Optional[LowCBFConfiguration] = None
