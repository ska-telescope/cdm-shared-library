"""
The configure.csp module contains Python classes that represent the various
aspects of CSP configuration that may be specified in a SubArrayNode.configure
command.
"""
import enum
from typing import List, Optional, Tuple

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


class FSPFunctionMode(enum.Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """

    CORR = "CORR"
    PSS_BF = "PSS-BF"
    PST_BF = "PST-BF"
    VLBI = "VLBI"


class FSPConfiguration:
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fsp_id: int,
        function_mode: FSPFunctionMode,
        frequency_slice_id: int,
        integration_factor: int,
        zoom_factor: int,
        channel_averaging_map: List[Tuple] = None,
        output_link_map: List[Tuple] = None,
        channel_offset: int = None,
        zoom_window_tuning: int = None,
    ) -> object:
        """
        Create a new FSPConfiguration.

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

        if not 1 <= fsp_id <= 27:
            raise ValueError("FSP ID must be in range 1..27. Got {}".format(fsp_id))
        self.fsp_id = fsp_id

        self.function_mode = function_mode

        if not 1 <= frequency_slice_id <= 26:
            msg = "Frequency slice ID must be in range 1..26. Got {}" "".format(
                frequency_slice_id
            )
            raise ValueError(msg)
        self.frequency_slice_id = frequency_slice_id

        if not 0 <= zoom_factor <= 6:
            msg = "Zoom factor must be in range 0..6. Got {}".format(zoom_factor)
            raise ValueError(msg)
        self.zoom_factor = zoom_factor

        if not 1 <= integration_factor <= 10:
            msg = "Integration factor must in range 1..10. Got {}" "".format(
                integration_factor
            )
            raise ValueError(msg)
        self.integration_factor = integration_factor

        if channel_averaging_map and len(channel_averaging_map) > 20:
            msg = (
                "Number of tuples in channel averaging map must be 20 or fewer."
                f"Got {len(channel_averaging_map)}"
            )

            raise ValueError(msg)
        self.channel_averaging_map = channel_averaging_map

        # could we add enforcements for output_link_map? What are the limits?
        self.output_link_map = output_link_map
        self.channel_offset = channel_offset
        self.zoom_window_tuning = zoom_window_tuning

    def __eq__(self, other):
        if not isinstance(other, FSPConfiguration):
            return False
        return (
            self.fsp_id == other.fsp_id
            and self.function_mode == other.function_mode
            and self.frequency_slice_id == other.frequency_slice_id
            and self.zoom_factor == other.zoom_factor
            and self.integration_factor == other.integration_factor
            and self.channel_averaging_map == other.channel_averaging_map
            and self.output_link_map == other.output_link_map
            and self.channel_offset == other.channel_offset
            and self.zoom_window_tuning == other.zoom_window_tuning
        )


class SubarrayConfiguration:
    """
    Class to hold the parameters relevant only for the current sub-array device.
    """

    def __init__(self, subarray_name: str) -> object:
        """
        Create  sub-array device configuration.
        :param sub-array_name: Name of the sub-array
        """
        self.subarray_name = subarray_name

    def __eq__(self, other):
        if not isinstance(other, SubarrayConfiguration):
            return False
        return self.subarray_name == other.subarray_name


class CommonConfiguration:
    """
    Class to hold the CSP sub-elements.
    """

    def __init__(
        self,
        config_id: str = None,
        frequency_band: core.ReceiverBand = None,
        subarray_id: int = None,
        band_5_tuning: Optional[List[float]] = None,
    ) -> object:
        """
        Create a new CSPConfiguration.

        :param config_id: CSP configuration ID
        :param frequency_band: the frequency band to set
        :param subarray_id: an ID of sub-array device
        :param band_5_tuning: band 5 receiver to set (optional)
        """
        self.config_id = config_id
        self.frequency_band = frequency_band
        self.subarray_id = subarray_id
        self.band_5_tuning = band_5_tuning

    def __eq__(self, other):
        if not isinstance(other, CommonConfiguration):
            return False
        return (
            self.config_id == other.config_id
            and self.frequency_band == other.frequency_band
            and self.subarray_id == other.subarray_id
            and self.band_5_tuning == other.band_5_tuning
        )


class StnBeamConfiguration:
    """
    Class to hold Stations Beam Configuration.
    """

    def __init__(
        self,
        beam_id: int = None,
        freq_ids: List[int] = None,
        boresight_dly_poly: str = None,
    ) -> object:
        """
        Create a new StnBeamConfiguration.

        :param beam_id: beam_id
        :param freq_ids: freq_ids
        :param boresight_dly_poly: boresight_dly_poly
        """
        self.beam_id = beam_id
        self.freq_ids = freq_ids
        self.boresight_dly_poly = boresight_dly_poly

    def __eq__(self, other):
        if not isinstance(other, StnBeamConfiguration):
            return False
        return (
            self.beam_id == other.beam_id
            and self.freq_ids == other.freq_ids
            and self.boresight_dly_poly == other.boresight_dly_poly
        )


class StationConfiguration:
    """
    Class to hold Stations Configuration.
    """

    def __init__(
        self,
        stns: List[List[int]] = None,
        stn_beams: List[StnBeamConfiguration] = None,
    ):
        """
        Create a new StationConfiguration.

        :param stns: stns
        :param stn_beams: stn_beams
        """
        self.stns = stns
        self.stn_beams = stn_beams

    def __eq__(self, other):
        if not isinstance(other, StationConfiguration):
            return False
        return self.stns == other.stns and self.stn_beams == other.stn_beams


class BeamConfiguration:
    """
    Class to hold Beams Configuration.
    """

    def __init__(
        self,
        pst_beam_id: int = None,
        stn_beam_id: int = None,
        offset_dly_poly: str = None,
        stn_weights: List[float] = None,
        jones: str = None,
        dest_chans: List[int] = None,
        rfi_enable: List[bool] = None,
        rfi_static_chans: List[int] = None,
        rfi_dynamic_chans: List[int] = None,
        rfi_weighted: float = None,
    ) -> object:
        """
        Create a new BeamConfiguration.

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
        self.pst_beam_id = pst_beam_id
        self.stn_beam_id = stn_beam_id
        self.offset_dly_poly = offset_dly_poly
        self.stn_weights = stn_weights
        self.jones = jones
        self.dest_chans = dest_chans
        self.rfi_enable = rfi_enable
        self.rfi_static_chans = rfi_static_chans
        self.rfi_dynamic_chans = rfi_dynamic_chans
        self.rfi_weighted = rfi_weighted

    def __eq__(self, other):
        if not isinstance(other, BeamConfiguration):
            return False
        return (
            self.pst_beam_id == other.pst_beam_id
            and self.stn_beam_id == other.stn_beam_id
            and self.offset_dly_poly == other.offset_dly_poly
            and self.stn_weights == other.stn_weights
            and self.jones == other.jones
            and self.dest_chans == other.dest_chans
            and self.rfi_enable == other.rfi_enable
            and self.rfi_static_chans == other.rfi_static_chans
            and self.rfi_dynamic_chans == other.rfi_dynamic_chans
            and self.rfi_weighted == other.rfi_weighted
        )


class TimingBeamConfiguration:
    """
    Class to hold Timing Beams Configuration.
    """

    def __init__(
        self,
        beams: List[BeamConfiguration] = None,
    ) -> object:
        """
        Create a new TimingBeamConfiguration.

        :param beams: beams
        """
        self.beams = beams

    def __eq__(self, other):
        if not isinstance(other, TimingBeamConfiguration):
            return False
        return self.beams == other.beams


class LowCBFConfiguration:
    """
    Class to hold Low CBF Configuration.
    """

    def __init__(
        self,
        stations: StationConfiguration = None,
        timing_beams: TimingBeamConfiguration = None,
    ) -> object:
        """
        Create a new LowCBFConfiguration.

        :param stations: stations
        :param timing_beams: PST beams subarray list
        """
        self.stations = stations
        self.timing_beams = timing_beams

    def __eq__(self, other):
        if not isinstance(other, LowCBFConfiguration):
            return False
        return (
            self.stations == other.stations and self.timing_beams == other.timing_beams
        )


class VLBIConfiguration:
    pass


class CBFConfiguration:
    """
    Class to hold all FSP and VLBI configurations.
    """

    def __init__(
        self,
        fsp_configs: List[FSPConfiguration],
        # TODO: In future when csp Interface 2.2 will be used than type of vlbi_config parameter                        # pylint: disable=W0511
        #  will be replaced with the respective class(VLBIConfiguration)
        vlbi_config: dict = None,
    ) -> object:
        """
        Create a new CBFConfiguration.
        :param fsp_configs: the FSP configurations to set
        :param vlbi_config: the VLBI configurations to set, it is optional
        """
        self.fsp_configs = fsp_configs
        self.vlbi_config = vlbi_config

    def __eq__(self, other):
        if not isinstance(other, CBFConfiguration):
            return False
        return (
            self.fsp_configs == other.fsp_configs
            and self.vlbi_config == other.vlbi_config
        )


class PSTConfiguration:
    pass


class PSSConfiguration:
    pass


class CSPConfiguration:
    """
    Class to hold all CSP configuration.
    """

    def __init__(
        self,
        interface: str = None,
        subarray: SubarrayConfiguration = None,
        common: CommonConfiguration = None,
        cbf_config: CBFConfiguration = None,
        # TODO: In future when csp Interface 2.2 will be used than type of pst_config and pss_config                    # pylint: disable=W0511
        #  parameter will be replaced with the respective class(PSTConfiguration,PSSConfiguration)
        pst_config: dict = None,
        pss_config: dict = None,
        lowcbf: LowCBFConfiguration = None,
    ) -> object:
        """
        Create a new CSPConfiguration, In order to support backward
        compatibility, We have kept old attributes as it is and added
        support of new attributes as per ADR-18

        :param interface: url string to determine JsonSchema version
        :param subarray: Sub-array configuration to set
        :param common: the common CSP elemenets to set
        :param cbf_config: the CBF configurations to set
        :param pst_config: the PST configurations to set
        :param pss_config: the PSS configurations to set
        """
        self.interface = interface
        self.subarray = subarray
        self.common = common
        self.cbf_config = cbf_config
        self.pst_config = pst_config
        self.pss_config = pss_config
        self.lowcbf = lowcbf

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return (
            self.interface == other.interface
            and self.subarray == other.subarray
            and self.common == other.common
            and self.cbf_config == other.cbf_config
            and self.pst_config == other.pst_config
            and self.pss_config == other.pss_config
            and self.lowcbf == other.lowcbf
        )
