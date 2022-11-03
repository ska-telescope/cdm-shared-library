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
    ):
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

    def __init__(self, subarray_name: str):
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
        config_id: str,
        frequency_band: core.ReceiverBand,
        subarray_id: int = None,
        band_5_tuning: Optional[List[float]] = None,
    ):
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


class VLBIConfiguration:
    pass


class CBFConfiguration:
    """
    Class to hold all FSP and VLBI configurations.
    """

    def __init__(
        self,
        fsp_configs: List[FSPConfiguration],
        # Todo in future when csp 2.2 will be used than type of vlbi_config parameter will be replaced with the respective class(VLBIConfiguration)
        vlbi_config: dict = None
    ):
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
        subarray_config: SubarrayConfiguration = None,
        common_config: CommonConfiguration = None,
        cbf_config: CBFConfiguration = None,
        #Todo in future when csp2.2 will be used than type of pst_config and pss_config parameter will be replaced with the respective class(PSTConfiguration,PSSConfiguration)
        pst_config: dict = None,
        pss_config: dict = None
    ):
        """
        Create a new CSPConfiguration, In order to support backward
        compatibility, We have kept old attributes as it is and added
        support of new attributes as per ADR-18

        :param interface: url string to determine JsonSchema version
        :param subarray_config: Sub-array configuration to set
        :param common_config: the common CSP elemenets to set
        :param cbf_config: the CBF configurations to set
        :param pst_config: the PST configurations to set
        :param pss_config: the PSS configurations to set
        """
        self.interface = interface
        self.subarray_config = subarray_config
        self.common_config = common_config
        self.cbf_config = cbf_config
        self.pst_config = pst_config
        self.pss_config = pss_config

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return (
            self.interface == other.interface
            and self.subarray_config == other.subarray_config
            and self.common_config == other.common_config
            and self.cbf_config == other.cbf_config
            and self.pst_config == other.pst_config
            and self.pss_config == other.pss_config
        )
